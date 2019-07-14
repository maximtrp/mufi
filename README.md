# Mufi 🐜

**Mufi** is a command-line **mu**sic **fi**nder written in Python with a bit of Javascript. It is capable of finding albums of various styles, genres, moods (even random, using command-line args). Basically, it uses Allmusic and Last.fm to get brief music information.

**Mufi** comes with two command-line tools:

1. `mufi`: finding albums by style, genre, date, mood.
2. `mufi-recs`: getting personal recommendations from Last.fm.

## Dependencies

Mufi depends heavily on [Selenium](https://pypi.org/project/selenium/) and Chrome WebDriver. I will add support for Firefox WebDriver soon.

## Installation

```bash
$ pip install mufi
```

Or you can install from this git repo:

```bash
$ pip install git+https://github.com/maximtrp/mufi
```

To use `mufi-recs` command, you need to provide your Last.fm login data. Mufi reads it from `~/.lastfm` and `~/.config/mufi/.lastfm` files. Just say:

```bash
$ echo login password > ~/.lastfm
```

## Usage

### mufi

```bash
$ mufi -h
usage: mufi [-h] [-d DATE] [-g GENRE] [-m MOODS] [-n ALBUMS_NUM] [-r RATING]
            [-s STYLE] [-v] [-o {album,year,rating}] [-x] [--and] [--asc]
            [-k SAMPLE_NUM] [--random-album] [--random-style] [--random-genre]

Mufi finds albums by style, genre, date, or mood 🐜

optional arguments:
  -h, --help            show this help message and exit
  -d DATE               date interval, e.g. 2010-2019
  -g GENRE              genres, e.g. rock electronic
  -m MOODS              moods, e.g. sad
  -n ALBUMS_NUM         number of albums to get (default: 1)
  -r RATING             rating interval (1-5), e.g. "3.5 5"
  -s STYLE              styles, e.g. "blues rock,indie"
  -v                    verbose

sorting/matching arguments:
  -o {album,year,rating}
                        sorting criteria
  -x                    strict style/genre matching
  --and                 AND logic (default is OR logic)
  --asc                 ascending sort

randomizer arguments:
  -k SAMPLE_NUM         number of random styles/genres to get (default: 1)
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

### Defaults

If executed without arguments, *mufi* selects a random style and fetches just one album from Allmusic.

```bash
$ mufi
Dierks Bentley - Up on the Ridge (2010) ⋆⋆⋆⋆
```

### Selecting 3 random styles and 5 random albums

```bash
$ mufi --random-style -k 3 -n 5
Bruce Springsteen - Nebraska (1982) ⋆⋆⋆⋆⋆
Billy Bragg - Life's a Riot with Spy vs Spy (1983) ⋆⋆⋆⋆
Bruce Springsteen - The Ghost of Tom Joad (1995) ⋆⋆⋆
Lucinda Williams - Lucinda Williams (1988) ⋆⋆⋆⋆
The Avett Brothers - Magpie and the Dandelion (2013) ⋆⋆⋆
```

It will not output the names of styles that were selected randomly. To get all this info, you need to use `-vv` flag. See below.

### Verbosity

You can tell mufi to be verbose (albums list will become numbered, and artist names will be in bold style):

```bash
$ mufi -v
[1] Kenny Neal - Hooked On Your Love (2010) ⋆⋆⋆
```

Or even more verbose (mufi will tell you what it is doing):

```bash
$ mufi -vv
Selected styles: Indie Rock

[1] The Smashing Pumpkins - Mellon Collie and the Infinite Sadness (1995) ⋆⋆⋆⋆
```

### Getting random albums of certain styles

```bash
$ mufi -s "blues rock" -n 5 -vv
Selected styles: Blues-Rock

[1] The Jimi Hendrix Experience / Jimi Hendrix - Are You Experienced? (1967) ⋆⋆⋆⋆⋆
[2] The Jimi Hendrix Experience / Jimi Hendrix - Electric Ladyland (1968) ⋆⋆⋆⋆⋆
[3] The Jimi Hendrix Experience / Jimi Hendrix - Axis: Bold as Love (1967) ⋆⋆⋆⋆⋆
[4] Jimi Hendrix / The Jimi Hendrix Experience - Smash Hits (1969) ⋆⋆⋆⋆
[5] Jimi Hendrix - First Rays of the New Rising Sun (1997) ⋆⋆⋆⋆
```

There is a difference between using a space and a comma in a style/genre query string. First, the string is split by non-word and non-whitespace symbols (such as punctuation symbols), and then each of substrings is split by non-word symbols. `Blues rock` will match only blues-rock style, but not all styles containing "rock" and "blues" words. If you want to match all styles with a word "rock", use a comma to separate it from another word: `blues,rock`.

See the following examples. Selecting all styles that contain `afro` substring:

```bash
$ mufi -s "afro" -vv
Selected styles: Afro-Brazilian OR Afro-Peruvian OR Afro-Pop OR Afro-beat OR Afro-Cuban Jazz OR Afro-Colombian OR Afro-Cuban

[1] Vinicius Cantuária / Bill Frisell - Lágrimas Mexicanas (2011) ⋆⋆⋆⋆
```

Selecting just Afro-pop:

```bash
$ mufi -s "afro pop" -vv
Selected styles: Afro-Pop

[1] Fela Kuti - Koola Lobitos/The '69 Los Angeles Sessions (2001) ⋆⋆⋆⋆
```

