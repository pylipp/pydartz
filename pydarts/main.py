from pydarts.session import Session


def main():
    nr_players = input("Nr of players: ")
    names = []
    for i in range(int(nr_players)):
        name = input("Name of player {}: ".format(i+1))
        names.append(name)
    start_value = input("Start value: ")

    s = Session(names, int(start_value))
    s.run()
