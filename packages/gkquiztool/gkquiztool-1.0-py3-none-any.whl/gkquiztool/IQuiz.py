# this is a General Knowledge quiz Game...
# Designed and Created By Ash bhatia...
options = 0
positive_marking = 1
negative_marking = 0.25
total_marks = 0
science_marks = 0
history_marks = 0
geography_marks = 0
general_aware_marks = 0
name = ""
science_started = False
history_started = False
geography_started = False
General_awareness_started = False
print("\033[38m".center(100, "-"))
print("".center(100, "-"))
print("Fill your personal details here".center(100).upper())
name = input("Name :: ".center(10).upper()).upper()
# qualification = input(" Qualification :: ".center(10).upper()).upper()
# roll_no = int(input(" Roll No :: ".center(10).upper()))
# gender = input("Sex :: ".center(10).upper()).upper()
# age = int(input("Age :: ".center(10).upper()))
quiz_option = ["Science", "History", "Geography", "General Awareness", "Exit"]
while True:
    print("\033[38m".center(100, "-"))
    print("".center(100, "-"))
    print("GENERAL KNOWLEDGE QUIZ".center(100).upper())
    print(f"Welcome : \033[31m {name} \033[38m".rjust(100))
    print("""
Press 1 - Science quiz.
Press 2 - History quiz
Press 3 - Social Science quiz
Press 4 - General awareness quiz
Press 5 - Exit\n""".title())
    options = int(input("Enter your option Here : ".upper())).__abs__()
    if options == 1:
        if science_started:
            print("Science Quiz already taken...")
        else:
            science_started = True
            print(
                f"\n\033[34mYou have selected {quiz_option[0].upper()} Quiz.")
            # while science_loop:
            science_answer_list = [
                "Fructose", "Sulphuric Acid", "Platinum", "7.5", "Nitrogen"]
            # Question No. 1
            science_query_first = input("""\033[38m
Q1. Which one is the sweetest sugar ? 
A - Sucrose
B - Maltose
C - Fructose
D - Lactose\n>> """).title()
            if science_query_first == str(science_answer_list[0]):
                print(
                    f"\033[38m {science_query_first} \033[36m is the Correct Answer")
                science_marks += positive_marking
            else:
                print(
                    f"\033[31m {science_query_first} \033[36m is the Wrong Answer")
                science_marks -= negative_marking
            # Question No. 2
            science_query_second = input("""\033[38m
Q2. Which one is the king of all chemical ? 
A - Sulphuric Acid
B - Hydrochloric Acid
C - lactic Acid
D - Nitric Acid\n>> """).title()
            if science_query_second == str(science_answer_list[1]):
                print(
                    f"\033[38m {science_query_second} \033[36m is the Correct Answer")
                science_marks += positive_marking
            else:
                print(
                    f"\033[31m {science_query_second} \033[36m is the Wrong Answer")
                science_marks -= negative_marking
            # Question No. 3
            science_query_third = input("""\033[38m
Q3. Which one is known as 'White Gold' ? 
A - Gold
B - Platinum
C - Silver
D - Bronze\n>> """).title()
            if science_query_third == str(science_answer_list[2]):
                print(
                    f"\033[38m {science_query_third} \033[36m is the Correct Answer")
                science_marks += positive_marking
            else:
                print(
                    f"\033[31m {science_query_third} \033[36m is the Wrong Answer")
                science_marks -= negative_marking
            # Question No. 4
            science_query_fourth = input("""\033[38m
Q4. PH Value of the Blood is ? 
A - 6.0
B - 7.0
C - 7.5
D - 5.5\n>> """).title()
            if science_query_fourth == str(science_answer_list[3]):
                print(
                    f"\033[38m {science_query_fourth} \033[36m is the Correct Answer")
                science_marks += positive_marking
            else:
                print(
                    f"\033[31m {science_query_fourth} \033[36m is the Wrong Answer")
                science_marks -= negative_marking
            # Question No. 5
            science_query_fifth = input("""\033[38m
Q5. Which gas is use as Preservative ? 
A - Methane
B - Butane
C - Oxygen
D - Nitrogen\n>> """).title()
            if science_query_fifth == str(science_answer_list[4]):
                print(
                    f"\033[38m {science_query_fifth} \033[36m is the Correct Answer")
                science_marks += positive_marking
            else:
                print(
                    f"\033[31m {science_query_fifth} \033[36m is the Wrong Answer")
                science_marks -= negative_marking
        print("\n\033[38mDo you want to continue or not!")
        main_quiz_continue = input("Press (Y) - Yes or (N) - No : ").upper()
        if main_quiz_continue == 'Y':
            continue
        elif main_quiz_continue == 'N':
            print(
                f"\n\033[33mTotal Marks in Science is : {science_marks} Marks")
            break
        else:
            print("\033[31mYou have entered wrong input")
    elif options == 2:
        if history_started:
            print("History Quiz already taken...")
        else:
            history_started = True
            print(
                f"\n\033[34mYou have selected {quiz_option[1].upper()} Quiz\033[38m")
            history_answer_list = ["Shahjhan",
                                   "Herodotus", "1757", "Lucknow", "323"]
            # Question No. 1
            history_query_first = input("""
Q1. Who built the Taj Mahal? 
A - Noorjhan
B - Shahjhan
C - Akbar
D - Bhadhur Shah Jaffar\n>> """).title()
            if history_query_first == str(history_answer_list[0]):
                print(
                    f"\033[38m {history_query_first} \033[36m is the Correct Answer")
                history_marks += positive_marking
            else:
                print(
                    f"\033[31m {history_query_first} \033[36m is the Wrong Answer")
                history_marks -= negative_marking
            # Question No. 2
            history_query_second = input("""\033[38m
Q2. Who is the founder of History ? 
A - Aristotle
B - Herodotus
C - Newton
D - Coulombs \n>> """).title()
            if history_query_second == str(history_answer_list[1]):
                print(
                    f"\033[38m {history_query_second} \033[36m is the Correct Answer")
                history_marks += positive_marking
            else:
                print(
                    f"\033[31m {history_query_second} \033[36m is the Wrong Answer")
                history_marks -= negative_marking
            # Question No. 3
            history_query_third = input("""\033[38m
Q3. Battle of Plassey was fought in which year? 
A - 1684
B - 1498
C - 1757
D - 1857\n>> """).title()
            if history_query_third == str(history_answer_list[2]):
                print(
                    f"\033[38m {history_query_third} \033[36m is the Correct Answer")
                history_marks += positive_marking
            else:
                print(
                    f"\033[31m {history_query_third} \033[36m is the Wrong Answer")
                history_marks -= negative_marking
            # Question No. 4
            history_query_fourth = input("""\033[38m 
Q4. Which City is located on the Bank of Gomati River ? 
A - Delhi
B - Patna
C - Kanpur
D - Lucknow\n>> """).title()
            if history_query_fourth == str(history_answer_list[3]):
                print(
                    f"\033[38m {history_query_fourth} \033[36m is the Correct Answer")
                history_marks += positive_marking
            else:
                print(
                    f"\033[31m {history_query_fourth} \033[36m is the Wrong Answer")
                history_marks -= negative_marking
            # Question No. 5
            history_query_fifth = input("""\033[38m
Q5. When was The Great Alexander came in India (B.C) ? 
A - 236
B - 323
C - 326
D - 330\n>> """).title()
            if history_query_fifth == str(history_answer_list[4]):
                print(
                    f"\033[38m {history_query_fifth} \033[36m is the Correct Answer")
                history_marks += positive_marking
            else:
                print(
                    f"\033[31m {history_query_fifth} \033[36m is the Wrong Answer")
                history_marks -= negative_marking
        print("\n\033[38mDo you want to continue or not!")
        main_quiz_continue = input("Press (Y) - Yes or (N) - No : ").upper()
        if main_quiz_continue == 'Y':
            continue
        elif main_quiz_continue == 'N':
            print(f"\033[33mTotal Marks in history is : {history_marks} Marks")
            break
        else:
            print("\033[36mYou have entered wrong input")
    elif options == 5:
        print("\n You are now Exit...")
        break
    else:
        print("\n\033[31mYou have entered wrong input try again..\n\033[38m")
print("".center(50, "^"))
print("FINAL REPORT CARD".center(50))

print(f"""\033[33m
Marks in Science           :  {science_marks} points
Marks in History           :  {history_marks} points
Marks in Geography         :  {geography_marks} points
Marks in General Awareness :  {general_aware_marks} points""")
total_marks = science_marks + history_marks + \
    geography_marks + general_aware_marks
print(f"""---------------------------------------a
Total Marks                :  {total_marks} points
---------------------------------------""")
if total_marks <= 7:
    print(f"\033[38m{name.upper()} YOUR GRADE IS \033[33m'E'")
elif total_marks <= 10:
    print(f"\033[38m{name.upper()} YOUR GRADE IS \033[33m'D'")
elif total_marks <= 13:
    print(f"\033[38m{name.upper()} YOUR GRADE IS \033[33m'C'")
elif total_marks <= 16:
    print(f"\033[38m{name.upper()} YOUR GRADE IS \033[33m'B'")
else:
    print(f"\033[38m{name.upper()} YOUR GRADE IS \033[33m'A'")
