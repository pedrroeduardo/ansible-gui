from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import *
from ldap3.core.exceptions import LDAPException
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import get_object_or_404

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
                            group = Group.objects.get(name=group_name)
                            user.groups.add(group)
                        except Group.DoesNotExist:
                            error_message = "Grupo não encontrado."

                        return redirect('dashboard/')
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
    return render(request, "dashboard.html")


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

    if "Fachgruppe Leitung" in user_group_names or "Fachgruppenübergreifend" in user_group_names:
        inventory = Inventory.objects.all()
    else:
        inventory = Inventory.objects.filter(group__in=core_groups)

    return render(request, "inventory.html", {"inventory": inventory})


@login_required
def playbook(request):
    # Obtendo os nomes dos grupos do usuário
    user_group_names = request.user.groups.all().values_list('name', flat=True)
    user_group_names = list(user_group_names)  # Convertendo para lista

    # Buscando os grupos correspondentes no modelo Core
    core_groups = Group.objects.filter(name__in=user_group_names)

    if "Fachgruppe Leitung" in user_group_names or "Fachgruppenübergreifend" in user_group_names:
        playbook = Playbook.objects.all()
    else:
        playbook = Playbook.objects.filter(group__in=core_groups)

    return render(request, "playbook.html", {"playbook": playbook})


@login_required
def create_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            inventory_name = form.cleaned_data['inventory_name']
            group = form.cleaned_data['group']
            group_model = get_object_or_404(Group, name=group)
            description = form.cleaned_data['description']
            content = form.cleaned_data['content']

            new_inventory = Inventory()
            new_inventory.name = inventory_name
            new_inventory.group = group_model
            new_inventory.description = description
            new_inventory.content = content
            new_inventory.save()

            return redirect('inventory')
        else:
            print("Formulário inválido", form.errors)
    else:
        form = InventoryForm()

    return render(request, "createinventory.html", {'form': form})


@login_required
def create_playbook(request):
    if request.method == 'POST':
        form = PlaybookForm(request.POST)
        if form.is_valid():
            playbook_name = form.cleaned_data['inventory_name']
            group = form.cleaned_data['group']
            group_model = get_object_or_404(Group, name=group)
            description = form.cleaned_data['description']
            content = form.cleaned_data['content']

            new_inventory = Playbook()
            new_inventory.name = playbook_name
            new_inventory.group = group_model
            new_inventory.description = description
            new_inventory.content = content
            new_inventory.save()

            return redirect('playbook')  # Certifique-se que 'dashboard' é uma URL nomeada correta
        else:
            print("Formulário inválido", form.errors)  # Mostra os erros de validação
    else:
        form = PlaybookForm()

    return render(request, "createplaybook.html", {'form': form})

@login_required
def create_job(request):
    user_group_names = request.user.groups.all().values_list('name', flat=True)
    user_group_names = list(user_group_names)
    core_groups = Group.objects.filter(name__in=user_group_names)

    if "Fachgruppe Leitung" in user_group_names or "Fachgruppenübergreifend" in user_group_names:
        playbook = Playbook.objects.all()
        inventory = Inventory.objects.all()
    else:
        playbook = Playbook.objects.filter(group__in=core_groups)
        inventory = Inventory.objects.filter(group__in=core_groups)

    playbook_choices = [(pb.id, pb.name) for pb in playbook]
    inventory_choices = [(iv.id, iv.name) for iv in inventory]

    if request.method == 'POST':
        form = JobForm(request.POST, playbook=playbook_choices, inventory=inventory_choices)
        if form.is_valid():
            name = form.cleaned_data['name']
            inventory = get_object_or_404(Inventory, id=form.cleaned_data['inventory'])
            playbook = get_object_or_404(Playbook, id=form.cleaned_data['playbook'])
            group = get_object_or_404(Group, name=form.cleaned_data['group'])
            description = form.cleaned_data['description']

            new_job = Job()
            new_job.name = name
            new_job.group = group
            new_job.playbook = playbook
            new_job.inventory = inventory
            new_job.description = description
            new_job.save()

            return redirect('jobs')
        else:
            print("Formulário inválido", form.errors)
    else:
        form = JobForm(request.POST, playbook=playbook_choices, inventory=inventory_choices)

    return render(request, "createjob.html", {'form': form})

