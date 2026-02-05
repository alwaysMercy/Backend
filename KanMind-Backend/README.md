# 🧠 KanMind – DRF Backend

**KanMind** ist eine Backend-Anwendung auf Basis von **Django REST Framework (DRF)**.  
Sie stellt eine leistungsfähige REST-API für **Task- und Projektmanagement nach dem Kanban-Prinzip** bereit und unterstützt Teams dabei, ihre Arbeitsabläufe effizient zu organisieren.

---

## 🚀 Features

- 🔐 **Benutzerverwaltung**
  - Registrierung & Login
  - Rollenbasierte Zugriffssteuerung

- 📁 **Projektmanagement**
  - Projekte erstellen, bearbeiten und löschen

- ✅ **Aufgabenverwaltung**
  - Aufgaben anlegen, aktualisieren und entfernen
  - Zuordnung zu Projekten

- 🏷️ **Priorisierung & Kategorisierung**
  - Aufgaben nach Dringlichkeit und Kategorie organisieren

- 🔌 **REST API**
  - Ideal für die Anbindung von Frontend-Anwendungen (z. B. React, Angular, Vue)

---

## ⚙️ Installation

### 1️⃣ Repository klonen

```bash
git clone https://github.com/alwaysMercy/Backend/tree/main/KanMind-Backend
cd KanMind-Backend
```

### 2️⃣ Virtuelle Umgebung erstellen & aktivieren

```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3️⃣ Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 4️⃣ Datenbank migrieren

```bash
python manage.py migrate
```

### 5️⃣ Entwicklungsserver starten

```bash
python manage.py runserver
```

Der Server läuft anschließend unter:  
👉 **http://127.0.0.1:8000/**

---

## 📡 API Endpoints

| Endpoint | Beschreibung |
|--------|--------------|
| `/api/auth/register/` | Benutzerregistrierung |
| `/api/auth/login/` | Benutzeranmeldung |
| `/api/projects/` | Projektverwaltung |
| `/api/tasks/` | Aufgabenverwaltung |

📘 **API-Dokumentation**  
Die API kann über **Swagger** oder **Postman** getestet werden.

---

## 🧪 Tests ausführen

```bash
python manage.py test
```

---

## 🤝 Mitwirken

Beiträge sind herzlich willkommen!  
Bitte erstelle einen **Pull Request** und stelle sicher, dass:
- der Code sauber dokumentiert ist
- alle Tests erfolgreich durchlaufen

---

## 📝 Lizenz

Dieses Projekt steht unter der **MIT-Lizenz**.
