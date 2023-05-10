import databaseManager as dM

def tables():
    mydb, cursor = dM.connectDB('userDatabase.db')

    sql = f'''CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone VARCHAR(20),
        address VARCHAR(255),
        zipcode VARCHAR(10),
        city VARCHAR(100),
        website VARCHAR(255),
        email VARCHAR(255),
        path VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );'''

    try:cursor.execute(sql)
    except:pass

    mydb.commit()
    mydb.close()

tables()