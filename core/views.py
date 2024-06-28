from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
import django
from .forms import *
from ldap3.core.exceptions import LDAPException
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import get_object_or_404
import re

import ldap3


def ldap_login(username):
    server_address = '192.168.10.20'
    search_base = 'DC=it-tf,DC=local'
    search_filter = f'(sAMAccountName={username})'
    bind_username = "CN=LDAP Abfrage,OU=Services,OU=User-IT,DC=it-tf,DC=local"
    bind_password = "Laebchueche_35"

    try:
        with ldap3.Connection(server_address, user=bind_username, password=bind_password) as conn:
            if conn.search(search_base, search_filter, attributes=['distinguishedName']):
                return conn.entries[0].distinguishedName
    except Exception:
        pass
    return None


def authenticate_user(server_address, user_dn, user_password):
    try:
        with ldap3.Connection(server_address, user=str(user_dn), password=user_password) as conn:
            return conn.bind()
    except LDAPException:
        pass
    return False


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard/')

    error_message = ""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_dn = ldap_login(username)

            try:
                if user_dn:
                    authenticated = authenticate_user("192.168.10.20", user_dn, password)
                    if authenticated:
                        user, created = User.objects.get_or_create(username=username)
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        login(request, user)
                        error_message = ""

                        group_name = "Fachgruppenübergreifend"

                        try:
                            group = django.contrib.auth.models.Group.objects.get(name=group_name)
                            print(group)
                            user.groups.add(group)
                            print("Good")
                            return redirect('dashboard/')
                        except Group.DoesNotExist:
                            print("No good")
                            error_message = "Grupo não encontrado."
                    else:
                        error_message = 'Benutzername oder Passwort ist falsch'
                else:
                    error_message = 'Benutzername oder Passwort ist falsch'
            except Exception:
                error_message = 'Benutzername oder Passwort ist falsch'
    else:
        form = LoginForm()

    return render(request, "index.html", {'form': form, 'error_message': error_message})


@login_required
def dashboard(request):
    # Obtendo os nomes dos grupos do usuário
    user_group_names = request.user.groups.all().values_list('name', flat=True)
    user_group_names = list(user_group_names)  # Convertendo para lista

    # Buscando os grupos correspondentes no modelo Core
    core_groups = Group.objects.filter(name__in=user_group_names)

    if "Fachgruppe Leitung" in user_group_names:
        jobs_runned = JobRunned.objects.all()
    else:
        jobs_runned = JobRunned.objects.filter(job__group__in=core_groups)

    return render(request, "dashboard.html", {"jobs": jobs_runned})


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def inventory(request):
    # Obtendo os nomes dos grupos do usuário
    user_group_names = request.user.groups.all().values_list('name', flat=True)
    user_group_names = list(user_group_names)  # Convertendo para lista

    # Buscando os grupos correspondentes no modelo Core
    core_groups = Group.objects.filter(name__in=user_group_names)

    tags = Tag.objects.all()

    selected_tag = request.GET.get('tag')

    if "Fachgruppe Leitung" in user_group_names:
        if selected_tag and selected_tag != 'all':
            inventory = Inventory.objects.filter(tags__name=selected_tag)
        else:
            inventory = Inventory.objects.all()
    else:
        if selected_tag and selected_tag != 'all':
            inventory = Inventory.objects.filter(group__in=core_groups, tags__name=selected_tag)
        else:
            inventory = Inventory.objects.filter(group__in=core_groups)

    return render(request, "inventory.html", {"inventory": inventory, "tags": tags})


@login_required
def playbook(request):
    # Obtendo os nomes dos grupos do usuário
    user_group_names = request.user.groups.all().values_list('name', flat=True)
    user_group_names = list(user_group_names)  # Convertendo para lista

    # Buscando os grupos correspondentes no modelo Core
    core_groups = Group.objects.filter(name__in=user_group_names)
    tags = Tag.objects.all()

    selected_tag = request.GET.get('tag')

    if "Fachgruppe Leitung" in user_group_names:
        if selected_tag and selected_tag != 'all':
            playbook = Playbook.objects.filter(tags__name=selected_tag)
        else:
            playbook = Playbook.objects.all()
    else:
        if selected_tag and selected_tag != 'all':
            playbook = Playbook.objects.filter(group__in=core_groups, tags__name=selected_tag)
        else:
            playbook = Playbook.objects.filter(group__in=core_groups)

    return render(request, "playbook.html", {"playbook": playbook, "tags": tags})


