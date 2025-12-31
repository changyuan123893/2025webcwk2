import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'site.db')


def main():
    if not os.path.exists(DB_PATH):
        print(f"The database file does not exist.: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, title, year, director FROM movie ORDER BY id")
        rows = cur.fetchall()
        print('COUNT=' + str(len(rows)))
        for r in rows:
            print(f"{r[0]}||{r[1]}||{r[2]}||{r[3]}")
    except Exception as e:
        print('Query error:', e)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
