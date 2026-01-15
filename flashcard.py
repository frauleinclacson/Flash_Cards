import os
import json
import time
import threading
from datetime import datetime

# File to store flashcard decks
DECKS_FILE = "flashcard_decks.json"

# Color codes
PURPLE = '\033[95m'
BLUE = '\033[94m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

# Timer variables
timer_running = False
time_remaining = 0

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_decks():
    """Load all decks from file"""
    if not os.path.exists(DECKS_FILE):
        # Create sample deck
        return [{
            "name": "Sample Deck",
            "cards": [
                {"question": "What is the capital of France?", "answer": "Paris", "difficulty": "easy"},
                {"question": "What is 15 × 12?", "answer": "180", "difficulty": "medium"},
                {"question": "Explain quantum entanglement", "answer": "A quantum phenomenon where particles become interconnected", "difficulty": "hard"}
            ]
        }]
    
    with open(DECKS_FILE, 'r') as f:
        return json.load(f)

def save_decks(decks):
    """Save all decks to file"""
    with open(DECKS_FILE, 'w') as f:
        json.dump(decks, f, indent=2)

def timer_countdown(seconds):
    """Countdown timer that runs in background"""
    global timer_running, time_remaining
    timer_running = True
    time_remaining = seconds
    
    while time_remaining > 0 and timer_running:
        time.sleep(1)
        time_remaining -= 1
    
    timer_running = False

def format_time(seconds):
    """Format seconds to MM:SS"""
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins}:{secs:02d}"

def print_header(text):
    """Print a styled header"""
    print(f"\n{PURPLE}{BOLD}{'=' * 60}")
    print(f"{text.center(60)}")
    print(f"{'=' * 60}{RESET}\n")

def view_all_decks(decks):
    """Display all decks"""
    clear_screen()
    print_header("📚 YOUR FLASHCARD DECKS")
    
    if not decks:
        print(f"{RED}No decks found! Create one to get started.{RESET}\n")
        return
    
    for i, deck in enumerate(decks, 1):
        card_count = len(deck['cards'])
        easy = sum(1 for c in deck['cards'] if c['difficulty'] == 'easy')
        medium = sum(1 for c in deck['cards'] if c['difficulty'] == 'medium')
        hard = sum(1 for c in deck['cards'] if c['difficulty'] == 'hard')
        
        print(f"{CYAN}{i}. {BOLD}{deck['name']}{RESET}")
        print(f"   {GREEN}Total Cards: {card_count}{RESET}")
        print(f"   {GREEN}Easy: {easy}{RESET} | {YELLOW}Medium: {medium}{RESET} | {RED}Hard: {hard}{RESET}")
        print()

def create_deck(decks):
    """Create a new deck"""
    clear_screen()
    print_header("➕ CREATE NEW DECK")
    
    name = input(f"{CYAN}Enter deck name: {RESET}").strip()
    
    if not name:
        print(f"{RED}Deck name cannot be empty!{RESET}")
        input("Press Enter to continue...")
        return
    
    decks.append({"name": name, "cards": []})
    save_decks(decks)
    print(f"{GREEN}✓ Deck '{name}' created successfully!{RESET}")
    input("Press Enter to continue...")

def select_deck(decks, action_text):
    """Helper function to select a deck"""
    clear_screen()
    view_all_decks(decks)
    
    if not decks:
        input("Press Enter to continue...")
        return None
    
    try:
        deck_num = int(input(f"{CYAN}{action_text}: {RESET}")) - 1
        
        if 0 <= deck_num < len(decks):
            return deck_num
        else:
            print(f"{RED}Invalid deck number!{RESET}")
            input("Press Enter to continue...")
            return None
    except ValueError:
        print(f"{RED}Please enter a valid number!{RESET}")
        input("Press Enter to continue...")
        return None

def add_card_to_deck(decks):
    """Add a flashcard to a deck - Step by step process"""
    # Step 1: Choose deck
    deck_num = select_deck(decks, "Select deck to add card to")
    if deck_num is None:
        return
    
    # Step 2: Enter question
    clear_screen()
    print_header(f"➕ ADD CARD TO: {decks[deck_num]['name']}")
    print(f"{PURPLE}{BOLD}Step 1: Enter Question{RESET}\n")
    
    question = input(f"{CYAN}Enter question: {RESET}").strip()
    if not question:
        print(f"{RED}Question cannot be empty!{RESET}")
        input("Press Enter to continue...")
        return
    
    # Step 3: Choose difficulty
    clear_screen()
    print_header(f"➕ ADD CARD TO: {decks[deck_num]['name']}")
    print(f"{PURPLE}{BOLD}Step 2: Choose Difficulty{RESET}\n")
    print(f"{CYAN}Question: {question}{RESET}\n")
    
    print(f"{GREEN}1. Easy{RESET}")
    print(f"{YELLOW}2. Medium{RESET}")
    print(f"{RED}3. Hard{RESET}")
    
    diff_choice = input(f"\n{CYAN}Select difficulty (1-3): {RESET}").strip()
    difficulty_map = {"1": "easy", "2": "medium", "3": "hard"}
    difficulty = difficulty_map.get(diff_choice, "medium")
    
    # Step 4: Enter answer
    clear_screen()
    print_header(f"➕ ADD CARD TO: {decks[deck_num]['name']}")
    print(f"{PURPLE}{BOLD}Step 3: Enter Answer{RESET}\n")
    print(f"{CYAN}Question: {question}{RESET}")
    
    diff_color = GREEN if difficulty == 'easy' else YELLOW if difficulty == 'medium' else RED
    print(f"{diff_color}Difficulty: {difficulty.upper()}{RESET}\n")
    
    answer = input(f"{CYAN}Enter answer: {RESET}").strip()
    if not answer:
        print(f"{RED}Answer cannot be empty!{RESET}")
        input("Press Enter to continue...")
        return
    
    # Add card to deck
    decks[deck_num]['cards'].append({
        "question": question,
        "answer": answer,
        "difficulty": difficulty
    })
    
    save_decks(decks)
    print(f"\n{GREEN}✓ Card added successfully!{RESET}")
    input("Press Enter to continue...")

