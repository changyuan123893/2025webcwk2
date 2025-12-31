import sqlite3
import os

DB = os.path.join(os.path.dirname(__file__), 'instance', 'site.db')


def main():
    if not os.path.exists(DB):
        print('The database does not exist:', DB)
        return
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT id, title, year, director FROM movie "
                "WHERE title LIKE 'movie_example%' ORDER BY id")
    rows = cur.fetchall()
    print('COUNT=' + str(len(rows)))
    for r in rows:
        print(r[0], r[1], r[2], r[3])
    conn.close()


if __name__ == '__main__':
    main()
