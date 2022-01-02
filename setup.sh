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
if ! wget https://github.com/bloc97/Anime4K/releases/download/v4.0.1/Anime4K_v4.0.zip; then
  echo "Failed to download Anime4K_v4.0.zip from https://github.com/bloc97/Anime4K/releases/download/v4.0.1/Anime4K_v4.0.zip"
  exit
fi
echo ""
echo ================================
echo ""

echo "Unzipping..."
if ! unzip Anime4K_v4.0.zip -d shaders/; then
  echo "Failed to unzip Anime4K_v4.0.zip"
  rm -rf Anime4K_v4.0.zip
  exit
fi

rm -rf Anime4K_v4.0.zip
echo ""
echo ================================
echo ""
echo "Done!"