@login_required
def create_inventory(request):
    available_tags = Tag.objects.all()
    tag_choices = [(tag.id, tag.name) for tag in available_tags]

    if request.method == 'POST':
        form = InventoryForm(request.POST, tag_choices=tag_choices)
        if form.is_valid():
            inventory_name = form.cleaned_data['inventory_name']
            group = form.cleaned_data['group']
            group_model = get_object_or_404(Group, name=group)
            description = form.cleaned_data['description']
            content = form.cleaned_data['content']
            selected_tags = form.cleaned_data['selected_tags']

            new_inventory = Inventory()
            new_inventory.name = inventory_name
            new_inventory.group = group_model
            new_inventory.description = description
            new_inventory.content = content
            new_inventory.save()

            # Add the selected tags to the new inventory
            new_inventory.tags.set(selected_tags)
            new_inventory.save()

            return redirect('inventory')
        else:
            # If the form is invalid, we need to manually set the choices again
            form.fields['available_tags'].choices = tag_choices
            form.fields['selected_tags'].choices = [(tag.id, tag.name) for tag in Tag.objects.filter(id__in=form.cleaned_data.get('selected_tags', []))]
            print("Formulário inválido", form.errors)
    else:
        form = InventoryForm(tag_choices=tag_choices)
        form.fields['selected_tags'].choices = []  # Ensure selected tags are initially empty

    return render(request, "createinventory.html", {'form': form})



@login_required
def create_playbook(request):
    available_tags = Tag.objects.all()
    tag_choices = [(tag.id, tag.name) for tag in available_tags]

    if request.method == 'POST':
        form = PlaybookForm(request.POST, tag_choices=tag_choices)
        if form.is_valid():
            playbook_name = form.cleaned_data['inventory_name']
            group = form.cleaned_data['group']
            group_model = get_object_or_404(Group, name=group)
            description = form.cleaned_data['description']
            content = form.cleaned_data['content']
            selected_tags = form.cleaned_data['selected_tags']

            new_playbook = Playbook()
            new_playbook.name = playbook_name
            new_playbook.group = group_model
            new_playbook.description = description
            new_playbook.content = content
            new_playbook.save()

            # Add the selected tags to the new playbook
            new_playbook.tags.set(selected_tags)
            new_playbook.save()

            return redirect('playbook')
        else:
            # If the form is invalid, we need to manually set the choices again
            form.fields['available_tags'].choices = tag_choices
            form.fields['selected_tags'].choices = [(tag.id, tag.name) for tag in Tag.objects.filter(id__in=form.cleaned_data.get('selected_tags', []))]
            print("Formulário inválido", form.errors)
    else:
        form = PlaybookForm(tag_choices=tag_choices)
        form.fields['selected_tags'].choices = []  # Ensure selected tags are initially empty

    return render(request, "createplaybook.html", {'form': form})


@login_required
def create_job(request):
    user_group_names = request.user.groups.all().values_list('name', flat=True)
    user_group_names = list(user_group_names)
    core_groups = Group.objects.filter(name__in=user_group_names)

    if "Fachgruppe Leitung" in user_group_names:
        playbook = Playbook.objects.all()
        inventory = Inventory.objects.all()
        available_tags = Tag.objects.all()
    else:
        playbook = Playbook.objects.filter(group__in=core_groups)
        inventory = Inventory.objects.filter(group__in=core_groups)
        available_tags = Tag.objects.filter(group__in=core_groups)

    playbook_choices = [(pb.id, pb.name) for pb in playbook]
    inventory_choices = [(iv.id, iv.name) for iv in inventory]
    tag_choices = [(tag.id, tag.name) for tag in available_tags]

    if request.method == 'POST':
        form = JobForm(request.POST, playbook=playbook_choices, inventory=inventory_choices, tag_choices=tag_choices)
        if form.is_valid():
            name = form.cleaned_data['name']
            inventory = get_object_or_404(Inventory, id=form.cleaned_data['inventory'])
            playbook = get_object_or_404(Playbook, id=form.cleaned_data['playbook'])
            group = get_object_or_404(Group, name=form.cleaned_data['group'])
            description = form.cleaned_data['description']
            selected_tags = form.cleaned_data['selected_tags']

            new_job = Job()
            new_job.name = name
            new_job.group = group
            new_job.playbook = playbook
            new_job.inventory = inventory
            new_job.description = description
            new_job.save()

            # Add the selected tags to the new job
            new_job.tags.set(selected_tags)
            new_job.save()

            return redirect('jobs')
        else:
            # If the form is invalid, we need to manually set the choices again
            form.fields['available_tags'].choices = tag_choices
            form.fields['selected_tags'].choices = [(tag.id, tag.name) for tag in Tag.objects.filter(id__in=form.cleaned_data.get('selected_tags', []))]
            print("Formulário inválido", form.errors)
    else:
        form = JobForm(playbook=playbook_choices, inventory=inventory_choices, tag_choices=tag_choices)
        form.fields['selected_tags'].choices = []  # Ensure selected tags are initially empty

    return render(request, "createjob.html", {'form': form})


