
import db_helper
import glob

db_files = glob.glob('./db/real_estate/news_article*.db')
db_files = sorted(db_files)
total_rows = 0
for i, db_file in enumerate(db_files):
    conn = db_helper.create_connection(db_file)

    cursor = db_helper.get_cursor(conn)

    if i == 0:
        cursor.execute('SELECT * from news_article')
        names = list(map(lambda x: x[0], cursor.description))
        print(names)
    cursor.execute('SELECT article_url, article_body from news_article')
    rows = cursor.fetchall()
    for row in rows:
        contents = row[1]
        if '갭투자' in contents:
            print(db_files)

    #rows = db_helper.select_news_table(cur)
    #for row in rows:
    #    print(row)
    
    total_rows += len(rows)

    if conn:
        conn.close()

print('total rows: ', total_rows)
