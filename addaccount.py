import sqlite3

db=sqlite3.connect("bookstore.db")
cursor = db.cursor()

for i in range(30):
    row = [str("newuser" + str(i)), str("key" + str(i)), str("John" + str(i)), str("Doe" + str(i)), str("jd"+str(i)+"@email.com"), 0]
    print(str(row))
    cursor.execute('INSERT into accounts (user_id, password, fname, lname, email, saved_payment) values (?,?,?,?,?,?)', row)
    db.commit()
cursor.close()
print("DONE")
