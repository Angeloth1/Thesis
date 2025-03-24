import json
import random
import time
import sqlite3
import aiohttp
import asyncio
from faker import Faker
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# Δημιουργία ενός αντικειμένου Faker για την παραγωγή τυχαίων δεδομένων
fake = Faker()

# Επιλογές για επίπεδα εξυπνάδας των bots
intelligence_levels = ["Low", "Medium", "High", "Realistic"]

# Θέματα για τα posts
topics = ["Technology", "Health", "Politics", "Entertainment", "Sports", "Travel"]

# Ορισμός της Ollama API URL για τη σύνδεση με το μοντέλο Mistral
OLLAMA_API_URL = "http://localhost:11434/v1/chat/completions"  # Διεύθυνση URL του Ollama API

# Δημιουργία Bot User με τυχαία στοιχεία
def create_bot(intelligence_level, bots):
    bot = {
        "name": fake.name(),
        "email": fake.email(),
        "password": fake.password(),
        "ip_address": fake.ipv4(),
        "bank_account": fake.iban(),
        "intelligence": intelligence_level,
        "posts": [],
        "chat": [],
        "last_active": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_login": datetime.now().strftime("%Y-%m-%d"),
    }
    return bot

# Συνάρτηση για τη χρήση του Mistral μοντέλου μέσω της Ollama API με aiohttp (Asynchronous)
async def ask_mistral_async(session, prompt, retries=3):
    payload = {
        "model": "llama3.1:latest",
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {"Content-Type": "application/json"}

    for attempt in range(retries):
        try:
            async with session.post(OLLAMA_API_URL, json=payload, headers=headers, timeout=60) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['choices'][0]['message']['content']
        except Exception as e:
            print(Fore.RED + f"Error: {e}")  # Color the error messages in red
            break
        time.sleep(2)  # Retry after 2 seconds
    return None

# Συνάρτηση για να τρέχει τα αιτήματα παράλληλα (Asynchronous)
async def ask_mistral_parallel_async(prompts):
    async with aiohttp.ClientSession() as session:
        tasks = [ask_mistral_async(session, prompt) for prompt in prompts]
        return await asyncio.gather(*tasks)

# Δημιουργία δημοσιεύσεων για το bot
def generate_posts():
    num_posts = random.randint(1, 5)
    posts = []
    prompts = []
    for _ in range(num_posts):
        topic = random.choice(topics)
        post_prompt = f"Create a post about {topic}."
        prompts.append(post_prompt)

    post_contents = asyncio.run(ask_mistral_parallel_async(prompts))  # Χρησιμοποιεί async εδώ
    for post_content in post_contents:
        if post_content:
            posts.append({"post": post_content, "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    return posts

# Δημιουργία συνομιλιών για το bot
def generate_chat(bots):
    chat = []
    num_interactions = random.randint(1, 5)
    prompts = []
    if len(bots) > 1:
        for _ in range(num_interactions):
            interacting_bot = random.choice(bots)
            chat_prompt = f"Generate a conversation between {fake.name()} and {interacting_bot['name']}."
            prompts.append(chat_prompt)

    chat_contents = asyncio.run(ask_mistral_parallel_async(prompts))  # Χρησιμοποιεί async εδώ
    for chat_content in chat_contents:
        if chat_content:
            chat.append({
                "interaction": chat_content,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    return chat

# Τυχαία Διαστήματα για τα Posts
def schedule_posts():
    today = datetime.today()
    days_to_post = random.sample(range(1, 31), 10)  # Κάθε μήνα έχει 30 μέρες
    post_dates = []
    for day in days_to_post:
        post_date = today.replace(day=day)
        post_dates.append(post_date.strftime("%Y-%m-%d"))
    return post_dates

# Σύνδεση με τη βάση δεδομένων
def create_db():
    conn = sqlite3.connect('bot_users.db')
    c = conn.cursor()

    # Δημιουργία πινάκων
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        password TEXT,
        last_active TEXT,
        last_login TEXT
    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        post TEXT,
        post_date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        chat_content TEXT,
        chat_date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

    conn.commit()
    conn.close()

# Αποθήκευση στους πίνακες της SQL
def save_to_db(bots):
    conn = sqlite3.connect('bot_users.db')
    c = conn.cursor()

    for bot in bots:
        c.execute("INSERT INTO users (name, email, password, last_active, last_login) VALUES (?, ?, ?, ?, ?)",
                  (bot['name'], bot['email'], bot['password'], bot['last_active'], bot['last_login']))
        user_id = c.lastrowid  # Παίρνουμε το user_id για να συνδέσουμε τα posts και τα chats με τον χρήστη

        for post in bot['posts']:
            c.execute("INSERT INTO posts (user_id, post, post_date) VALUES (?, ?, ?)",
                      (user_id, post['post'], post['date']))

        for chat in bot['chat']:
            c.execute("INSERT INTO chats (user_id, chat_content, chat_date) VALUES (?, ?, ?)",
                      (user_id, chat['interaction'], chat['date']))

    conn.commit()
    conn.close()

# Προσομοίωση αλληλεπιδράσεων των bots για έναν καθορισμένο αριθμό μηνών
def simulate_interactions(bots, months):
    for month in range(months):
        print(f"Simulating month {month + 1}/{months}...")
        for day in range(30):
            print(Fore.GREEN + f"Simulating day {day + 1}/30...")  # Green color for the next day messages
            for bot in bots:
                new_posts = generate_posts()
                bot["posts"].extend(new_posts)
                chat_interactions = generate_chat(bots)
                bot["chat"].extend(chat_interactions)
                bot["last_active"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time.sleep(0.1)

# Αποθήκευση των δεδομένων σε αρχείο JSON
def save_data_to_json(bots):
    with open("bot_users_simulated.json", "w") as outfile:
        json.dump(bots, outfile, indent=4)

def main():
    create_db()  # Δημιουργία της βάσης δεδομένων αν δεν υπάρχει
    print("Welcome to the Bot Creator CLI!")
    num_bots = int(input("Enter the number of bots you want to create: "))
    intelligence_level = input(f"Select intelligence level ({', '.join(intelligence_levels)}): ")
    simulation_duration = int(input("Enter the number of months for simulation: "))

    if intelligence_level not in intelligence_levels:
        print("Invalid intelligence level! Setting to Medium.")
        intelligence_level = "Medium"

    bots = []
    for _ in range(num_bots):
        bot = create_bot(intelligence_level, bots)
        bots.append(bot)

    simulate_interactions(bots, simulation_duration)

    save_choice = input("Would you like to save the bots and interactions to a database? (y/n): ")
    if save_choice.lower() == 'y':
        save_to_db(bots)
    else:
        save_data_to_json(bots)

    print(f"{num_bots} bots have been created and interactions simulated for {simulation_duration} months. Data saved to 'bot_users_simulated.json'.")

if __name__ == "__main__":
    main()
