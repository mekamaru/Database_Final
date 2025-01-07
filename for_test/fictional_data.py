#add fictional books and accounts data examples on bookstore.db for test
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

    ["StormStorm", "ThunderCrush", "Evan", "Storm", "evan.storm@stormmail.com"],
    ["CrystalStone", "GlowGem", "Sierra", "Bright", "sierra.bright@crystalmail.com"],
    ["BlazeComet", "FireTrail", "Henry", "Nova", "henry.nova@blazemail.com"]
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
    ["The Journey Within", "Emily Davis", "ED Press", 15.99, 5],
    ["Chasing Dreams", "Justin Lee", "JL Books", 12.99, 8],
    ["Finding Your Voice", "Victoria Kim", "VK Publishing", 14.99, 6],
    ["A Second Chance", "Peter Lee", "PL Books", 16.99, 4],
    ["Happiness", "Sophia Chen", "SC Press", 13.99, 7],
    ["Whispers of the Past", "Mark Harris", "Moonlit Publishing", 18.50, 10],
    ["Into the Unknown", "Olivia Carter", "Blue Sky Editions", 11.75, 3],
    ["The Last Horizon", "Jameson Blake", "Harbor Books", 19.00, 12],
    ["Shadows of the Future", "Lily Adams", "Urban Reads", 9.99, 2],
    ["Echoes of Silence", "Mason Roberts", "Sunshine Media", 17.25, 6],
    ["A Path to Peace", "Rachel Turner", "Golden Leaf Press", 20.00, 15],
    ["Beneath the Stars", "Aiden Scott", "Silver Wave Books", 14.50, 4],
    ["Waves of Change", "Ella Wright", "Evergreen Publications", 13.75, 8],
    ["A Moment in Time", "Isaac Moore", "Skyline Media", 15.99, 7],
    ["The Road Ahead", "Grace Bennett", "Twilight House", 16.25, 9],
    ["Timeless Wisdom", "Liam Williams", "Dreamcatcher Publishing", 17.99, 6],
    ["Fragments of Hope", "Amelia Clark", "Windswept Books", 14.99, 5],
    ["Beyond the Clouds", "Ethan Harris", "Autumn Leaf Press", 12.00, 4],
    ["The Power of Now", "Charlotte Mitchell", "Royal Reads", 18.99, 7],
    ["Shifting Realities", "Benjamin King", "Echo Publishing", 13.25, 10],
    ["In Search of Truth", "Mia Roberts", "Blue Horizon Books", 11.50, 6],
    ["The Hidden Path", "John Wilson", "Mystic Books", 19.99, 9],
    ["Chasing the Dream", "Oliver Smith", "Open Sky Publishing", 14.25, 4],
    ["Under the Moonlight", "Lily Davis", "Riverstone Press", 16.75, 3],
    ["A New Beginning", "Zoe Anderson", "Eclipse Publications", 17.50, 8],
    ["The Infinite Journey", "Max Brown", "Horizon Books", 18.25, 5],
    ["Rising Stars", "Laura Green", "Sundown Publishing", 13.50, 6],
    ["Silent Night", "Amos Carter", "Dreamtide Press", 16.00, 11],
    ["The Last Sunset", "Victoria Stone", "Moonshine Books", 15.75, 4],
    ["Into the Light", "Eva Clark", "Falling Star Publishing", 10.99, 7],
    ["Journey to the Top", "Nathan Walker", "Golden Key Press", 12.49, 8],
    ["Legacy of the Brave", "Oscar Knight", "Bronze Gate Press", 14.75, 6],
    ["Awakening the Soul", "Leah White", "Riverside Books", 18.99, 2],
    ["The Quest for Truth", "Peter Lang", "Crossroads Publishing", 17.00, 5],
    ["Stories of the Lost", "Tara Smith", "Timeless Press", 11.99, 7],
    ["The Final Chapter", "Ian Young", "Writers Guild Publishing", 13.99, 9],
    ["Endless Horizons", "Rachel Black", "Skyward Books", 16.50, 6],
    ["Secrets of the Sea", "George Miller", "Oceanside Press", 12.75, 8],
    ["Whispers in the Wind", "Lucy Brown", "Twilight Press", 14.25, 5],
    ["Pathways to the Stars", "Hannah Jones", "Starfield Publishing", 15.50, 10],
    ["Awakening", "Megan Lee", "Dawnlight Publishing", 17.75, 3],
    ["Echoes of Eternity", "Paul Turner", "Moonbeam Books", 19.49, 12],
    ["Beneath the Surface", "Naomi Davis", "Sunset Books", 13.50, 8],
    ["The Unspoken Truth", "Zachary Moore", "Starfire Press", 14.99, 4],
    ["The Fire Within", "Lara Greene", "Bright Horizon Press", 18.99, 6],
    ["Voices from the Past", "Jason Clark", "Silverstone Publishing", 16.75, 3],
    ["Whispers of the Future", "Madeline Lee", "Clearview Press", 15.99, 5],
    ["Steps to Freedom", "Chris Allen", "Sunshine Books", 14.50, 7],
    ["The Edge of Tomorrow", "Jasmine Carter", "New World Press", 17.00, 6],
    ["Breaking Boundaries", "James White", "Ironwood Publishing", 18.25, 9],
    ["The Silent Witness", "Oliver Clark", "Mystic Horizon", 16.99, 3],
    ["Shifting Sands", "Isabelle Walker", "Windmill Press", 12.99, 6],
    ["The Forgotten Story", "Diana Smith", "Redwood Press", 13.50, 8],
    ["Uncharted Paths", "Maxwell Hill", "Northstar Books", 17.99, 7],
    ["Love in the Time of Change", "Sophie King", "Dreamworld Press", 19.25, 4],
    ["The Forgotten Truth", "Benjamin Clark", "Clearstream Books", 18.50, 9],
    ["Voices in the Dark", "Oliver Gray", "Crescent Moon Publishing", 11.99, 5],
    ["The Sky's the Limit", "Katherine West", "Horizon Press", 14.75, 3],
    ["Chasing Shadows", "Ella Fisher", "Lightstone Publishing", 17.00, 10],
    ["The Silent Echo", "Brian Adams", "Stonebridge Press", 15.25, 6],
    ["A World Beyond", "Tessa Green", "Blue Valley Publishing", 18.99, 7],
    ["Unspoken Words", "Isaiah Brown", "Greenleaf Press", 16.50, 8],
    ["Rebirth of a Dream", "Megan Johnson", "Eclipse Publishing", 13.75, 5],
    ["Starlit Paths", "Isaac Williams", "Golden Gate Press", 17.25, 6],
    ["The Final Horizon", "Aiden White", "Lighthouse Books", 14.99, 8],
    ["Shadows and Light", "Leah Harris", "Northern Lights Press", 15.50, 4],
    ["The Lost City", "Lucas Clark", "Blue Ocean Publishing", 19.99, 2],
    ["The Call of Adventure", "Lily King", "Sunrise Books", 18.00, 10],
    ["Waves of Time", "Evan Lee", "Blue Sky Publishing", 12.50, 3],
    ["A New Dawn", "Isabella Adams", "Evergreen Books", 14.25, 5],
    ["Through the Storm", "Jacob Moore", "Morning Star Press", 16.99, 7],
    ["The Shadow of the Moon", "Riley White", "Winterfell Books", 15.00, 8],
    ["Hearts of Steel", "Scarlett Jones", "Steelbridge Publishing", 13.00, 6],
    ["Beyond the Sea", "Finn Turner", "Silverline Press", 14.50, 7],
    ["Destiny's Path", "Grace Morgan", "Harborview Press", 16.25, 4],
    ["In the Blink of an Eye", "Sophia Lee", "Firstlight Books", 13.99, 6],
    ["The Final Awakening", "Logan Green", "Horizon Press", 15.75, 5],
    ["Voices of the Earth", "Amelia Lee", "Wildwood Press", 12.25, 8],
    ["Living the Dream", "Daniel White", "Skyview Publishing", 17.00, 3],
    ["The Secret of the Stars", "Abigail Scott", "Brightside Press", 14.99, 9],
    ["Through the Fire", "Charles Harris", "Redstone Publishing", 18.99, 6],
    ["The Heart of the Ocean", "Sophie Bennett", "Crestview Press", 16.75, 7],
    ["Into the Night", "Daniela King", "Mooncrest Press", 17.50, 5],
    ["The Voice of the Wind", "Luke Adams", "Golden Horizons", 18.99, 6],
    ["Storms of the Heart", "Jackie Williams", "Clearwater Press", 15.99, 8],
    ["The Colors of the Sky", "Hannah Scott", "Blue Moon Press", 13.25, 7],
    ["The Memory Keeper", "Benjamin Davis", "Whisperwind Books", 16.50, 9],
    ["Chasing Dreams", "Madeline Brown", "Oceanview Books", 12.99, 10],
    ["The Edge of Eternity", "Ava Miller", "Northfield Press", 17.25, 6],
    ["Between the Lines", "William Lee", "Ocean Breeze Publishing", 18.50, 5],
    ["Unwritten Stories", "Oliver Brown", "Moonlit Nights Press", 14.75, 6],
]
for i in range(len(bookrow)):
    print(str(bookrow[i] + [0]))
    cursor.execute('INSERT into books (title, author, publisher, price, available,sold) values (?,?,?,?,?,?)',
                   bookrow[i] + [0])
    db.commit()
cursor.close()
print("Book: DONE")