@login_required
def item_inventory_details(request, id):
    inventory = get_object_or_404(Inventory, pk=id)
    available_tags = Tag.objects.all()
    tag_choices = [(tag.id, tag.name) for tag in available_tags]
    selected_tag_ids = list(inventory.tags.values_list('id', flat=True))

    if request.method == 'POST':
        action = request.POST.get('action')
        submitted_tag_ids = request.POST.getlist('selected_tags')
        all_selected_ids = list(set(selected_tag_ids + [int(tag_id) for tag_id in submitted_tag_ids]))
        form = InventoryDetailsForm(request.POST, tag_choices=tag_choices, selected_tag_ids=all_selected_ids)
        if form.is_valid():
            if action == 'edit':
                inventory.name = form.cleaned_data['inventory_name']
                inventory.group = get_object_or_404(Group, name=form.cleaned_data['group'])
                inventory.description = form.cleaned_data['description']
                inventory.content = form.cleaned_data['content']
                selected_tags = form.cleaned_data['selected_tags']
                inventory.save()
                inventory.tags.set(Tag.objects.filter(id__in=selected_tags))
                return redirect('inventory')
            elif action == 'delete':
                inventory.delete()
                return redirect('inventory')
            elif action == 'cancel':
                return redirect('inventory')
        else:
            print("Formulário inválido", form.errors)
            print("Submitted data:", request.POST)
            print("Tag choices:", tag_choices)
            print("Selected tag ids:", selected_tag_ids)
    else:
        initial_data = {
            'inventory_name': inventory.name,
            'group': inventory.group.name if inventory.group else None,
            'description': inventory.description,
            'content': inventory.content
        }
        form = InventoryDetailsForm(initial=initial_data, tag_choices=tag_choices, selected_tag_ids=selected_tag_ids)

    return render(request, 'details.html', {'form': form, 'inventory': inventory})

@login_required
def item_job_details(request, id):
    job = get_object_or_404(Job, pk=id)
    error_message = ""

    user_group_names = request.user.groups.all().values_list('name', flat=True)
    user_group_names = list(user_group_names)
    core_groups = Group.objects.filter(name__in=user_group_names)

    if "Fachgruppe Leitung" in user_group_names:
        playbook = Playbook.objects.all()
        inventory = Inventory.objects.all()
    else:
        playbook = Playbook.objects.filter(group__in=core_groups)
        inventory = Inventory.objects.filter(group__in=core_groups)

    playbook_choices = [(pb.id, pb.name) for pb in playbook]
    inventory_choices = [(iv.id, iv.name) for iv in inventory]

    available_tags = Tag.objects.all()
    tag_choices = [(tag.id, tag.name) for tag in available_tags]
    selected_tag_ids = list(job.tags.values_list('id', flat=True))

    if request.method == 'POST':
        action = request.POST.get('action')
        submitted_tag_ids = request.POST.getlist('selected_tags')
        all_selected_ids = list(set(selected_tag_ids + [int(tag_id) for tag_id in submitted_tag_ids]))
        form = JobForm(request.POST, playbook=playbook_choices, inventory=inventory_choices, tag_choices=tag_choices, selected_tag_ids=all_selected_ids)
        if form.is_valid():
            if action == 'edit':
                job.name = form.cleaned_data['name']
                job.group = get_object_or_404(Group, name=form.cleaned_data['group'])
                job.playbook = get_object_or_404(Playbook, id=form.cleaned_data['playbook'])
                job.inventory = get_object_or_404(Inventory, id=form.cleaned_data['inventory'])
                job.description = form.cleaned_data['description']
                job.save()
                job.tags.set(Tag.objects.filter(id__in=form.cleaned_data['selected_tags']))
                return redirect('jobs')
            else:
                error_message = form.errors

        elif action == 'delete':
            job.delete()
            return redirect('jobs')

        elif action == 'cancel':
            return redirect('jobs')

        # Retorna ao formulário se não houver ação reconhecida ou o formulário não for válido
        initial_data = {
            'name': job.name,
            'group': job.group.name if job.group else None,
            'playbook': job.playbook.id if job.playbook else None,
            'inventory': job.inventory.id if job.inventory else None,
            'description': job.description
        }
        form = JobForm(initial=initial_data, playbook=playbook_choices, inventory=inventory_choices, tag_choices=tag_choices, selected_tag_ids=selected_tag_ids)
    else:
        initial_data = {
            'name': job.name,
            'group': job.group.name if job.group else None,
            'playbook': job.playbook.id if job.playbook else None,
            'inventory': job.inventory.id if job.inventory else None,
            'description': job.description
        }
        form = JobForm(initial=initial_data, playbook=playbook_choices, inventory=inventory_choices, tag_choices=tag_choices, selected_tag_ids=selected_tag_ids)

    return render(request, 'jobdetails.html', {'form': form, 'job': job, 'error_message': error_message})



