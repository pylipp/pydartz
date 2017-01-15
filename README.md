# pydarts

Play with your friends and keep track of your darts scores!

## Features
- arbitray start value (501, 301, whatever positive number you like, ...)
- unlimited number of players
- scores can be passed in sum (i.e. the total visit) or throw by throw
- finish suggestions
- player database to keep track of player performance

## Upcoming
- database evaluation to find player average, highscore, etc.

## TODO
- revisit finish options (e.g. 56, 46)

## Installation

```
git clone https://github.com/pylipp/pydarts
cd pydarts
mkvirtualenv --python=/usr/bin/python3 pydarts
pip install -r requirements.txt -e .
```

## Usage

For playing, simply type `pydarts` (with the virtualenv activated) and following the instructions on screen.

For displaying player statistics, type `pydarts --stats <player_name>`. 

Also, see the output of `pydarts --help`.

Have fun!
