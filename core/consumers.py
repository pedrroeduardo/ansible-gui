from django.shortcuts import get_object_or_404
from django.http import Http404
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import paramiko
from asgiref.sync import sync_to_async
import logging
import time

logger = logging.getLogger(__name__)


class RunJobConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        logger.info("WebSocket connected.")

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected with code: {close_code}")

    async def receive(self, text_data):
        job_id = self.scope['url_route']['kwargs']['id']
        logger.info(f"Received job ID: {job_id}")
        try:
            await self.run_job(job_id)
        except Http404:
            await self.send(text_data=json.dumps({"redirect": True, "url": "/dashboard"}))
            await self.close()

    async def establish_ssh_connection(self, hostname, username, password):
        connection = paramiko.SSHClient()
        connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            connection.connect(hostname, username=username, password=password)
            return connection
        except Exception as error:
            logger.error(f"Failed to connect: {error}")
            return None

    async def run_ssh_command(self, command, ssh_client):
        stdin, stdout, stderr = ssh_client.exec_command(command, get_pty=True)
        output_lines = []

        async for line in self.async_readline(stdout):
            await self.send(text_data=json.dumps({"message": line.strip()}))
            output_lines.append(line)

        return output_lines

    async def async_readline(self, stream):
        while True:
            line = await sync_to_async(stream.readline)()
            if not line:
                break
            yield line

    @sync_to_async
    def update_job_status(self, job_run_id, output):
        from .models import JobRunned, Status

        try:
            job_run = JobRunned.objects.get(id=job_run_id)
            job_run.output = output
            job_run.has_run = True
            job_run.save()

            recap_lines = [line for line in output.splitlines() if line.startswith('PLAY RECAP')]
            failed_tasks = 0
            unreachable_hosts = 0

            error_keywords = ["ERROR!", "fatal:", "UNREACHABLE"]
            critical_error = any(keyword in output for keyword in error_keywords)

            if recap_lines:
                logger.info("Found PLAY RECAP")
                recap_index = output.splitlines().index(recap_lines[0])
                for line in output.splitlines()[recap_index:]:
                    if "failed=" in line:
                        failed_tasks += int(line.split("failed=")[1].split()[0])
                    if "unreachable=" in line:
                        unreachable_hosts += int(line.split("unreachable=")[1].split()[0])

                if failed_tasks > 0 or unreachable_hosts > 0:
                    logger.info("Setting status to Fehlgeschlagen")
                    status = Status.objects.get(name="Fehlgeschlagen")
                    logger.info(f"Status found: {status}")
                    job_run.status = status
                    job_run.save()
                else:
                    logger.info("Setting status to Erfolgreich")
                    status = Status.objects.get(name="Erfolgreich")
                    logger.info(f"Status found: {status}")
                    job_run.status = status
                    job_run.save()
            elif critical_error:
                logger.info("Found critical error")
                status = Status.objects.get(name="Fehlgeschlagen")
                logger.info(f"Status found: {status}")
                job_run.status = status
                job_run.save()
            else:
                logger.info("Setting status to Fehlgeschlagen due to unknown error")
                status = Status.objects.get(name="Fehlgeschlagen")
                logger.info(f"Status found: {status}")
                job_run.status = status
                job_run.save()

            return job_run
        except JobRunned.DoesNotExist:
            logger.info("JobRunned does not Exist")
            return None
        except Status.DoesNotExist:
            logger.info("Status does not Exist")
            return None

    @sync_to_async
    def get_job_run(self, job_id):
        from .models import JobRunned
        job_run = get_object_or_404(JobRunned, id=job_id)
        if job_run.has_run:
            raise Http404("Job already executed")
        return job_run

    @sync_to_async
    def get_job(self, job_id):
        from .models import Job
        return get_object_or_404(Job, id=job_id)

    async def run_job(self, job_id):
        logger.info("Starting job.")
        job_run = await self.get_job_run(int(job_id))

        job = await sync_to_async(lambda: job_run.job)()  # Ensure job is fetched asynchronously
        playbook = await sync_to_async(lambda: job.playbook)()
        inventory = await sync_to_async(lambda: job.inventory)()

        ansible_server_hostname = "10.10.20.2"
        ansible_server_username = "netadmin"
        ansible_server_password = "TFBern_3013"

        ssh_client = await self.establish_ssh_connection(
            hostname=ansible_server_hostname,
            username=ansible_server_username,
            password=ansible_server_password
        )

        if not ssh_client:
            await self.send(text_data=json.dumps({"message": "SSH connection failed"}))
            logger.error("SSH connection failed.")
            return

        try:
            logger.info("Running SSH commands.")
            await self.run_ssh_command(f"echo '{playbook.content}' > /home/netadmin/ansible/playbook.yml", ssh_client)
            await self.run_ssh_command(f"echo '{inventory.content}' > /home/netadmin/ansible/inventory", ssh_client)

            output = await self.run_ssh_command(
                "ansible-playbook /home/netadmin/ansible/playbook.yml -i /home/netadmin/ansible/inventory", ssh_client
            )

            # Save job status and output
            await self.update_job_status(job_run.id, "\n".join(output))
            await self.send(text_data=json.dumps({"message": "Job completed successfully", "status": True}))
            logger.info("Job completed successfully.")

        except Exception as e:
            await self.send(text_data=json.dumps({"message": f"Error during job execution: {e}"}))
            logger.error(f"Error during job execution: {e}")
        finally:
            logger.info("Cleaning up.")
            await self.run_ssh_command("rm -rf /home/netadmin/ansible/playbook.yml /home/netadmin/ansible/inventory",
                                       ssh_client)
            await self.run_ssh_command("rm -rf ansible/playbook.yml ansible/inventory", ssh_client)
            await self.run_ssh_command("rm -rf /tmp/vault_password.txt", ssh_client)

            await self.send(text_data=json.dumps({"redirect": True, "url": f"/jobs/run/details/{job_id}"}))

            ssh_client.close()
