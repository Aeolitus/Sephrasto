#!/bin/bash

# install dependencies
echo "Bitte gib dein Adminpasswort ein, um die für Sephrasto erforderlichen Pakete zu installiern:"
echo "sudo apt install python3-pip python3-venv openjdk-11-jdk pdftk libxcb-cursor0"
sudo apt install python3-pip python3-venv openjdk-11-jdk pdftk libxcb-cursor0

# download code from latest sephrasto release
# git clone https://github.com/Aeolitus/Sephrasto.git
echo "Lade Sephrasto (latest release)..."
curl -s https://api.github.com/repos/Aeolitus/Sephrasto/releases/latest \
| grep "tarball_url" \
| cut -d '"' -f 4 \
| xargs curl -L -o sephrasto_latest.tar.gz

# extract sephrasto
echo "Entpacke Sephrasto..."
mkdir -p Sephrasto
tar -xzf sephrasto_latest.tar.gz -C Sephrasto --strip-components=1
rm sephrasto_latest.tar.gz

INSTALL=$(pwd)/Sephrasto

# create and install virtual environment
# mkdir -p "$INSTALL/.venv"
echo "Installiere virtuelle Umgebung..."
python3 -m venv "$INSTALL/.venv"
source "$INSTALL/.venv/bin/activate"
pip install -r $INSTALL/requirements.txt


# Create desktop entry file (starter)
cat <<EOL > Sephrasto.desktop
[Desktop Entry]
Encoding=UTF-8
Name=Sephrasto
Description=Heldengenerator für Ilaris
Comment=Heldengenerator für Ilaris
Exec=$INSTALL/.venv/bin/python $INSTALL/src/Sephrasto/Sephrasto.py
Icon=$INSTALL/src/Sephrasto/icon_large.png
Type=Application
Categories=Games;
EOL

# make desktop entry executable and found by desktop environemnt
chmod +x Sephrasto.desktop
mv Sephrasto.desktop ~/.local/share/applications/