KanMind - DRF Backend

KanMind ist ein Backend-Service, entwickelt mit Django REST Framework (DRF), um eine effiziente Verwaltung von Aufgaben und Projekten zu ermöglichen. Mit der Anwendung können Benutzer ihre Arbeitsprozesse nach dem Kanban-Prinzip organisieren, Aufgaben zuweisen und den Fortschritt verfolgen.

Funktionen

Benutzerverwaltung: Benutzer können sich registrieren und anmelden. Der Zugriff wird durch rollenbasierte Berechtigungen kontrolliert.

Projekt- und Aufgabenverwaltung: Erstellen, Bearbeiten und Löschen von Projekten und Aufgaben.

Priorisierung und Kategorisierung: Aufgaben können nach Dringlichkeit und Kategorie sortiert werden.

REST API: Die API bietet eine einfache Integration mit Frontend-Anwendungen.


Installation

Repository klonen:

git clone https://github.com/alwaysMercy/Backend/tree/main/KanMind-Backend
cd KanMind-Backend


Virtuelle Umgebung erstellen:

python -m venv venv
source venv/bin/activate  # Auf Windows: venv\Scripts\activate


Abhängigkeiten installieren:

pip install -r requirements.txt


Datenbank-Migrationen durchführen:

python manage.py migrate


Entwicklungsserver starten:

python manage.py runserver

API Endpoints

Die API bietet die folgenden Endpoints:

/api/auth/register/: Benutzerregistrierung

/api/auth/login/: Benutzeranmeldung

/api/projects/: Verwaltung von Projekten (Erstellen, Bearbeiten, Löschen)

/api/tasks/: Verwaltung von Aufgaben (Erstellen, Bearbeiten, Löschen)

Eine detaillierte Dokumentation der API-Endpunkte kann mit Swagger oder Postman aufgerufen werden.

Tests

Die Tests können mit folgendem Befehl ausgeführt werden:

python manage.py test

Mitwirken

Beiträge sind immer willkommen! Um Änderungen vorzuschlagen, erstelle einfach einen Pull Request. Achte darauf, dass dein Code gut dokumentiert ist und alle Tests bestehen.

Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.