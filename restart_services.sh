#!/bin/bash

# Definiere den Pfad zum virtuellen Environment und zum Projekt
VENV_DIR="/home/netadmin/venv"
PROJECT_DIR="/home/netadmin/ansible"

# Daphne stoppen
echo "Daphne wird gestoppt..."
pkill -f "daphne -b 127.0.0.1 -p 8000 ansible.asgi:application"

# Überprüfen, ob der Befehl erfolgreich war
if [ $? -eq 0 ]; then
    echo "Daphne erfolgreich gestoppt."
else
    echo "Fehler beim Stoppen von Daphne oder Daphne ist bereits gestoppt."
fi

# Apache neu starten
echo "Apache wird neu gestartet..."
sudo systemctl restart apache2

# Überprüfen, ob Apache erfolgreich neu gestartet wurde
if [ $? -eq 0 ]; then
    echo "Apache erfolgreich neu gestartet."
else
    echo "Fehler beim Neustart von Apache."
    exit 1
fi

# Wechseln in das Projektverzeichnis und das virtuelle Environment aktivieren
echo "Wechseln in das Projektverzeichnis und Aktivieren des virtuellen Environments..."
cd $PROJECT_DIR || { echo "Fehler beim Wechseln in das Projektverzeichnis."; exit 1; }
source $VENV_DIR/bin/activate || { echo "Fehler beim Aktivieren des virtuellen Environments."; exit 1; }

# Daphne starten
echo "Daphne wird gestartet..."
nohup daphne -b 127.0.0.1 -p 8000 ansible.asgi:application > daphne.log 2>&1 &

# Überprüfen, ob Daphne erfolgreich gestartet wurde
if [ $? -eq 0 ]; then
    echo "Daphne erfolgreich gestartet."
else
    echo "Fehler beim Starten von Daphne."
    exit 1
fi

echo "Dienste erfolgreich neu gestartet."
