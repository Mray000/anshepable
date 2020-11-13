import requests
import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup


def create_connection(db_file):
    """ 
        create a database connection to the SQLite database
        specified by db_file
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def collect_data(url, name, con):
  '''
    sending https request to take away data from http server
    specified by name of href, name of text and db connection
  '''
  print(f"Collecting {name.lower()} dictionary...")

  try: 
  
    r = requests.get(url)

    soup = BeautifulSoup(r.text, features="html.parser")

    data = list(map(lambda x: x.text,
      soup.find_all('td', {'class': 'text'}))) 

    cur = con.cursor()

    for item in data:
      cur.execute(""" INSERT INTO texts (text, type)
        VALUES (?, ?)""", (item, name,))

    con.commit()
  
    print(f"{name.title()} collected!")

  except Exception as e:
    print("Load failed with exception: ")
    print(e)



def download(dictionaries, con):
  '''
    sending requensts from dictionaries
  '''
  for d in dictionaries:
    collect_data(d['url'], d['name'], con)


def db_creation(con):
  '''
    creation our own database
  '''
  cur = con.cursor()
  cur.execute("""CREATE TABLE texts (
        id   INTEGER PRIMARY KEY AUTOINCREMENT
                    UNIQUE
                    NOT NULL,
        text TEXT,
        type STRING
    );
    """)
  con.commit()
  

def test_connection(con):
  '''
    take away our data from db
  '''
  cur = con.cursor()
  res = cur.execute("""SELECT * FROM texts""").fetchall()
  for item in res:
    print(item)


def clear_base(con):
  '''
    clearing our base after testing connection and other things
  '''
  cur = con.cursor()
  res = cur.execute("""DELETE FROM texts""")  
  con.commit()


def main():
  '''
    main interface
  '''
  database_name = 'db.sqlite'

  connection = sqlite3.connect(database_name)

  with connection as con:

    DICTIONARIES = [
      {'url': 'https://klavogonki.ru/vocs/12726/', 'name': 'basic russian'},
      {'url': 'https://klavogonki.ru/vocs/120759/', 'name': 'hard russian'},
      {'url': 'https://klavogonki.ru/vocs/6018/',  'name': 'long russian'},
      {'url': 'https://klavogonki.ru/vocs/5539/', 'name': 'basic english'},
      {'url': 'https://klavogonki.ru/vocs/8835/', 'name': 'long english'},
      {'url': 'https://klavogonki.ru/vocs/62238/', 'name':  'numbers'},
    ] 
    
    # db_creation(con)
    # clear_base(con)

    download(DICTIONARIES, con)

    # test_connection(con)



if __name__ == "__main__":
  main()
