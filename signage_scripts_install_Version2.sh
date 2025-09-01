#!/bin/bash
set -e

echo "==== Digital Signage – Installation ===="
echo "Mise à jour du système…"
apt update && apt upgrade -y

echo "Installation des dépendances système…"
apt install -y python3 python3-pip python3-venv ffmpeg mpv \
  chromium-browser xorg x11-xserver-utils unclutter \
  fonts-dejavu fonts-liberation alsa-utils libpq-dev

echo "Création de l'utilisateur de service 'signage'…"
id -u signage &>/dev/null || useradd -m -s /bin/bash signage

echo "Création du virtualenv Python…"
sudo -u signage bash -c "python3 -m venv ~/signage-venv"

echo "Installation des dépendances Python…"
sudo -u signage bash -c "~/signage-venv/bin/pip install --upgrade pip"
sudo -u signage bash -c "~/signage-venv/bin/pip install -r $(pwd)/../requirements.txt"

echo "Initialisation de la base de données…"
sudo -u signage bash -c "~/signage-venv/bin/python3 $(pwd)/../backend/app.py --init-db"

echo "Création de l'admin par défaut (admin/change_me)…"
sudo -u signage bash -c "~/signage-venv/bin/python3 $(pwd)/../backend/app.py --create-admin"

echo "Copie des fichiers systemd…"
cp $(pwd)/../systemd/signage-backend.service /etc/systemd/system/
cp $(pwd)/../systemd/signage-player.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable signage-backend.service
systemctl enable signage-player.service

echo "Désactivation du screensaver/DPMS…"
cat <<EOF > /etc/X11/xinit/xinitrc.d/99-noblank.sh
xset s off
xset -dpms
xset s noblank
unclutter &
EOF
chmod +x /etc/X11/xinit/xinitrc.d/99-noblank.sh

echo "Configuration du timezone Europe/Paris (si absent)…"
timedatectl set-timezone Europe/Paris

echo "Installation terminée !"
echo "Accédez à l'interface sur http://<ip-du-pi>:8080/"