# Mufi 🐜

**Mufi** is a command-line music finder written in Python with a bit of Javascript and based on Selenium. It is capable of finding albums of various styles, genres, moods (even random, using command-line args). Basically, it uses Allmusic and Last.fm to get brief music information.

**Mufi** comes with two command-line tools:

1. `mufi`: finding albums by style, genre, date, mood.
2. `mufi-recs`: getting personal recommendations from Last.fm.

## Usage

### mufi

```bash
$ mufi -h
usage: mufi [-h] [-a ARTIST] [-d DATE] [-g GENRE] [-m MOODS]
            [-n ALBUMS_NUMBER] [-r RATING]
            [-t {album,studio,live,single,remix,va,all}] [-s STYLE] [-v]
            [-o {album,year,rating}] [-x {0,1,2}] [--and] [--asc]
            [-k SAMPLE_NUM] [--random-album] [--random-style]
            [--random-genre]

Mufi finds albums by style, genre, date, or mood 🐜

optional arguments:
  -h, --help            show this help message and exit
  -a ARTIST             artist
  -d DATE               date interval, e.g. 2010-2019
  -g GENRE              genres, e.g. rock electronic
  -m MOODS              moods, e.g. sad
  -n ALBUMS_NUMBER      number of albums to get (default: 1)
  -r RATING             rating interval (1-5), e.g. "3.5 5"
  -t {album,studio,live,single,remix,va,all}
                        recording type
  -s STYLE              styles, e.g. "blues rock,indie"
  -v                    verbose

sorting/matching arguments:
  -o {album,year,rating}
                        sorting criteria
  -x {0,1,2}            strictness level for style/genre matching
  --and                 use AND logic (default: OR)
  --asc                 ascending sort

randomizer arguments:
  -k SAMPLE_NUM         number of random styles/genres to get
  --random-album        get random album
  --random-style        get random style
  --random-genre        get random genre
```

### mufi-recs

```bash
$ mufi-recs -h
usage: mufi-recs [-h] [-a] [-l] [-n NUMBER] [-o ORDERBY] [-s] [-v]

Mufi fetches your recommendations from last.fm 🐜

optional arguments:
  -h, --help  show this help message and exit
  -a          recommended artists (default)
  -l          recommended albums
  -n NUMBER   results number
  -o ORDERBY  sort by: none, random (default), name, listeners
  -s          show similar/context
  -v          verbose
```

## Examples

```bash
$ mufi 
```