from django.shortcuts import get_object_or_404
import json
import time
from channels.generic.websocket import WebsocketConsumer
import paramiko


class RunJobConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        job_id = self.scope['url_route']['kwargs']['id']
        self.run_job(job_id)

    def establish_ssh_connection(self, hostname, username, password):
        connection = paramiko.SSHClient()
        connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            connection.connect(hostname, username=username, password=password)
            return connection
        except Exception as error:
            print(f"Failed to connect: {error}")
            return False

    def run_ssh_command(self, command, ssh_client):
        stdin, stdout, stderr = ssh_client.exec_command(command, get_pty=True)
        output_lines = []

        for line in iter(stdout.readline, ""):
            self.send(text_data=json.dumps({"message": line.strip()}))
            output_lines.append(line)

        return output_lines

    def run_job(self, job_id):
        from .models import Job, JobRunned

        job_run = get_object_or_404(JobRunned, id=int(job_id))  # Ensure correct field usage
        job = get_object_or_404(Job, id=job_run.job.id)  # Ensure correct field usage
        playbook = job.playbook
        inventory = job.inventory

        ansible_server_hostname = "10.10.20.2"
        ansible_server_username = "netadmin"
        ansible_server_password = "TFBern_3013"

        ssh_client = self.establish_ssh_connection(hostname=ansible_server_hostname, username=ansible_server_username, password=ansible_server_password)

        self.run_ssh_command(f"echo '{playbook.content}' > /home/netadmin/ansible/playbook.yml", ssh_client)
        self.run_ssh_command(f"echo '{inventory.content}' > /home/netadmin/ansible/inventory", ssh_client)

        output = self.run_ssh_command(
            "ansible-playbook /home/netadmin/ansible/playbook.yml -i /home/netadmin/ansible/inventory", ssh_client)

        self.run_ssh_command("rm -rf /home/netadmin/ansible/playbook.yml /home/netadmin/ansible/inventory", ssh_client)

        self.run_ssh_command("rm -rf ansible/playbook.yml ansible/inventory", ssh_client)
        self.run_ssh_command("rm -rf /tmp/vault_password.txt", ssh_client)

        job_run.output = output
        job_run.has_run = True
        job_run.save()


