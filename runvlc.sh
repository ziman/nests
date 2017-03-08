#!/usr/bin/env bash

echo "Generating playlist (this should take about 10 seconds)..."
python3 mkpls.py > nests.m3u

echo "Playing the playlist in VLC..."
exec vlc --no-playlist-autostart --playlist-tree nests.m3u
