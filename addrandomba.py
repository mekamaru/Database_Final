import sqlite3

db = sqlite3.connect("bookstore.db")
cursor = db.cursor()

db.execute('''CREATE TABLE IF NOT EXISTS accounts(
                   user_id TEXT PRIMARY KEY,
                   password TEXT NOT NULL,
                   fname TEXT,
                   lname TEXT,
                   email TEXT,
                   saved_payment INTEGER)''')

db.commit()
db.execute('''CREATE TABLE IF NOT EXISTS books(
                   book_id INTEGER PRIMARY KEY,
                   title TEXT,
                   author TEXT,
                   publisher TEXT,
                   price FLOAT,
                   available INTEGER,
                   sold INTEGER)''')
db.commit()

accrow = [
    ["maryr1234", "passformary", "Mary", "Robinson", "mrobinson@email.com"],
    ["Steve3", "SteveSteve", "Steven", "Jones", "sj0822@yahoo.com"],
    ["Chris225", "CatsWithHats", "Chris", "Robinson", "crobinson@email.com"],
    ["Chris11", "DogsWithBlogs", "Chris", "Migliore", "realemail@msn.com"],
    ["StillStanding", "JustBetter", "Elton", "John", "ejohn@yeahyeahyeah.com"],
    ["MikhailTheVast", "Winterborn", "Mikhail", "Hartman", "mfh1129@gmail.com"],
    ["LilianaVe55", "ByeGideon", "Liliana", "Vess", "whydoIhavean@email.com"]
]

for i in range(len(accrow)):
    print(str(accrow[i] + [0]))
    cursor.execute('INSERT into accounts (user_id, password, fname, lname, email, saved_payment) values (?,?,?,?,?,?)',
                   accrow[i] + [0])
    db.commit()
print("Account: DONE")

bookrow = [
    ["The New World", "James H.", "abc publish", 23.99, 3],
    ["Dear My Friend", "Mary Robinson", "CC books", 19.99, 5],
    ["Secrets Revealed", "Samantha Lee", "ML Publishing", 15.99, 2],
    ["The Last Goodbye", "James Harris", "JH Books", 12.99, 8],
    ["Forgotten Memories", "Sarah Williams", "SW Press", 9.99, 12],
    ["Lost in Translation", "Emily Chen", "EC Publishing", 16.99, 3],
    ["The Truth Within", "David Kim", "DK Books", 14.99, 6],
    ["Love and Lies", "Jennifer Lee", "JL Press", 11.99, 9],
    ["Unseen Forces", "Mark Johnson", "MJ Publishing", 18.99, 4],
    ["Breaking the Silence", "Grace Chen", "GC Books", 13.99, 7],
    ["The Missing Piece", "Ryan Wong", "RW Press", 10.99, 11],
    ["Behind Closed Doors", "Emma Taylor", "ET Publishing", 17.99, 3],
    ["A Journey Home", "Patrick Lee", "PL Books", 14.99, 6],
    ["Echoes of the Past", "Rachel Kim", "RK Press", 11.99, 9],
    ["Whispers in the Dark", "Melissa Chen", "MC Publishing", 16.99, 4],
    ["The Final Countdown", "Andrew Lee", "AL Books", 12.99, 8],
    ["Bridging the Gap", "Nicole Johnson", "NJ Press", 9.99, 12],
    ["The Road Less Traveled", "Daniel Kim", "DK Books", 18.99, 2],
    ["Pieces of Me", "Laura Smith", "LS Publishing", 15.99, 5],
    ["The Power of Forgiveness", "Kevin Lee", "KL Books", 11.99, 9],
    ["The Key to Happiness", "Emily Johnson", "EJ Press", 13.99, 7],
    ["A New Beginning", "Sarah Kim", "SK Publishing", 16.99, 4],
    ["The Art of Letting Go", "William Chen", "WC Books", 14.99, 6],
    ["The Weight of the World", "Samantha Smith", "SS Press", 12.99, 8],
    ["The Courage to Change", "Grace Lee", "GL Books", 11.99, 9],
    ["A Leap of Faith", "Michael Kim", "MK Publishing", 17.99, 3],
    ["Life Lessons", "Olivia Chen", "OC Books", 10.99, 11],
    ["The Journey Within", "Emily Davis", "ED Press", 15.99, 5],
    ["Chasing Dreams", "Justin Lee", "JL Books", 12.99, 8],
    ["Finding Your Voice", "Victoria Kim", "VK Publishing", 14.99, 6],
    ["A Second Chance", "Peter Lee", "PL Books", 16.99, 4],
    ["Happiness", "Sophia Chen", "SC Press", 13.99, 7],
]
for i in range(len(bookrow)):
    print(str(bookrow[i] + [0]))
    cursor.execute('INSERT into books (title, author, publisher, price, available,sold) values (?,?,?,?,?,?)',
                   bookrow[i] + [0])
    db.commit()
cursor.close()
print("Book: DONE")


