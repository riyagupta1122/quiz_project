import json
import os
import time
from colorama import Fore, Style, init


init(autoreset=True)

def load_questions(category="general"):
    
    filename = f"{category}_questions.json"
    try:
        with open(filename, 'r') as file:
            questions = json.load(file)
        return questions
    except FileNotFoundError:
        print(f"{Fore.RED}Error: {filename} file not found!{Style.RESET_ALL}")
        return []
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error: {filename} file is not valid JSON!{Style.RESET_ALL}")
        return []

def get_high_score(category="general"):
    """Read the high score from file for a specific category"""
    filename = f"{category}_high_score.txt"
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                content = file.read().strip()
                if content:
                    return int(content)
        return 0
    except (ValueError, FileNotFoundError):
        return 0

def save_high_score(score, category="general"):
    
    filename = f"{category}_high_score.txt"
    try:
        with open(filename, 'w') as file:
            file.write(str(score))
    except Exception as e:
        print(f"{Fore.RED}Error saving high score: {e}{Style.RESET_ALL}")

def ask_question_with_timer(question, question_num, total_questions, time_limit=15):
    
    
    progress = f"[{question_num}/{total_questions}]"
    print(f"{Fore.CYAN}{progress} {question['question']}{Style.RESET_ALL}")

    for index, option in enumerate(question['options'], start=1):
        print(f"  {Fore.YELLOW}{index}.{Style.RESET_ALL} {option}")

    print(f"{Fore.MAGENTA}\n⏰ You have {time_limit} seconds to answer!{Style.RESET_ALL}")
    start_time = time.time()

    user_answer = None
    while time.time() - start_time < time_limit:
        remaining = time_limit - (time.time() - start_time)

        
        if remaining < 5:
            print(f"{Fore.RED}⏰ {int(remaining)} seconds left!{Style.RESET_ALL}")

        try:
            user_answer = input(f"\n{Fore.GREEN}Your answer (1-4): {Style.RESET_ALL}")
            if user_answer in ['1', '2', '3', '4']:
                break
            else:
                print(f"{Fore.RED}❌ Invalid input. Please enter 1, 2, 3, or 4.{Style.RESET_ALL}")
        except:
            break

        time.sleep(0.1)  

    if user_answer is None or user_answer not in ['1', '2', '3', '4']:
        print(f"\n{Fore.RED}⏰ Time's up!{Style.RESET_ALL}")
        user_answer = "0"  

    return user_answer

def show_category_menu():
    """Display category selection menu"""
    print(f"\n{Fore.BLUE}🎯 SELECT QUIZ CATEGORY{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1.{Style.RESET_ALL} General Knowledge")
    print(f"{Fore.YELLOW}2.{Style.RESET_ALL} Python Programming")
    print(f"{Fore.YELLOW}3.{Style.RESET_ALL} Science & Technology")

    while True:
        choice = input(f"\n{Fore.GREEN}Choose category (1-3): {Style.RESET_ALL}")
        if choice in ['1', '2', '3']:
            categories = {
                '1': 'general',
                '2': 'python', 
                '3': 'science'
            }
            return categories[choice]
        print(f"{Fore.RED}❌ Invalid choice. Please enter 1, 2, or 3.{Style.RESET_ALL}")

def run_quiz():
    """Main quiz function"""
    print(f"{Fore.BLUE}=" * 50)
    print(f"🎯 WELCOME TO THE PYTHON QUIZ APPLICATION!")
    print(f"=" * 50 + Style.RESET_ALL)

    
    category = show_category_menu()
    category_names = {
        'general': 'General Knowledge',
        'python': 'Python Programming',
        'science': 'Science & Technology'
    }

    
    questions = load_questions(category)

    if not questions:
        print(f"{Fore.RED}No questions found for this category. Exiting.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.GREEN}Starting {category_names[category]} Quiz!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}You will be presented with {len(questions)} questions.")
    print(f"Enter the number (1-4) of your chosen answer.{Style.RESET_ALL}\n")

    score = 0
    high_score = get_high_score(category)
    wrong_answers = []

    
    for i, q in enumerate(questions, 1):
        user_answer = ask_question_with_timer(q, i, len(questions))

        if user_answer == q['answer']:
            print(f"{Fore.GREEN}✅ Correct!{Style.RESET_ALL}\n")
            score += 1
        else:
            correct_index = int(q['answer']) - 1
            correct_answer = q['options'][correct_index]
            print(f"{Fore.RED}❌ Wrong! The correct answer is: {correct_answer}{Style.RESET_ALL}\n")
            wrong_answers.append({
                'question': q['question'],
                'your_answer': q['options'][int(user_answer)-1] if user_answer != '0' else 'Time Out',
                'correct_answer': correct_answer
            })

        time.sleep(1)  
    print(f"{Fore.BLUE}=" * 50)
    print(f"📊 QUIZ FINISHED - RESULTS")
    print(f"=" * 50 + Style.RESET_ALL)
    print(f"{Fore.CYAN}Your final score: {Fore.YELLOW}{score}/{len(questions)}{Style.RESET_ALL}")

    
    if wrong_answers:
        print(f"\n{Fore.RED}📝 Questions you missed:{Style.RESET_ALL}")
        for i, wrong in enumerate(wrong_answers, 1):
            print(f"\n{Fore.YELLOW}{i}. {wrong['question']}{Style.RESET_ALL}")
            print(f"   Your answer: {Fore.RED}{wrong['your_answer']}{Style.RESET_ALL}")
            print(f"   Correct answer: {Fore.GREEN}{wrong['correct_answer']}{Style.RESET_ALL}")

    
    if score > high_score:
        print(f"\n{Fore.YELLOW}🎉 NEW HIGH SCORE! 🎉{Style.RESET_ALL}")
        save_high_score(score, category)
        high_score = score
    elif score == high_score and high_score > 0:
        print(f"\n{Fore.CYAN}🔥 You matched the high score! 🔥{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.MAGENTA}Current high score: {high_score}{Style.RESET_ALL}")

    print(f"{Fore.GREEN}Your best in this category: {high_score}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}=" * 50 + Style.RESET_ALL)
if __name__ == "__main__":
    run_quiz()