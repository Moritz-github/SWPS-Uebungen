import pickle
import api_service


def rock_paper_scissors_lizard_spock(ch1, ch2):
    if ch1 is ch2:
        return Winner.draw

    # Scissors wins
    if ch1 is Choice.scissors and ch2 is Choice.paper:
        return Winner.player_1
    if ch1 is Choice.scissors and ch2 is Choice.lizard:
        return  Winner.player_1

    # Paper wins
    if ch1 is Choice.paper and ch2 is Choice.spock:
        return Winner.player_1
    if ch1 is Choice.paper and ch2 is Choice.rock:
        return Winner.player_1

    # Rock wins
    if ch1 is Choice.rock and ch2 is Choice.scissors:
        return Winner.player_1
    if ch1 is Choice.rock and ch2 is Choice.lizard:
        return Winner.player_1

    # Lizard wins
    if ch1 is Choice.lizard and ch2 is Choice.spock:
        return Winner.player_1
    if ch2 is Choice.lizard and ch2 is Choice.paper:
        return Winner.player_1

    #Spock wins
    if ch1 is Choice.spock and ch2 is Choice.scissors:
        return Winner.player_1
    if ch1 is Choice.spock and ch2 is Choice.rock:
        return Winner.player_1

    return Winner.player_2


class Choice:
    rock = 0
    paper = 1
    scissors = 2
    lizard = 3
    spock = 4

class Winner:
    draw = 0
    player_1 = 1
    player_2 = 2


def print_choices():
    print("""rock = 0, paper = 1, scissors = 2, lizard = 3, spock = 4""")


def get_input(player_num):
    while True:
        print_choices()
        user_input = input("Playe " + str(player_num) + " choice: ")
        if not user_input.isdecimal():
            print("Numbers only")
            continue
        if int(user_input) < 0 or int(user_input) > 4:
            print("Invalid input (0 - 4 only)")
            continue
        return int(user_input)


def note_wins(winner_choice):
    try:
        # read existing wins
        file = open("wins.pkl", "rb")
        wins_dir = pickle.load(file)
        file.close()
        # add win to dict
        wins_dir[winner_choice] = wins_dir[winner_choice] + 1
        # save new wins
        with open("wins.pkl", "wb") as file:
            pickle.dump(wins_dir, file)

        # send wins to api server
        api_service.sendRequest("mo", wins_dir[2], wins_dir[0], wins_dir[1], wins_dir[4], wins_dir[3])

    except (FileNotFoundError) as e: # file doesn't exist
        with open("wins.pkl", "wb") as file:
            pickle.dump([0 for x in range(0,5)], file)


if __name__ == "__main__":
    while True:
        choice1 = get_input(1)
        print()
        choice2 = get_input(2)
        winner = rock_paper_scissors_lizard_spock(choice1, choice2)
        if winner is Winner.draw:
            print("Game ended in a draw")
        else:
            print("Player 1 won the game" if winner is Winner.player_1 else "Player 2 won the game")
        print("\n")

        note_wins(choice1 if winner is Winner.player_1 else choice2)
