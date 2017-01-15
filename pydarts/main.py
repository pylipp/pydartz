import os.path
import argparse

from tinydb import where
import simpleaudio

from .session import Session
from .database import Stats


def main():
    args = vars(_parse_command())
    player_name = args.pop("stats", None)
    if player_name is not None:
        stats = Stats()
        player = stats.table("players").get(where("name") == player_name)
        if player is not None:
            print(player)
        import sys; sys.exit(0)
    s = _setup_session()
    s.run()

    _play_ending_song()

def _parse_command():
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--stats", metavar="NAME",
            help="display player stats")

    return parser.parse_args()

def _setup_session():
    print(r"      ___                                   ___           ___                         ___     ")
    print(r"     /\  \                   _____         /\  \         /\  \                       /\__\    ")
    print(r"    /::\  \       ___       /::\  \       /::\  \       /::\  \         ___         /:/ _/_   ")
    print(r"   /:/\:\__\     /|  |     /:/\:\  \     /:/\:\  \     /:/\:\__\       /\__\       /:/ /\  \  ")
    print(r"  /:/ /:/  /    |:|  |    /:/  \:\__\   /:/ /::\  \   /:/ /:/  /      /:/  /      /:/ /::\  \ ")
    print(r" /:/_/:/  /     |:|  |   /:/__/ \:|__| /:/_/:/\:\__\ /:/_/:/__/___   /:/__/      /:/_/:/\:\__\ ")
    print(r" \:\/:/  /    __|:|__|   \:\  \ /:/  / \:\/:/  \/__/ \:\/:::::/  /  /::\  \      \:\/:/ /:/  /")
    print(r"  \::/__/    /::::\  \    \:\  /:/  /   \::/__/       \::/~~/~~~~  /:/\:\  \      \::/ /:/  / ")
    print(r"   \:\  \    ~~~~\:\  \    \:\/:/  /     \:\  \        \:\~~\      \/__\:\  \      \/_/:/  /  ")
    print(r"    \:\__\        \:\__\    \::/  /       \:\__\        \:\__\          \:\__\       /:/  /   ")
    print(r"     \/__/         \/__/     \/__/         \/__/         \/__/           \/__/       \/__/    ")
    print()

    while True:
        try:
            nr_players = int(input("Nr of players: "))
            if nr_players >= 1:
                break
        except (ValueError):
            print("Invalid input.")

    names = []
    for i in range(nr_players):
        name = input("Name of player {}: ".format(i+1))
        names.append(name)

    while True:
        try:
            start_value = int(input("Start value: "))
            if start_value >= 2:
                break
        except (ValueError):
            print("Invalid input.")

    return Session(names, start_value, True)

def _play_ending_song():
    dirname = os.path.dirname(os.path.abspath(__file__))
    wave_obj = simpleaudio.WaveObject.from_wave_file(
            os.path.join(dirname, "..", "data", "chase_the_sun.wav"))
    play_obj = wave_obj.play()
    play_obj.wait_done()
