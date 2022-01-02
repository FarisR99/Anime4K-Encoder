#!/bin/bash
echo ================================
echo Setup
echo ================================
echo ""

echo Installing necessary python libraries
pip3 install -r requirements.txt
echo ""
echo ================================
echo ""

echo Installing optional progress bar...
if ! npm install --global ffmpeg-progressbar-cli; then
  echo "Failed to install optional progress bar."
fi
echo ""
echo ================================
echo ""

echo "Downloading shaders..."
if [[ -d shaders/ ]]; then
  echo "Shaders directory already exists!"
  echo ================================
  echo ""
  echo "Done!"
  exit
fi

if ! mkdir shaders; then
  echo "Failed to create shaders directory."
  exit
fi
if ! wget https://github.com/bloc97/Anime4K/releases/download/v4.0.1/Anime4K_v4.0.zip; then
  echo "Failed to download Anime4K_v4.0.zip from https://github.com/bloc97/Anime4K/releases/download/v4.0.1/Anime4K_v4.0.zip"
  exit
fi
if ! mv Anime4K_v4.0.zip shaders/; then
  echo "Failed to move Anime4K_v4.0.zip to shaders directory"
  exit
fi
echo ""
echo ================================
echo ""

echo "Unzipping..."
if ! unzip shaders/Anime4K_v4.0.zip; then
  echo "Failed to unzip."
  exit
fi

rm -rf shaders/Anime4K_v4.0.zip
echo ""
echo ================================
echo ""
echo "Done!"
