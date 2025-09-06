# Form Management System

A comprehensive form management system with multi-tenant support, role-based access control, and integrated messaging.

## Features

- Multi-tenant architecture with subdomain support
- Role-based access control (Super Admin, Site Admin, User)
- Dynamic form creation and management
- File upload capabilities
- Integrated messaging system
- PDF generation for form responses
- Automated user cleanup after 1 year of inactivity
- Ticket management system

## Technology Stack

- Backend: FastAPI + PostgreSQL + SQLAlchemy
- Frontend: React + TailwindCSS
- Authentication: JWT
- File Storage: Local filesystem
- Documentation: Swagger/OpenAPI

## Installation

1. Clone the repository
2. Install dependencies:
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize the database:
```bash
python createdb.py
cd backend
alembic upgrade head
```

## Running the Application

Use the unified startup script:

```bash
python run.py
```

This will start both the backend and frontend servers.

## User Roles

### Super Admin
- Create and manage sites
- Access all sites' data
- Manage users across all sites
- Full access to all features

### Site Admin
- Manage forms for their site
- Access site-specific data
- Manage users within their site
- Create and manage tickets for their site

### User
- Submit form responses
- View their submissions
- Send/receive messages
- Create and view tickets

## Ticket System

The ticket system allows users to report issues, request features, or seek support.

### Features
- Create, view, update, and comment on tickets
- Priority levels (Low, Medium, High)
- Status tracking (Open, In Progress, Resolved)
- Site-specific ticket management
- Comment system for ticket discussions

### Usage

#### Creating a Ticket
1. Navigate to the Tickets page
2. Click "Create New Ticket"
3. Fill in:
   - Title
   - Description
   - Priority level
4. Submit the ticket

#### Managing Tickets
1. View ticket list filtered by site
2. Update ticket status
3. Add comments for discussion
4. Track ticket progress

#### Access Control
- Super Admins can access tickets across all sites
- Site Admins can manage tickets for their site
- Users can create and view tickets for their site

### API Endpoints

#### Tickets
- `GET /tickets/` - List tickets (filtered by user's site)
- `POST /tickets/` - Create a new ticket
- `GET /tickets/{ticket_id}` - Get ticket details
- `PUT /tickets/{ticket_id}` - Update ticket status/priority
- `DELETE /tickets/{ticket_id}` - Delete a ticket (admin only)

#### Comments
- `POST /tickets/{ticket_id}/comments` - Add a comment
- `GET /tickets/{ticket_id}/comments` - List ticket comments

## Security

- JWT-based authentication
- Role-based access control
- Input validation
- SQL injection protection
- XSS prevention
- CORS configuration
- Rate limiting
- Secure file uploads

## Maintenance

### User Cleanup
Inactive users (no login for 1 year) are automatically removed:
```bash
python -m backend.app.database.cleanup
```

### Database Migrations
```bash
cd backend
alembic upgrade head
```

## License

MIT License

---

# Système de Gestion de Formulaires

Un système complet de gestion de formulaires avec support multi-locataires, contrôle d'accès basé sur les rôles et messagerie intégrée.

## Fonctionnalités

- Architecture multi-locataires avec support des sous-domaines
- Contrôle d'accès basé sur les rôles (Super Admin, Admin Site, Utilisateur)
- Création et gestion de formulaires dynamiques
- Capacités de téléchargement de fichiers
- Système de messagerie intégré
- Génération de PDF pour les réponses aux formulaires
- Nettoyage automatique des utilisateurs après 1 an d'inactivité
- Système de gestion des tickets

## Stack Technologique

- Backend : FastAPI + PostgreSQL + SQLAlchemy
- Frontend : React + TailwindCSS
- Authentification : JWT
- Stockage de fichiers : Système de fichiers local
- Documentation : Swagger/OpenAPI

## Installation

1. Cloner le dépôt
2. Installer les dépendances :
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

3. Configurer les variables d'environnement :
```bash
cp .env.example .env
# Éditer .env avec votre configuration
```

4. Initialiser la base de données :
```bash
python createdb.py
cd backend
alembic upgrade head
```

## Lancement de l'Application

Utilisez le script de démarrage unifié :

```bash
python run.py
```

Cela démarrera les serveurs backend et frontend.

## Rôles Utilisateur

### Super Admin
- Créer et gérer les sites
- Accéder aux données de tous les sites
- Gérer les utilisateurs sur tous les sites
- Accès complet à toutes les fonctionnalités

### Admin Site
- Gérer les formulaires pour leur site
- Accéder aux données spécifiques au site
- Gérer les utilisateurs de leur site
- Créer et gérer les tickets pour leur site

### Utilisateur
- Soumettre des réponses aux formulaires
- Voir leurs soumissions
- Envoyer/recevoir des messages
- Créer et voir les tickets

## Système de Tickets

Le système de tickets permet aux utilisateurs de signaler des problèmes, demander des fonctionnalités ou obtenir de l'aide.

### Fonctionnalités
- Créer, voir, mettre à jour et commenter les tickets
- Niveaux de priorité (Bas, Moyen, Haut)
- Suivi du statut (Ouvert, En Cours, Résolu)
- Gestion des tickets spécifique au site
- Système de commentaires pour les discussions

### Utilisation

#### Création d'un Ticket
1. Naviguer vers la page Tickets
2. Cliquer sur "Créer un Nouveau Ticket"
3. Remplir :
   - Titre
   - Description
   - Niveau de priorité
4. Soumettre le ticket

#### Gestion des Tickets
1. Voir la liste des tickets filtrée par site
2. Mettre à jour le statut du ticket
3. Ajouter des commentaires pour la discussion
4. Suivre la progression du ticket

#### Contrôle d'Accès
- Les Super Admins peuvent accéder aux tickets de tous les sites
- Les Admins Site peuvent gérer les tickets de leur site
- Les Utilisateurs peuvent créer et voir les tickets de leur site

### Points de Terminaison API

#### Tickets
- `GET /tickets/` - Lister les tickets (filtrés par site de l'utilisateur)
- `POST /tickets/` - Créer un nouveau ticket
- `GET /tickets/{ticket_id}` - Obtenir les détails du ticket
- `PUT /tickets/{ticket_id}` - Mettre à jour le statut/priorité du ticket
- `DELETE /tickets/{ticket_id}` - Supprimer un ticket (admin uniquement)

#### Commentaires
- `POST /tickets/{ticket_id}/comments` - Ajouter un commentaire
- `GET /tickets/{ticket_id}/comments` - Lister les commentaires du ticket

## Sécurité

- Authentification basée sur JWT
- Contrôle d'accès basé sur les rôles
- Validation des entrées
- Protection contre l'injection SQL
- Prévention XSS
- Configuration CORS
- Limitation de débit
- Téléchargements de fichiers sécurisés

## Maintenance

### Nettoyage des Utilisateurs
Les utilisateurs inactifs (pas de connexion pendant 1 an) sont automatiquement supprimés :
```bash
python -m backend.app.database.cleanup
```

### Migrations de Base de Données
```bash
cd backend
alembic upgrade head
```

## Licence

Licence MIT