@login_required
def item_inventory_details(request, id):
    inventory = get_object_or_404(Inventory, pk=id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'edit':
            form = InventoryForm(request.POST)
            if form.is_valid():
                inventory.name = form.cleaned_data['inventory_name']
                inventory.group = get_object_or_404(Group, name=form.cleaned_data['group'])
                inventory.description = form.cleaned_data['description']
                inventory.content = form.cleaned_data['content']
                inventory.save()
                return redirect('inventory')
            else:
                print("Formulário inválido", form.errors)

        elif action == 'delete':
            inventory.delete()
            return redirect('inventory')

        elif action == 'cancel':
            return redirect('inventory')

        # Retorna ao formulário se não houver ação reconhecida ou o formulário não for válido
        initial_data = {
            'inventory_name': inventory.name,
            'group': inventory.group.name if inventory.group else None,
            'description': inventory.description,
            'content': inventory.content
        }
        form = InventoryForm(initial=initial_data)
        return render(request, 'details.html', {'form': form, 'inventory': inventory})

    else:
        # Preparar o formulário para GET request
        initial_data = {
            'inventory_name': inventory.name,
            'group': inventory.group.name if inventory.group else None,
            'description': inventory.description,
            'content': inventory.content
        }
        form = InventoryForm(initial=initial_data)
        return render(request, 'details.html', {'form': form, 'inventory': inventory})


@login_required
def item_job_details(request, id):
    job = get_object_or_404(Job, pk=id)
    error_message = ""

    user_group_names = request.user.groups.all().values_list('name', flat=True)
    user_group_names = list(user_group_names)
    core_groups = Group.objects.filter(name__in=user_group_names)

    if "Fachgruppe Leitung" in user_group_names or "Fachgruppenübergreifend" in user_group_names:
        playbook = Playbook.objects.all()
        inventory = Inventory.objects.all()
    else:
        playbook = Playbook.objects.filter(group__in=core_groups)
        inventory = Inventory.objects.filter(group__in=core_groups)

    playbook_choices = [(pb.id, pb.name) for pb in playbook]
    inventory_choices = [(iv.id, iv.name) for iv in inventory]

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'edit':
            form = JobForm(request.POST, playbook=playbook_choices, inventory=inventory_choices)
            if form.is_valid():
                job.name = form.cleaned_data['name']
                job.group = get_object_or_404(Group, name=form.cleaned_data['group'])
                job.playbook = get_object_or_404(Playbook, id=form.cleaned_data['playbook'])
                job.inventory = get_object_or_404(Inventory, id=form.cleaned_data['inventory'])
                job.description = form.cleaned_data['description']
                job.save()
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
        form = JobForm(initial=initial_data, playbook=playbook_choices, inventory=inventory_choices)
        return render(request, 'jobdetails.html', {'form': form, 'inventory': inventory, "error_message": error_message})

    else:
        # Preparar o formulário para GET request
        initial_data = {
            'name': job.name,
            'group': job.group.name if job.group else None,
            'playbook': job.playbook.id if job.playbook else None,
            'inventory': job.inventory.id if job.inventory else None,
            'description': job.description
        }
        form = JobForm(initial=initial_data, playbook=playbook_choices, inventory=inventory_choices)
        return render(request, 'jobdetails.html', {'form': form, 'inventory': inventory, "error_message": error_message})


@login_required
def item_playbook_details(request, id):
    playbook = get_object_or_404(Playbook, pk=id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'edit':
            form = InventoryForm(request.POST)
            if form.is_valid():
                playbook.name = form.cleaned_data['inventory_name']
                playbook.group = get_object_or_404(Group, name=form.cleaned_data['group'])
                playbook.description = form.cleaned_data['description']
                playbook.content = form.cleaned_data['content']
                playbook.save()
                return redirect('playbook')
            else:
                print("Formulário inválido", form.errors)

        elif action == 'delete':
            playbook.delete()
            return redirect('playbook')

        elif action == 'cancel':
            return redirect('playbook')

        # Retorna ao formulário se não houver ação reconhecida ou o formulário não for válido
        initial_data = {
            'inventory_name': playbook.name,
            'group': playbook.group.name if playbook.group else None,
            'description': playbook.description,
            'content': playbook.content
        }
        form = InventoryForm(initial=initial_data)
        return render(request, 'detailsplaybook.html', {'form': form, 'playbook': playbook})

    else:
        # Preparar o formulário para GET request
        initial_data = {
            'inventory_name': playbook.name,
            'group': playbook.group.name if playbook.group else None,
            'description': playbook.description,
            'content': playbook.content
        }
        form = InventoryForm(initial=initial_data)
        return render(request, 'detailsplaybook.html', {'form': form, 'playbook': playbook})


@login_required
def jobs(request):
    # Obtendo os nomes dos grupos do usuário
    user_group_names = request.user.groups.all().values_list('name', flat=True)
    user_group_names = list(user_group_names)  # Convertendo para lista

    # Buscando os grupos correspondentes no modelo Core
    core_groups = Group.objects.filter(name__in=user_group_names)

    if "Fachgruppe Leitung" in user_group_names or "Fachgruppenübergreifend" in user_group_names:
        job = Job.objects.all()
    else:
        job = Job.objects.filter(group__in=core_groups)

    return render(request, 'jobs.html', {"job": job})

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
    return render(request, 'run_job_details.html', {'job_id': id})