def delete_card_from_deck(decks):
    """Delete a specific card from a deck"""
    # Step 1: Choose deck
    deck_num = select_deck(decks, "Select deck to delete card from")
    if deck_num is None:
        return
    
    deck = decks[deck_num]
    
    if not deck['cards']:
        print(f"{RED}This deck has no cards!{RESET}")
        input("Press Enter to continue...")
        return
    
    # Step 2: Show all cards and select one to delete
    clear_screen()
    print_header(f"🗑️ DELETE CARD FROM: {deck['name']}")
    
    for i, card in enumerate(deck['cards'], 1):
        diff_color = GREEN if card['difficulty'] == 'easy' else YELLOW if card['difficulty'] == 'medium' else RED
        print(f"{CYAN}{i}.{RESET} {diff_color}[{card['difficulty'].upper()}]{RESET}")
        print(f"   Q: {card['question']}")
        print(f"   A: {card['answer']}")
        print()
    
    try:
        card_num = int(input(f"{CYAN}Select card to delete (1-{len(deck['cards'])}): {RESET}")) - 1
        
        if 0 <= card_num < len(deck['cards']):
            deleted_card = deck['cards'][card_num]
            confirm = input(f"{RED}Delete this card? (y/n): {RESET}").strip().lower()
            
            if confirm == 'y':
                deck['cards'].pop(card_num)
                save_decks(decks)
                print(f"{GREEN}✓ Card deleted successfully!{RESET}")
            else:
                print(f"{YELLOW}Deletion cancelled.{RESET}")
        else:
            print(f"{RED}Invalid card number!{RESET}")
        
        input("Press Enter to continue...")
    except ValueError:
        print(f"{RED}Please enter a valid number!{RESET}")
        input("Press Enter to continue...")

def delete_deck(decks):
    """Delete an entire deck"""
    deck_num = select_deck(decks, "Select deck to delete")
    if deck_num is None:
        return
    
    deck_name = decks[deck_num]['name']
    confirm = input(f"{RED}Are you sure you want to delete '{deck_name}' and ALL its cards? (y/n): {RESET}").strip().lower()
    
    if confirm == 'y':
        decks.pop(deck_num)
        save_decks(decks)
        print(f"{GREEN}✓ Deck deleted successfully!{RESET}")
    else:
        print(f"{YELLOW}Deletion cancelled.{RESET}")
    
    input("Press Enter to continue...")

