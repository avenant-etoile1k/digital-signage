# Digital Signage Local – Agence Immobilière (Raspberry Pi 4)

**Solution complète d’affichage dynamique 100% locale, sans cloud, pour Raspberry Pi 4.**  
Inspirée de Screenly, elle permet l’affichage d’images, vidéos, audio, et pages web, avec interface de gestion web locale.

---

## Sommaire

- [Fonctionnalités](#fonctionnalités)
- [Prérequis Matériel & OS](#prérequis-matériel--os)
- [Installation (copier-coller)](#installation-copier-coller)
- [Démarrage et accès](#démarrage-et-accès)
- [Utilisation](#utilisation)
- [Configuration](#configuration)
- [Dépannage](#dépannage)
- [Limites connues & Arbitrages techniques](#limites-connues--arbitrages-techniques)

---

## Fonctionnalités

- Affichage plein écran d’images, vidéos, audio, pages web (1080p/4K, portrait/paysage)
- Interface d’administration web locale
- Authentification sécurisée (mot de passe hashé)
- Playlists, planification horaires/jours/slots
- Upload médias drag & drop, transcodage vidéo optionnel
- Contrôle du player en temps réel (WebSocket)
- Démarrage automatique au boot (systemd)
- Logs détaillés & monitoring matériel
- Fonctionne entièrement hors-ligne (LAN/localhost)
- Fallback écran d’attente avec IP locale
- “Watch-folder” d’import automatique
- Accessibilité (contraste), internationalisation FR

---

## Prérequis Matériel & OS

- **Raspberry Pi 4** (2Go+ recommandé)
- **Raspberry Pi OS Bookworm 64-bit** (clean install)
- Affichage HDMI (1080p ou 4K)
- Accès SSH ou clavier/souris pour installation initiale

---

## Installation (copier-coller)

> **À exécuter sur le Raspberry Pi, connecté à Internet pour l’installation initiale**

```sh
# 1. Cloner le dépôt
git clone https://github.com/avenant-etoile1k/digital-signage.git
cd digital-signage/signage

# 2. Lancer le script d’installation (en sudo)
sudo bash scripts/install.sh

# 3. (optionnel) Redémarrer pour prise en compte complète
sudo reboot
```

---

## Démarrage et accès

- **Les deux services se lancent automatiquement** :
  - `signage-backend` : API/UI web sur http://raspberrypi:8080
  - `signage-player` : player plein écran sur l’afficheur principal

- **Connexion à l’interface web** :  
  Depuis un navigateur sur le même réseau :  
  `http://<IP-RaspberryPi>:8080`  
  _Identifiants par défaut :_  
  - **Utilisateur** : `admin`
  - **Mot de passe** : `change_me`

---

## Utilisation

1. **Uploader des médias** (images/vidéos/audio/web)
2. **Créer playlist** > ajouter des items > configurer durée/volume
3. **Planifier** via “Créneaux” (jours, plages horaires, priorités)
4. **Le player bascule automatiquement** sur la nouvelle playlist active
5. **Changer orientation/résolution** dans “Réglages” (appliqué au prochain slot)

---

## Configuration

- **Fichier :** `config/config.yaml`
  - Orientation (`portrait`/`paysage`)
  - Volume global
  - Timeout web
  - Chemin médias, logs, quota disque, etc.
- **Page “Réglages”** dans l’UI web : modifie dynamiquement certains paramètres

---

## Dépannage

- **Logs système** :  
  `sudo journalctl -u signage-backend -u signage-player`
- **Logs applicatifs** :  
  Voir page “Logs & Santé” dans l’UI
- **Température/CPU/disque** :  
  Affichés en temps réel dans l’UI (“Logs & Santé”)
- **Écran noir avec IP** :  
  Aucune playlist active ou erreur de lecture – vérifier la planification et les médias.

---

## Limites connues & Arbitrages techniques

- **Pas de Docker** : stabilité/compatibilité sur Pi OS.
- **mpv utilisé pour toute lecture multimédia** (images, vidéos, audio) avec accélération matérielle (`--hwdec=auto`).  
  _Arbitrage :_ mpv est plus stable et maintenu sur Pi OS Bookworm que omxplayer ou autres alternatives.
- **Chromium kiosk** utilisé pour l’affichage web (mode kiosque, kill propre après chaque slot).
- **Pas de dépendances cloud/CDN** : toutes les librairies (ex Tailwind) sont locales.
- **Transcodage vidéo** : optionnel, géré en tâche de fond (ffmpeg).
- **Sécurité** :
  - Auth admin obligatoire, CSRF, upload médias filtré (whitelist, scan minimal, pas d’exécutables)
  - Interface web accessible uniquement depuis le LAN (0.0.0.0:8080)
- **Offline-first** : tout fonctionne sans Internet, sauf URLs web externes, qui sont gérées avec timeout et fallback.
- **Internationalisation** : FR par défaut, structure prête pour d’autres langues.

---

## Structure du projet

```
signage/
  backend/         # API Flask/FastAPI, UI admin, WebSocket, jobs
  player/          # Player Python (mpv, Chromium kiosk)
  config/          # Config YAML par défaut
  scripts/         # install.sh, helpers
  systemd/         # Fichiers de services systemd
  migrations/      # Init DB
  tests/           # Tests unitaires logique
  README.md
  requirements.txt
```

---

## Remerciements

Inspiré par Screenly et la communauté open source Raspberry Pi.

---