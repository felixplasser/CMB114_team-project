# code written by Yoyo
import os
import json
import random
import csv
import time
from converter_engine import to_joules, from_joules # call functions from converter_engine

# Physical constants from converter_engine
H = 6.62607015e-34   # Planck constant (J·s)
C = 2.99792458e8     # Speed of light (m/s)
KB = 1.380649e-23    # Boltzmann constant (J/K)
E  = 1.602176634e-19 # Elementary charge (C)
NA = 6.02214076e23   # Avogadro's number (mol⁻¹)

# Conversion factors to Joules from converter_engine
TO_JOULES = {
    "J":        1.0,
    "kJ":       1e3,
    "eV":       E,
    "cal":      4.184,
    "kcal":     4184.0,
    "kJ/mol":   1e3 / NA,
    "kcal/mol": 4184.0 / NA,
    "cm-1":     H * C * 100,   # E = h*c*wavenumber (in m⁻¹)
    "Hz":       H,             # E = h*freq
    "nm":       None,          # E = h*c/wavelength (handled below)
    "K":        KB,            # E = kB * T
    "Eh":       27.2113862 * E # 1 Hartree = 27.211 eV
}


# open and load the question for beginner and intermediate level stored in JSON file
def load_question():
    with open("question_bank.json","r") as data: 
        question_bank=json.load(data)
        return question_bank

class quiz_class:
    def beginner():
        """
        Quiz at beginner level
        """
        print("Difficulty choosen: Beginner")
        bank = load_question()
        level_questions = bank["beginner"]
        selected = random.sample(level_questions, 3) # randomly pick 3 questions from the bank
        time_start = time.time() # count the time
        score=0
        wrong_questions =[]

        for i,q in enumerate(selected, start=1):
            elapsed = time.time() - time_start # time passed
            print(f"\nTime elapsed: {elapsed:.1f} seconds")

            print(f"Question {i}: {q['question']}")
            for option in q["options"]:
                print(option)
            
            while True:
                user_answer = input("\nAnswer (e.g. A):" ).lower().strip()
                if len(user_answer) == 1 and user_answer in "abcd": # control the user can only enter one character
                    break
                else:
                    print("Please enter a valid option (A/B/C/D)")        

            if user_answer == q["answer"].lower():
                print("Correct!")
                score +=1 
                print(f"Explanation: ",q['explanation'])
            else:
                print("Incorrect!")
                print("You can try again later.")
        
            if i != 3:
                input("\nPress Enter to proceed to the next question...")
                wrong_questions.append(q)
            
        # skip showing in the last question
        print(f"\nFinal Score: {score}/3")
        time_end = time.time() # stop counting time
        time_taken = round(time_end - time_start, 2) # get the time taken to complete the quiz
        print(f"\nYou took {time_taken} seconds to complete.")
        print("Summary of the quiz stored. Please check in the same directory and open with notepad.\n")
        return score, time_taken

    # quiz at intermediate level
    def intermediate():
        print("Difficulty choosen: Intermediate")
        bank = load_question()
        level_questions = bank["intermediate"]
        selected = random.sample(level_questions, 3)
        score = 0
        wrong_questions = []
        time_start=time.time()
        for i,q in enumerate(selected, start=1):
            elapsed = time.time() - time_start 
            print(f"\nTime elapsed: {elapsed:.1f} seconds")
            print(f"Question {i}: {q['question']}")
                    
            while True:
                user_answer = input("\nAnswer:" ).lower().strip()
                if user_answer:
                    break
                else:
                    print("Please enter an answer in character.")

            if user_answer == q['answer'].lower():
                print("Correct!")
                score +=1
                print(f"Explanation: ",q['explanation'])
            else:
                print("Incorrect!")
                wrong_questions.append(q)
                print("You can try again later.")
            
            if i != 3:
                input("\nPress Enter to proceed to the next question...")

        print(f"\nFinal Score: {score}/3")
        time_end = time.time()
        time_taken = round(time_end - time_start, 2)
        print(f"\nYou took {time_taken} seconds to complete.")
        print("Summary of the quiz stored. Please check in the same directory and open with notepad.\n")
        return score, time_taken

    # quiz at advanced level
    def advanced():
        # storing the variable in a dictionary
        {
        "value": value,
        "unit_from": unit_from,
        "unit_to": unit_to,
        "correct": correct
        }

        score = 0
        wrong_questions = []
        time_start=time.time()
        units = list(TO_JOULES.keys()) # get units from TO_JOULES

        # generate 3 questions for unit conversion with for loop
        for i in range (1,4):
            unit_from = random.choice(units)
            unit_to = random.choice([x for x in units if x != unit_from]) # avoide choosing the same unit to convert in the question
            if unit_from == "nm":
                value = round(random.uniform(200, 800), 3) # set ranges for getting random number for nm (thats the usual wavelength range)

            elif unit_from == "Hz":
                value = round(random.uniform(1e12, 1e15), 3)

            else:
                value = round(random.uniform(1, 100), 3)
            # convert the value in question to get the correct answer, convert it to joule first, then to the target unit
            # call the function from converter_engine
            joules = to_joules(value, unit_from)
            correct = from_joules(joules, unit_to)

            elapsed = time.time() - time_start 
            print(f"\nTime elapsed: {elapsed:.1f} seconds")
            print(f"\nQuestion {i}")
            print(f"Convert {value} {unit_from} to {unit_to} (enter the power to e, e.g.1.23e-19, and correct the answer to 3 decimal places)")
            while True:
                user_input = input(f"Answer in {unit_to}: ")

                try:
                    user_answer = float(user_input)
                    break
                except ValueError:
                    print("Please enter a valid number (e.g. 1.23e-19)")

            # allow error
            if correct != 0 and abs(user_answer - correct) / correct < 0.01:
                print("Correct!")
                score += 1
            else:
                print("Incorrect!")
                wrong_questions.append({
                "value": value,
                "unit_from": unit_from,
                "unit_to": unit_to,
                "correct": correct 
                })
                print("You can try again later.")

            if i != 3:
                input("\nPress Enter to proceed to the next question...")

        print(f"\nFinal Score: {score}/3")
        time_end = time.time()
        time_taken = round(time_end - time_start, 2)
        print(f"\nYou took {time_taken} seconds to complete.")
        print("Summary of the quiz stored. Please check in the same directory and open with notepad.\n")
        return score, time_taken

