from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
import django
from core.forms.login_form import LoginForm
from ldap3.core.exceptions import LDAPException
from core.models import *

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
                            user.groups.add(group)
                            return redirect('dashboard/')
                        except Group.DoesNotExist:
                            error_message = "Gruppe wurde nicht gefunden"
                    else:
                        error_message = 'Benutzername oder Passwort ist falsch'
                else:
                    error_message = 'Benutzername oder Passwort ist falsch'
            except Exception:
                error_message = 'Benutzername oder Passwort ist falsch'
    else:
        form = LoginForm()

    return render(request, "index.html", {'form': form, 'error_message': error_message})
