from django.urls import path

from .views.login import index
from .views.logout import logout_view
from .views.dashboard import dashboard

from .views.inventory.inventory import inventory
from .views.inventory.create_inventory import create_inventory
from .views.inventory.inventory_details import item_inventory_details

from .views.playbook.playbook import playbook
from .views.playbook.create_playbook import create_playbook
from .views.playbook.playbook_details import item_playbook_details

from .views.jobs.jobs import jobs
from .views.jobs.create_job import create_job
from .views.jobs.job_details import item_job_details
from .views.jobs.run_job import create_new_job_run, run_job, details_run_job

urlpatterns = [
    path("", index),
    path("dashboard/", dashboard, name="dashboard"),
    path("logout/", logout_view, name="logout"),


    path("inventory/", inventory, name="inventory"),
    path("inventory/details/<int:id>", item_inventory_details, name="inventory_details"),
    path("inventory/create-inventory/", create_inventory, name="create-inventory"),

    path("playbook/", playbook, name="playbook"),
    path("playbook/create-playbook/", create_playbook, name="create-playbook"),
    path("playbook/details/<int:id>", item_playbook_details, name="playbook_details"),

    path("jobs/", jobs, name="jobs"),
    path("jobs/create-job/", create_job, name="create-job"),
    path("jobs/details/<int:id>", item_job_details, name="job_details"),
    path("jobs/run/create/<int:id>/", create_new_job_run, name="create-run-job"),
    path("jobs/run/<int:id>", run_job, name="run-job"),
    path("jobs/run/details/<int:id>", details_run_job, name="details-run-job"),
]
