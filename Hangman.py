granted = False
def grant():
    global granted
    granted = True

def login():
    global username
    existingUsers = open("logindetails.txt", "r")
    username = input("Enter username: ")
    instancesOfUsername = 0

    for i in existingUsers:
        a, b = i.split(",")
        b = b.strip()
        if a == username:
            instancesOfUsername += 1
            password = input("Enter password: ")
            if b == password:
                print("Log-in successful!\n")
                grant()
            else:
                print("Password does not match.\n")
                login()

    if instancesOfUsername == 0:
            print("Username doesn't exist. \n")
            login()
    existingUsers.close()

def reg():
    global username
    existingUsers = open("logindetails.txt", "r")
    username = input("Enter username (with no spaces) to use: ")
    instancesOfUsername = 0

    if " " in username or len(username) == 0:
        print("Empty names or names with spaces are not allowed.\n")
        reg()

    else:

        for i in existingUsers:
            a, b = i.split(",")
            if a == username:
                instancesOfUsername += 1
        existingUsers.close()

        if instancesOfUsername == 0:
            existingUsers = open("logindetails.txt", "a")
            password = input("Enter password: ")
            passwordConfirm = input("Enter password again: ")

            if password == passwordConfirm:
                existingUsers.write("\n" + username + ", " + password)
                existingUsers.close()
                print("Registration successful!\n")

                userStats = open("userstats.txt", "a")
                userStats.write(f'\n{username} 0 0')
                userStats.close()

                grant()

            else:
                print("Password confirmation does not match.\n")
                reg()

        else:
            print("Username is already taken!\n")
            reg()

def loginOrReg():
    print("Welcome to Hangman!")
    option = ''
    while option != "A" and option != "B":
        option = input("Select letter of action to execute:\n(A) Log-in\n(B) Register\n").upper()
        if option == "A":
            login()
        elif option == "B":
            reg()
        else:
            print("Invalid input.\n")

from wordlist import word_list
import random

def play(username):
    word = random.choice(word_list)
    lives = 10
    underscores = "_" * len(word)
    attemptedLetters = []
    attemptedWords = []
    wordProgress = list(underscores)
    print(f"Word to guess: {underscores}")

    while lives > 0 and "".join(wordProgress) != word:
        guess = input("Enter letter or word guess: ").lower()

        if len(guess) == 1:
            if guess in word and guess not in attemptedLetters and guess.isalpha():
                for i in word:
                    if guess == i:
                        indicesOfguess = [w for w, e in enumerate(word) if e == i]
                        for r in indicesOfguess:
                            wordProgress[r] = guess
                attemptedLetters.append(guess)
                print(f'Correct guess.\n{"".join(wordProgress)}')
            elif guess in attemptedLetters:
                print("You already attempted that letter.")
            elif guess not in word and guess not in attemptedLetters and guess.isalpha():
                lives -= 1
                attemptedLetters.append(guess)
                print(f'Guessed letter is wrong, {lives} lives left.\n{"".join(wordProgress)}')
            else:
                print("Invalid guess.")

        elif len(guess) > 1:
            if guess != word and guess not in attemptedWords and guess.isalpha():
                lives -= 1
                attemptedWords.append(guess)
                print(f'Guessed word is wrong, {lives} lives left.\n{"".join(wordProgress)}')
            elif guess in attemptedWords:
                print("You already attempted that word.")
            elif guess == word:
                break
            else:
                print("Invalid guess.")

        else:
            print("Enter something.")

    if "".join(wordProgress) == word or guess == word:
        print(f'You got it! The word was indeed "{word}".')

        with open("userstats.txt", "r") as userStats:
            whole = userStats.readlines()

            for i in whole:
                a, b, c = i.split()
                if username == a:
                    Index = whole.index(i)
                    line = whole[Index].split()
                    line = [int(k) if line.index(k) > 0 else k for k in line]
                    line[1] += 1
                    whole[Index] = ''
                    for j in range(len(line)):
                        if j < 2:
                            whole[Index] += str(line[j]) + " "
                        elif j == 2 and Index != (len(whole) - 1):
                            whole[Index] += str(line[j]) + "\n"
                        elif j == 2 and Index == (len(whole) - 1):
                            whole[Index] += str(line[j])

        with open("userstats.txt", "w") as userStats:
            userStats.writelines(whole)

    if lives == 0:
        print(f'You\'re out of lives! The word was "{word}"!')

        with open("userstats.txt", "r") as userStats:
            whole = userStats.readlines()

            for i in whole:
                a, b, c = i.split()
                if username == a:
                    Index = whole.index(i)
                    line = whole[Index].split()
                    line = [int(k) if line.index(k) > 0 else k for k in line]
                    line[2] += 1
                    whole[Index] = ''
                    for j in range(len(line)):
                        if j < 2:
                            whole[Index] += str(line[j]) + " "
                        elif j == 2 and Index != (len(whole) - 1):
                            whole[Index] += str(line[j]) + "\n"
                        elif j == 2 and Index == (len(whole) - 1):
                            whole[Index] += str(line[j])

        with open("userstats.txt", "w") as userStats:
            userStats.writelines(whole)

def main(username):
    playAgain = True
    while playAgain:
        play(username)
        Prompt = ''
        while Prompt != "A" and Prompt != "B" and Prompt != "C":
            Prompt = input("""Select letter of action to execute:\n(A) Play again\n(B) Go to menu
(C) Quit.\n""").upper()
            if Prompt == "A":
                print("☰☰☰☰☰☰☰☰☰☰☰☰")
            elif Prompt == "B":
                playAgain = False
                menu(username)
            elif Prompt == "C":
                playAgain = False
            else:
                print("Invalid input!")

def menu(username):
    choice = input(f"""Welcome to Hangman, {username}! Select letter of action to execute:\n(A) Play
(B) View Player Statistics\n(C) Options\n(D) Exit\n""").upper()
    if choice == "A":
        print("☰☰☰☰☰☰☰☰☰☰☰☰")
        main(username)
    elif choice == "B":
        playerStats(username)
    elif choice == "C":
        options(username)
    elif choice == "D":
        pass
    else:
        print("Invalid input!")
        menu(username)

def playerStats(username):
    with open("userstats.txt", "r") as userStats:
        for i in userStats:
            a, b, c = i.split()
            b = int(b)
            c = int(c)
            if a == username:
                if b + c == 0:
                    winRate = "N/A"
                else:
                    winRate = str(round((b/(b+c)), 4) * 100) + "%"
                print(f"""\nUsername: {a}\nWins: {b}\nLosses: {c}\nWin Rate: {winRate}
Level: {round(b/5)}""")
    choice = ''
    while choice != "B":
        choice = input("Enter B to go back to the menu.\n").upper()
        if choice == "B":
            menu(username)
        else:
            print("Invalid input!\n")

def options(username):
    opt = ""
    while opt != "A" and opt != "B" and opt != "C":
        opt = input("""Select letter of action to execute:\n(A) Log-out\n(B) Show credits
(C) Go back to menu\n""").upper()
        if opt == "A":
            granted = False
            mainFunction()
        elif opt == "B":
            credits(username)
        elif opt == "C":
            menu(username)
        else:
            print("Invalid input!")

def credits(username):
    print("Game Creator: Beam\nDate Finished: August 31, 2021")
    choice = ''
    while choice != "B":
        choice = input("Enter B to go back to Options.\n").upper()
        if choice == "B":
            options(username)
        else:
            print("Invalid input!\n")

def mainFunction():
    loginOrReg()
    if granted:
        menu(username)

mainFunction()
