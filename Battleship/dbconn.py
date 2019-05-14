def get_user(conn, user: str) -> tuple:
    cur = conn.cursor()
    return cur.execute("SELECT * FROM users WHERE nama =?", (user, )).fetchone()

def get_highscore(conn) -> list:
    hi = []
    for skor in conn.cursor().execute("SELECT * FROM score ORDER BY score ASC LIMIT 10").fetchall():
        hi += [skor]
    return hi

def register(conn, user: str, passowrd: str) -> bool:
    cur = conn.cursor()
    # check for user
    if cur.execute("SELECT * FROM users WHERE nama = ?", (user, )).fetchone():
        return False

    # register user
    cur.execute("INSERT INTO users VALUES(?, ?)", (user, passowrd,))
    conn.commit()

    return True

def newscore(conn, user: str, score: int) -> bool:
    cur = conn.cursor()
    cur.execute("INSERT INTO score VALUES(?, ?)", (user, score))
    conn.commit()

    return True
