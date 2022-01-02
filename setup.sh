#!/bin/bash
echo Installing necessary python libraries
pip3 install -r requirements.txt

echo Installing optional progress bar...
if ! npm install --global ffmpeg-progressbar-cli; then
  echo "Failed to install optional progress bar."
fi

echo "Downloading shaders..."
if ! mkdir shaders && cd shaders; then
  echo "Failed to create shaders directory."
  exit
fi
if ! wget https://github.com/bloc97/Anime4K/releases/download/v4.0.1/Anime4K_v4.0.zip; then
  echo "Failed to download Anime4K_v4.0.zip from https://github.com/bloc97/Anime4K/releases/download/v4.0.1/Anime4K_v4.0.zip"
  exit
fi

echo "Unzipping..."
if ! unzip Anime4K_v4.0.zip; then
  echo "Failed to unzip."
  exit
fi

rm -rf Anime4K_v4.0.zip
echo "Done!"
