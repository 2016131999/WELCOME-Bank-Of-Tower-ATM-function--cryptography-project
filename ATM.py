from datetime import datetime 
import time
from RSA_General import encrypt
from RSA_General import decrypt, decrypt_text
import sqlite3
import hashlib
import numpy as np

public_key = (4351, 7081)
private_key = (2815, 7081)
d = private_key[0]
e = public_key[0]
n = public_key[1]


def is_valid_pin_length(a):
    if len(a) != 4:
        return False
    else:
        return True


def set_pin(card):
    pin = input("Set PIN\n")
    if not is_valid_pin_length(pin):
        print("Invalid PIN Length! Enter Valid PIN!")
        while not is_valid_pin_length(pin):
            pin = input("Set PIN\n")
    pin = encrypt(pin, public_key[0], public_key[1])[0]
    conn = sqlite3.connect("AccountsInfo.db")
    conn.execute("UPDATE Accounts SET Pin = ? WHERE Card_No = ?", (str(pin), str(card)))
    conn.commit()
    conn.close()


def is_valid_pin(card, a):
    conn = sqlite3.connect("AccountsInfo.db")
    cur = conn.execute("SELECT * FROM Accounts WHERE Card_No = ?", (str(card),))
    for row in cur:
        if row[5] == str(a[0]):
            return True
    return False


def custom_similarity(input_pin, correct_pin):
    pin1 = np.array([int(x) for x in decrypt(input_pin[1], private_key[0], private_key[1])])
    pin2 = np.array([int(x) for x in decrypt_text(correct_pin, private_key[0], private_key[1])])
    similarity = 0
    for i in range(4):
        similarity += pin1[i]-pin2[i] if pin1[i] > pin2[i] else pin2[i]-pin1[i]
    return similarity


def anomaly_behaviour(card, time_taken, pin_similarity):
    score = 0
    if pin_similarity > 10:
        score += 10
    elif time_taken > 15:
        score += 1
    conn = sqlite3.connect("AccountsInfo.db")
    conn.execute("UPDATE Accounts SET score = ?, Last_Score_Update = ? WHERE Card_No = ?", (score, str(datetime.now()), str(card)))
    print(card)
    conn.commit()
    conn.close()


def withdrawal(card):
    conn = sqlite3.connect("AccountsInfo.db")
    card = str(hashlib.sha512(card.encode()).hexdigest())
    cur = conn.execute("SELECT * FROM Accounts WHERE Card_No = ?", (str(card),))
    for row in cur:
        if row[5] is None:
            set_pin(card)
        else:
            start = time.time()
            pin_user = input("Enter PIN\n")
            end = time.time()
            pin_input_time = end-start
            if is_valid_pin(card, encrypt(pin_user, public_key[0], public_key[1])):
                amount = float(input("ENTER AMOUNT TO WITHDRAW\n"))
                balance = row[4] - amount
                if balance < 0:
                    print("Not Sufficient Balance!!")
                else:
                    cur.execute("UPDATE Accounts SET Amount = ? WHERE Card_No = ?", (str(balance), str(card)))
                    print("Transaction Successful!")
                    print("Available Balance: ", balance)
            else:
                correct_encrypted_pin = row[5]
                anomaly_behaviour(card,
                                  time_taken=pin_input_time,
                                  pin_similarity=custom_similarity(encrypt(pin_user, public_key[0], public_key[1]), correct_encrypted_pin))
                print("Incorrect PIN!")
    conn.commit()
    conn.close()


def check_balance(card):
    conn = sqlite3.connect("AccountsInfo.db")
    card = str(hashlib.sha512(card.encode()).hexdigest())
    cur = conn.execute("SELECT * FROM Accounts WHERE Card_No = ?", (str(card),))
    for row in cur:
        if row[5] is None:
            set_pin(card)
        else:
            start = time.time()
            pin_user = input("Enter PIN\n")
            end = time.time()
            pin_input_time = end-start
            if is_valid_pin(card, encrypt(pin_user, public_key[0], public_key[1])):
                print("Balance: ", row[4])
            else:
                correct_encrypted_pin = row[5]
                anomaly_behaviour(card,
                                  time_taken=pin_input_time,
                                  pin_similarity=custom_similarity(encrypt(pin_user, public_key[0], public_key[1]),
                                                                   correct_encrypted_pin))
                print("Incorrect PIN!")
    conn.commit()
    conn.close()


def change_pin(card):
    conn = sqlite3.connect("AccountsInfo.db")
    card = str(hashlib.sha512(card.encode()).hexdigest())
    cur = conn.execute("SELECT * FROM Accounts WHERE Card_No = ?", (str(card),))
    for row in cur:
        if row[5] is None:
            set_pin(card)
        else:
            start = time.time()
            pin_user = input("Enter PIN\n")
            end = time.time()
            pin_input_time = end-start
            if is_valid_pin(card, encrypt(pin_user, public_key[0], public_key[1])):
                set_pin(card)
            else:
                correct_encrypted_pin = row[5]
                anomaly_behaviour(card,
                                  time_taken=pin_input_time,
                                  pin_similarity=custom_similarity(encrypt(pin_user, public_key[0], public_key[1]),
                                                                   correct_encrypted_pin))
                print("Incorrect PIN!")
    conn.commit()
    conn.close()


def if_record_exists(a):
    conn = sqlite3.connect("AccountsInfo.db")
    cur = conn.cursor()
    a = str(hashlib.sha512(a.encode()).hexdigest())
    for row in cur.execute("SELECT * FROM Accounts WHERE Card_No = ?", (str(a),)):
        return True
    return False


print("***************WELCOME Bank Of Tower***************")
card_num = input("ENTER CARD NUMBER\n")
if not if_record_exists(card_num):
    print("No Records Found!")
else:
    task = int(input("1. Withdraw \n2. Check Balance\n3. Change PIN\n"))
    if task == 1:
        withdrawal(card_num)
    elif task == 2:
        check_balance(card_num)
    elif task == 3:
        change_pin(card_num)


#Card No 8117029392784680