import sqlite3,datetime,csv

def connectDB(databaseName):
    print('CONNECTING TO DATABASE\n')
    mydb = sqlite3.connect(databaseName)
    return mydb,mydb.cursor()

def error_while(response):
  with open('exceptions.log','a+',encoding='utf-8') as raw:raw.write(f"Date: {datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}, Error: {response}\n")

def executecomm(cursor,comm,to_return=False,to_insert=False):
  print(comm)
  if to_insert == False:cursor.execute(comm)
  else:cursor.executemany(comm,to_insert)
  if to_return == True:return cursor.fetchall()

def endConnection(mydb):
  mydb.commit()
  mydb.close()


def exportDB():

  mydb,cursor = connectDB('userDatabase.db')
  raw_names = executecomm(cursor,f"PRAGMA table_info(users)",True)
  rows,names = [],[]
  for name in raw_names:
    names.append(name[1])
  rows.append(names)
  rows.extend(executecomm(cursor,f"SELECT * FROM users",True))
  users = '\n'.join([';'.join(r) for r in [[str(r) for r in row] for row in rows]])
  with open(f'users.csv', 'w', newline='',encoding = 'utf-8') as file:
    file.write(users)
  endConnection(mydb)
  return True



def addUsers(records):
  try:
    mydb,cursor = connectDB('userDatabase.db')
    for record in records:
      sql = f"""INSERT INTO users (name, phone, address, zipcode, city, website, email, path) VALUES ("{'", "'.join(record)}")"""
      executecomm(cursor,sql)
    endConnection(mydb)
    return True
  except Exception as exc:
    error_while(exc)
    return False

   