import sqlite3 

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        #print(sqlite3.version)
    except sqlite3.Error as e:
        print('create_connection: ', e)

    return conn

def get_cursor(conn):
    return conn.cursor()

def create_news_table(conn):
    success = conn.execute('CREATE TABLE news_article(datetime TEXT, article_title TEXT, media_name TEXT, article_url TEXT, article_body TEXT, article_author TEXT)') 

    #if success:
    #    print('News table created!')

def create_urls_table(conn):
    success = conn.execute('CREATE TABLE news_url(article_url TEXT, media_name TEXT)')
    #if success:
    #    print('Url Table created!')

def select_news_table(cursor):
    cursor.execute('SELECT * from news_article')
    rows = cursor.fetchall()
    return rows