@login_required
def item_playbook_details(request, id):
    playbook = get_object_or_404(Playbook, pk=id)
    available_tags = Tag.objects.all()
    tag_choices = [(tag.id, tag.name) for tag in available_tags]
    selected_tag_ids = list(playbook.tags.values_list('id', flat=True))

    if request.method == 'POST':
        action = request.POST.get('action')
        submitted_tag_ids = request.POST.getlist('selected_tags')
        all_selected_ids = list(set(selected_tag_ids + [int(tag_id) for tag_id in submitted_tag_ids]))
        form = PlaybookDetailsForm(request.POST, tag_choices=tag_choices, selected_tag_ids=all_selected_ids)
        if form.is_valid():
            if action == 'edit':
                playbook.name = form.cleaned_data['playbook_name']
                playbook.group = get_object_or_404(Group, name=form.cleaned_data['group'])
                playbook.description = form.cleaned_data['description']
                playbook.content = form.cleaned_data['content']
                playbook.save()
                playbook.tags.set(Tag.objects.filter(id__in=form.cleaned_data['selected_tags']))
                return redirect('playbook')
            elif action == 'delete':
                playbook.delete()
                return redirect('playbook')
            elif action == 'cancel':
                return redirect('playbook')
        else:
            print("Formulário inválido", form.errors)
            print("Submitted data:", request.POST)
            print("Tag choices:", tag_choices)
            print("Selected tag ids:", selected_tag_ids)
    else:
        initial_data = {
            'playbook_name': playbook.name,
            'group': playbook.group.name if playbook.group else None,
            'description': playbook.description,
            'content': playbook.content
        }
        form = PlaybookDetailsForm(initial=initial_data, tag_choices=tag_choices, selected_tag_ids=selected_tag_ids)

    return render(request, 'detailsplaybook.html', {'form': form, 'playbook': playbook})



@login_required
def jobs(request):
    # Obtendo os nomes dos grupos do usuário
    user_group_names = request.user.groups.all().values_list('name', flat=True)
    user_group_names = list(user_group_names)

    # Buscando os grupos correspondentes no modelo Core
    core_groups = Group.objects.filter(name__in=user_group_names)
    tags = Tag.objects.all()

    selected_tag = request.GET.get('tag')

    if "Fachgruppe Leitung" in user_group_names:
        if selected_tag and selected_tag != 'all':
            job = Job.objects.filter(tags__name=selected_tag)
        else:
            job = Job.objects.all()
    else:
        if selected_tag and selected_tag != 'all':
            job = Job.objects.filter(group__in=core_groups, tags__name=selected_tag)
        else:
            job = Job.objects.filter(group__in=core_groups)

    return render(request, 'jobs.html', {"job": job, "tags": tags, "selected_tag": selected_tag})

@login_required
def create_new_job_run(request, id):
    job = get_object_or_404(Job, id=id)
    job_runned = JobRunned.objects.create(
        job=job,
        username=request.user.username,
        output="",
        status=Status.objects.get(name="Laufend")
    )
    return redirect('run-job', id=job_runned.id)

@login_required
def run_job(request, id):
    job = get_object_or_404(JobRunned, id=id)
    return render(request, 'run_job_details.html', {'job_id': id, "jobs": job})


@login_required
def details_run_job(request, id):
    job = get_object_or_404(JobRunned, id=id)

    output = re.sub(r'\\n', '\n', job.output)
    processed_output = "\n".join([line for line in output.splitlines() if line.strip() != ""])

    return render(request, 'job_details.html', {'jobs': job, 'processed_output': processed_output})
