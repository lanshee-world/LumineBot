import pandas as pd
import re
import random
import os

# --- CONFIGURATION ---
CSV_FILE = "lumine_bot.csv"
LOG_FILE = "unanswered_queries.txt"

# 1. Load the data with 'keep_default_na=False' to fix the 'nan' error
try:
    # This specifically prevents empty cells from being read as 'nan'
    df = pd.read_csv(CSV_FILE, keep_default_na=False)
except FileNotFoundError:
    print(f"Error: '{CSV_FILE}' not found. Ensure it is in the same folder as this script.")
    exit()

def log_unknown_query(query):
    """Saves queries the bot didn't understand to a file for later review."""
    with open(LOG_FILE, "a") as f:
        f.write(query + "\n")

# --- 2. THE SOPHISTICATED ENGLISH WELCOME ---
# This ignores Sheng/Swahili for the very first greeting
welcome_row = df[df['Category'] == 'English_Welcome']
if not welcome_row.empty:
    # Pick a random exquisite greeting
    welcome_options = str(welcome_row.iloc[0]['Responses']).split('|')
    print(f"Luminebot: {random.choice(welcome_options)}")
else:
    print("Luminebot: Welcome to Lumine. How can I assist you with our prestigious collection today?")

# --- 3. MAIN CONVERSATION LOOP ---
while True:
    raw_input = input("\nYou: ").lower().strip()
    
    # Check for exit commands
    if raw_input in ["quit", "exit", "bye", "kwaheri", "tutaonana"]:
        print("Luminebot: Stay stylish. Goodbye!")
        break

    # Clean up common Sheng/Slang typing habits for better matching
    # This helps catch "natafuta" or "mkona" which users type as one word
    user_text = raw_input.replace("natafuta", "na tafuta").replace("mkona", "mko na").replace("iko", "iko ")

    found_answer = False
    possible_matches = []

    # Search for matches using word boundaries (\b)
    for index, row in df.iterrows():
        # Skip the internal English_Welcome category during the chat loop
        if row['Category'] == 'English_Welcome':
            continue

        keywords_list = str(row['Keywords']).split(';')
        for word in keywords_list:
            clean_word = word.strip().lower()
            
            # Check if keyword exists as a whole word in user input
            if clean_word and re.search(r'\b' + re.escape(clean_word) + r'\b', user_text):
                possible_matches.append(row)
                found_answer = True
                break 
    
    # Handle the Response
    if found_answer:
        # Pick the last match found (usually the most specific)
        best_match = possible_matches[-1]
        
        # Split the multiple responses by '|' and pick one at random
        response_options = str(best_match['Responses']).split('|')
        final_response = random.choice(response_options)
        
        print(f"Luminebot: {final_response}")
    
    else:
        # If no answer, log it so you can see it in 'unanswered_queries.txt'
        print("Luminebot: I'm not quite sure about that yet. I've noted it down so my team can teach me!")
        log_unknown_query(raw_input)