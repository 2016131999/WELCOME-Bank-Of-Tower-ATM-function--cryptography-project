import sqlite3
import random
import re
import hashlib


def count_accounts():
    conn = sqlite3.connect("AccountsInfo.db")
    cursor = conn.execute('''SELECT COUNT(*) FROM Accounts''')
    count = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return count


def is_valid_card_no(card_no_to_check):
    # To Check if card number generated is available
    conn = sqlite3.connect("AccountsInfo.db")
    cursor = conn.execute('''SELECT Card_No FROM Accounts''')
    for row in cursor:
        if card_no_to_check == row:
            return False
    return True


def card_no_gen():
    result = ""
    for i in range(16):
        result += str(random.randint(0, 9))
    while not is_valid_card_no(result):
        for i in range(16):
            result += str(random.randint(0, 9))
    return result


def create_account():
    conn = sqlite3.connect("AccountsInfo.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Accounts(Account_No INTEGER, Card_No TEXT,
                    User_Name TEXT, Phone_Number TEXT, Amount FLOAT, Pin TEXT, Score INTEGER, 
                    Last_Score_Update TEXT )''')
    new_account_no = count_accounts() + 1
    new_card_no = card_no_gen()
    hashed_card_no = str(hashlib.sha512(new_card_no.encode()).hexdigest())
    new_user_name = input("Enter Name: ")
    new_phone_number = input("Enter Phone Number: ")
    new_amount = float(input("Enter Amount: "))
    cur.execute('''INSERT INTO Accounts (Account_No, Card_No, User_Name, Phone_Number, Amount, Score) 
                    VALUES (?, ?, ?, ?, ?, 0)''',
                (new_account_no, hashed_card_no, new_user_name, new_phone_number, new_amount))
    print("Card Number generated for the user is: ", new_card_no)
    conn.commit()
    conn.close()


def update_account(card):
    conn = sqlite3.connect("AccountsInfo.db")
    cur = conn.cursor()
    card = str(hashlib.sha512(card.encode()).hexdigest())
    cursor = cur.execute("SELECT * FROM Accounts WHERE Card_No = ?", (card,))
    record_exists = False
    for row in cursor:
        record_exists = True
    if record_exists:
        name = input("Enter Name:   ")
        cur.execute("UPDATE Accounts SET User_Name = ? WHERE Card_No = ?", (name, card))
        phone = int(input("Enter Phone Number:   "))
        cur.execute("UPDATE Accounts SET Phone_Number = ? WHERE Card_No = ?", (phone, card))
        amount = float(input("Enter Amount:    "))
        cur.execute("UPDATE Accounts SET Amount = ? WHERE Card_No = ?", (amount, card))
        conn.commit()
        conn.close()
    else:
        print("No such records found.")

print("*" * 17, "WELCOME Bank Of Tower", "*" * 17)
choice = int(input("Enter 1 to Create Account or 2 to Update Account Details\n"))
if choice == 1:
    create_account()
elif choice == 2:
    card_no = input("Enter Card Number:    ")
    if not re.match(r'[0-9]{16}', card_no):
        while not re.match(r'[0-9]{16}', card_no):
            print("Invalid Card Number")
            card_no = input("Enter Card Number:     ")
    update_account(card_no)