def study_deck(decks):
    """Study a selected deck - Step by step process"""
    global timer_running, time_remaining
    
    # Step 1: Choose deck
    deck_num = select_deck(decks, "Select deck to study")
    if deck_num is None:
        return
    
    deck = decks[deck_num]
    
    if not deck['cards']:
        print(f"{RED}This deck has no cards! Add some first.{RESET}")
        input("Press Enter to continue...")
        return
    
    # Step 2: Choose difficulty filter
    clear_screen()
    print_header(f"🎯 STEP 1: FILTER BY DIFFICULTY")
    print(f"{CYAN}Studying: {BOLD}{deck['name']}{RESET}\n")
    
    print(f"{GREEN}1. Easy only{RESET}")
    print(f"{YELLOW}2. Medium only{RESET}")
    print(f"{RED}3. Hard only{RESET}")
    print(f"{CYAN}4. Easy + Medium{RESET}")
    print(f"{CYAN}5. Medium + Hard{RESET}")
    print(f"{CYAN}6. All difficulties{RESET}")
    
    filter_choice = input(f"\n{CYAN}Select filter (1-6): {RESET}").strip()
    
    # Filter cards based on choice
    if filter_choice == "1":
        filtered_cards = [c for c in deck['cards'] if c['difficulty'] == 'easy']
    elif filter_choice == "2":
        filtered_cards = [c for c in deck['cards'] if c['difficulty'] == 'medium']
    elif filter_choice == "3":
        filtered_cards = [c for c in deck['cards'] if c['difficulty'] == 'hard']
    elif filter_choice == "4":
        filtered_cards = [c for c in deck['cards'] if c['difficulty'] in ['easy', 'medium']]
    elif filter_choice == "5":
        filtered_cards = [c for c in deck['cards'] if c['difficulty'] in ['medium', 'hard']]
    else:
        filtered_cards = deck['cards'].copy()
    
    if not filtered_cards:
        print(f"{RED}No cards match this filter!{RESET}")
        input("Press Enter to continue...")
        return
    
    # Step 3: Choose timer
    clear_screen()
    print_header(f"⏱️ STEP 2: SELECT TIMER")
    print(f"{CYAN}Studying: {BOLD}{deck['name']}{RESET}")
    print(f"{GREEN}Cards to study: {len(filtered_cards)}{RESET}\n")
    
    print(f"{CYAN}1. 10 seconds{RESET}")
    print(f"{CYAN}2. 30 seconds{RESET}")
    print(f"{CYAN}3. 1 minute{RESET}")
    print(f"{CYAN}4. No timer{RESET}")
    
    timer_choice = input(f"\n{CYAN}Select timer (1-4): {RESET}").strip()
    timer_map = {"1": 10, "2": 30, "3": 60, "4": 0}
    timer_seconds = timer_map.get(timer_choice, 0)
    
    # Step 4: Study session
    clear_screen()
    print(f"{GREEN}Starting study session...{RESET}")
    time.sleep(1)
    
    card_index = 0
    
    while True:
        clear_screen()
        card = filtered_cards[card_index]
        
        # Get difficulty color
        diff_color = GREEN if card['difficulty'] == 'easy' else YELLOW if card['difficulty'] == 'medium' else RED
        
        print_header(f"📖 STUDYING: {deck['name']}")
        print(f"{CYAN}Card {card_index + 1} of {len(filtered_cards)}{RESET}")
        print(f"{diff_color}Difficulty: {card['difficulty'].upper()}{RESET}\n")
        
        # Start timer if enabled
        if timer_seconds > 0:
            timer_thread = threading.Thread(target=timer_countdown, args=(timer_seconds,))
            timer_thread.daemon = True
            timer_thread.start()
        
        # Show question
        print(f"{PURPLE}{BOLD}QUESTION:{RESET}")
        print(f"{card['question']}\n")
        
        if timer_seconds > 0:
            print(f"{YELLOW}⏱️  Timer: {format_time(timer_seconds)}{RESET}")
        
        input(f"\n{CYAN}Press Enter to reveal answer...{RESET}")
        
        # Stop timer
        timer_running = False
        
        # Show answer
        clear_screen()
        print_header(f"📖 STUDYING: {deck['name']}")
        print(f"{CYAN}Card {card_index + 1} of {len(filtered_cards)}{RESET}")
        print(f"{diff_color}Difficulty: {card['difficulty'].upper()}{RESET}\n")
        
        print(f"{PURPLE}{BOLD}QUESTION:{RESET}")
        print(f"{card['question']}\n")
        
        print(f"{GREEN}{BOLD}ANSWER:{RESET}")
        print(f"{card['answer']}\n")
        
        # Navigation
        print(f"\n{CYAN}{'─' * 60}{RESET}")
        print(f"{CYAN}[N]ext  [P]revious  [S]huffle  [Q]uit{RESET}")
        
        choice = input(f"{CYAN}Your choice: {RESET}").strip().lower()
        
        if choice == 'q':
            break
        elif choice == 'n':
            card_index = (card_index + 1) % len(filtered_cards)
        elif choice == 'p':
            card_index = (card_index - 1) % len(filtered_cards)
        elif choice == 's':
            import random
            random.shuffle(filtered_cards)
            card_index = 0
            print(f"{GREEN}✓ Cards shuffled!{RESET}")
            time.sleep(1)
    
    print(f"{GREEN}Study session completed! Great work! 🎉{RESET}")
    input("Press Enter to continue...")

def main_menu():
    """Main menu"""
    decks = load_decks()
    
    while True:
        clear_screen()
        print_header("📚 FLASHCARD STUDY APP")
        
        print(f"{PURPLE}1.{RESET} View All Decks")
        print(f"{PURPLE}2.{RESET} Create New Deck")
        print(f"{PURPLE}3.{RESET} Add Card to Deck")
        print(f"{PURPLE}4.{RESET} Delete Card from Deck")
        print(f"{PURPLE}5.{RESET} Delete Entire Deck")
        print(f"{PURPLE}6.{RESET} Study Deck")
        print(f"{PURPLE}7.{RESET} Save & Exit")
        
        choice = input(f"\n{CYAN}Select option (1-7): {RESET}").strip()
        
        if choice == '1':
            view_all_decks(decks)
            input("Press Enter to continue...")
        elif choice == '2':
            create_deck(decks)
        elif choice == '3':
            add_card_to_deck(decks)
        elif choice == '4':
            delete_card_from_deck(decks)
        elif choice == '5':
            delete_deck(decks)
        elif choice == '6':
            study_deck(decks)
        elif choice == '7':
            save_decks(decks)
            clear_screen()
            print(f"{GREEN}{BOLD}Your decks have been saved! Happy studying! 📚✨{RESET}\n")
            break
        else:
            print(f"{RED}Invalid choice! Please select 1-7.{RESET}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main_menu()