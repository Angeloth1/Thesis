# Bot Users Simulator

Αυτό το CLI εργαλείο δημιουργεί και διαχειρίζεται αυτόνομους bot users, οι οποίοι προσομοιώνουν κοινωνικές αλληλεπιδράσεις μέσω τυχαίων δημοσιεύσεων και συνομιλιών.

## 🚀 Χαρακτηριστικά

- Δημιουργία bot users με τυχαία δεδομένα (όνομα, email, IP, τραπεζικό λογαριασμό, κ.λπ.)
- Διαφορετικά επίπεδα "εξυπνάδας" των bots: `Low`, `Medium`, `High`, `Realistic`
- Αυτόματη δημιουργία posts και συνομιλιών με χρήση **Ollama API** και μοντέλου **Mistral**
- Αποθήκευση δεδομένων σε **SQLite database** ή **JSON αρχείο**
- Προσομοίωση δραστηριότητας για καθορισμένο αριθμό μηνών

## 📦 Εξαρτήσεις

Πριν τρέξετε το πρόγραμμα, εγκαταστήστε τις απαιτούμενες βιβλιοθήκες:

```sh
pip install faker aiohttp sqlite3 colorama
```

## 🛠 Τρόπος Χρήσης

1. **Εκκίνηση του προγράμματος**  
   Εκτελέστε το αρχείο:

   ```sh
   python bot_simulator.py
   ```

2. **Δημιουργία bot users**  
   Θα σας ζητηθεί να εισάγετε:
   - Αριθμό bots
   - Επίπεδο εξυπνάδας (`Low`, `Medium`, `High`, `Realistic`)
   - Διάρκεια προσομοίωσης (μήνες)

3. **Αποθήκευση δεδομένων**  
   Επιλέξτε αν θέλετε να αποθηκεύσετε τα δεδομένα στη βάση δεδομένων (`SQLite`) ή σε αρχείο `JSON`.

## 🏗 Δομή Κώδικα

- **`create_bot()`**: Δημιουργεί ένα νέο bot με τυχαία στοιχεία.
- **`generate_posts()`**: Παράγει δημοσιεύσεις χρησιμοποιώντας το μοντέλο AI.
- **`generate_chat()`**: Δημιουργεί συνομιλίες μεταξύ των bots.
- **`save_to_db()`**: Αποθηκεύει τους χρήστες και τις αλληλεπιδράσεις τους σε **SQLite**.
- **`simulate_interactions()`**: Εκτελεί προσομοίωση για συγκεκριμένο αριθμό μηνών.
- **`save_data_to_json()`**: Αποθηκεύει τα δεδομένα των bots σε αρχείο **JSON**.

## 📂 Βάση Δεδομένων

Το πρόγραμμα δημιουργεί μια βάση δεδομένων **`bot_users.db`** με τις εξής δομές:

- **`users`** (id, name, email, password, last_active, last_login)
- **`posts`** (id, user_id, post, post_date)
- **`chats`** (id, user_id, chat_content, chat_date)

## ⚡ Παραδείγματα Χρήσης

```sh
Enter the number of bots you want to create: 10
Select intelligence level (Low, Medium, High, Realistic): High
Enter the number of months for simulation: 3
Would you like to save the bots and interactions to a database? (y/n): y
```

## 🔗 Συνδέσεις

- **[Ollama API](https://ollama.ai)**
- **[SQLite Documentation](https://www.sqlite.org/docs.html)**

## 📝 Άδεια

Αυτό το έργο διατίθεται υπό την άδεια **MIT**.

---

🎯 **Αναπτύξτε και βελτιώστε το σύστημα για να δημιουργήσετε πιο ρεαλιστικές αλληλεπιδράσεις!** 🚀
