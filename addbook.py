import sqlite3

db=sqlite3.connect("bookstore.db")
cursor = db.cursor()

for i in range(30):
    row = [str("newbook" + str(i)), str("author" + str(i)), str("No." + str(i) + " publish"), float("{:.2f}".format(i * 32.2)), int(i), 0]
    print(str(row))
    cursor.execute('INSERT into books (title, author, publisher, price, available,sold) values (?,?,?,?,?,?)', row)
    db.commit()
cursor.close()
print("DONE")
