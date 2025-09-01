# Migrations

Utilisez le script d'init DB fourni (`app.py --init-db`).  
Pour toute évolution du schéma, adaptez `models.py` et réexécutez l'init (en production, utiliser Flask-Migrate ou backup puis apply).