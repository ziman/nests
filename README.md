# nests

A small commandline wrapper to create M3U playlists of bird nest streams

## Data sources

* Peregrine falcons on the ABN AMRO building in Amsterdam
* https://www.vogelbescherming.nl/beleefdelente

## Usage

```{bash}
# install bs4 and requests if you don't have them yet
pip3 install --user bs4 requests

# generate playlist and run VLC
./runvlc.sh
```

## Explicit playlist generation

```{bash}
python3 mkpls.py > playlist.m3u
```
