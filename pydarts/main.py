from pydarts.session import Session


def main():
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

    s = Session(names, start_value, True)
    s.run()
