#!/usr/bin/env bash

echo -n "Looking for VLC... "

vlc="$(which vlc)"
if ! [ -x "$vlc" ]; then
	# try the usual Mac OS path
	vlc="/Applications/VLC.app/Contents/MacOS/VLC"
fi

if ! [ -x "$vlc" ]; then
	echo "not found"
	exit 1
fi

echo "$vlc"

echo "Generating playlist (this should take about 10 seconds)..."
python3 mkpls.py > nests.m3u

echo "Playing the playlist in VLC..."
exec "$vlc" --no-playlist-autostart nests.m3u
