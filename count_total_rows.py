
import db_helper
import glob

db_files = glob.glob('./db/real_estate/news_article*.db')
db_files = sorted(db_files)
total_rows = 0
for i, db_file in enumerate(db_files):
    conn = db_helper.create_connection(db_file)

    cursor = db_helper.get_cursor(conn)

    rows = db_helper.select_news_table(cursor)
    
    total_rows += len(rows)

    if conn:
        conn.close()

print('total rows: ', total_rows)
