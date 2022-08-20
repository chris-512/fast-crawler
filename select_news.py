
import db_helper
import glob

db_files = glob.glob('./db/news_article*.db')
total_rows = 0
for db_file in db_files:
    conn = db_helper.create_connection(db_file)

    cur = db_helper.get_cursor(conn)

    rows = db_helper.select_news_table(cur)
    #for row in rows:
    #    print(row)
    total_rows += len(rows)

    if conn:
        conn.close()

print(total_rows)