def retry_beginner(wrong_questions):
    for i, q in enumerate(wrong_questions, start=1):
        while True:
            print(f"\nQ{i}: {q['question']}")
            for option in q["options"]:
                print(option)
            while True:
                user_answer = input("\nAnswer (e.g. A):" ).lower().strip()
                if len(user_answer) == 1 and user_answer in "abcd": # control the user can only enter one character
                    break
                else:
                    print("Please enter a valid option (A/B/C/D)")  
            if user_answer == q["answer"].lower():
                print("Correct!")
                print(q["explanation"])
                break
            else:
                print("Try again.")

# print a summary of the quiz
def summary(username, difficulty, score, time_taken):
    file_exists = os.path.isfile("score.csv")
    with open("score.csv", "a",newline = "") as csv_file:
        writer=csv.writer(csv_file)

        if not file_exists: # only write the row's titles if they are not exist in the file
            writer.writerow(["Username", "Difficulty", "Score /3", "Percentage", "Time taken"])
        writer.writerow([username, difficulty, score, f"{(score/3)*100}%", f"{time_taken} s"])

# function for leaderboard
def leaderboard():
    results=[]
    with open("score.csv", "r") as f:
        reader = csv.reader(f)
        next(reader) # skip header row
        for row in reader:
            if len(row) < 4:
                continue

            name = row[0]
            difficulty = row[1]
            score = int(row[2])
            percent = float(row[3].replace("%", "")) # compare using float
            time_taken = float(row[4].replace("s", ""))
            results.append((name, difficulty, score, percent))
    results.sort(key=lambda x: x[2], reverse=True)
    print("\nLEADERBOARD ")
    print("-" * 10)
    print("Ranking | Username | Difficulty | Score /3 | Percentage (%) | Time taken (s)")

    for i, r in enumerate(results[:10], start=1):
        name, diff, score, percent = r
        print(f"{i}. {name} | {diff} | {score}/3 | {percent}% | {time_taken}")

# funtion to run the quiz
def run_quiz():
    print("\n--- UNIT CONVERSION QUIZ ---")
    # enter name before choosing the difficulty
    while True:
        username = input("Enter your username: ").strip()
        if len(username) >= 3:
            username = username.capitalize()
            break
        else:
            print("Username should be at least 3 characters.")

    while True:
        print("Choose a difficulty for the quiz")
        print("\n 1. Beginner")
        print(" 2. Intermediate")
        print(" 3. Advanced")
        print(" 4. Leaderboard")
        print(" q. Quit")

        # user can choose the difficulty or to quit the quiz
        choice = input("\n  Select: ").strip().lower()

        qc = quiz_class()

        if choice == "1":
            score, time_taken = qc.beginner()
            summary(username, "Beginner", score, time_taken)

        elif choice == "2":
            score, time_taken = qc.intermediate()
            summary(username, "Intermediate", score, time_taken)

        elif choice == "3":
            score, time_taken = qc.advanced()
            summary(username, "Advanced", score, time_taken)

        elif choice == "4":
            leaderboard()

        elif choice == "q":
            print("\n  Goodbye!\n")
            print("\n========================================")
            print("      ENERGY UNIT CONVERTER v1.0")
            print("========================================")
            return
        else:
            print("  Invalid option.")
    
    run_quiz()