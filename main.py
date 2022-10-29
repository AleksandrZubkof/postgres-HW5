import psycopg2


def create_table(conn):
    cur.execute("""
        DROP TABLE phone;
        DROP TABLE client;
        """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(60) NOT NULL,
        last_name VARCHAR(60) NOT NULL,
        email VARCHAR(60));
        """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phone(
        id SERIAL PRIMARY KEY,
        number VARCHAR(20) UNIQUE,
        client_id integer references client(id));
        """)

    return conn.commit()


def add_client(conn, name, surname, email, number_phone=None):
    cur.execute("""
        INSERT INTO client(first_name, last_name, email) 
        VALUES(%s, %s, %s) RETURNING id, first_name""", (name, surname, email))
    print(cur.fetchone())

    if number_phone !=None:
        cur.execute("""
            INSERT INTO phone(number) VALUES(%s, %s) RETURNING id, number""", (number_phone,))
        print(cur.fetchone())


def add_phone(conn, client_id, phone):
    cur.execute("""
        INSERT INTO phone(client_id, number) 
        VALUES(%s, %s) RETURNING client_id, number""", (client_id, phone))
    print(cur.fetchone())


def change_client(conn):
    client_id = input("Введите ID клиента: ")
    first_name = input("Введите новое имя : ")
    last_name = input("Введите новую фамилию : ")
    email = input("Введите новый e-mail : ")

    cur.execute("""
            UPDATE client SET first_name=%s, last_name=%s, email=%s WHERE id=%s;
            """, (first_name, last_name, email, client_id))
    cur.execute("""
            SELECT * FROM client;
            """)
    print(cur.fetchall())


def delete_phone(conn, client_id):
    cur.execute("""
            DELETE FROM phone WHERE client_id=%s;
            """, (client_id,))
    cur.execute("""
            SELECT * FROM phone;
            """)
    print(cur.fetchall())

def delete_client(conn, client_id):
    cur.execute("""
                DELETE FROM phone WHERE client_id=%s;
                """, (client_id,))
    cur.execute("""
                SELECT * FROM phone;
                """)
    print(cur.fetchall())

    cur.execute(""" 
        DELETE FROM client WHERE id=%s;""", (client_id,))

    cur.execute("""
        SELECT * FROM client;
            """)
    print(cur.fetchall())


def find_client(conn):
    find = input('Выберите параметр поиска \n (1 - Имя), (2 - Фамилия), (3 - E-mail), (4 - номер телефона):')
    if find == '1':
        find_name = input('Введите имя: ')
        cur.execute("""
            SELECT c.id, first_name, last_name, email, p.number FROM client c
            FULL JOIN phone p ON c.id = p.client_id
            WHERE UPPER(c.first_name) = %s;""", (find_name.upper(),))
        print(cur.fetchall())

    elif find == '2':
        find_surname = input('Введите фамилию: ')
        cur.execute("""
                    SELECT c.id, first_name, last_name, email, p.number FROM client c
                    FULL JOIN phone p ON c.id = p.client_id
                    WHERE UPPER(c.last_name) = %s;""", (find_surname.upper(),))
        print(cur.fetchall())

    elif find == '3':
        find_email = input('Введите электронную почту: ')
        cur.execute("""
                    SELECT c.id, first_name, last_name, email, p.number FROM client c
                    FULL JOIN phone p ON c.id = p.client_id
                    WHERE UPPER(c.email) = %s;""", (find_email.upper(),))
        print(cur.fetchall())

    elif find == '4':
        find_number = input('Введите номер телефона: ')
        cur.execute("""
                    SELECT c.id, first_name, last_name, email, p.number FROM client c
                    FULL JOIN phone p ON c.id = p.client_id
                    WHERE p.number = %s;""", (find_number,))
        print(cur.fetchall())

with psycopg2.connect(database="HW5", user="postgres", password="132465798") as conn:
    with conn.cursor() as cur:
        # create_table(conn)
        # add_client(conn, 'Ivan', 'Ivanov', 'ii@ya.ru')
        # add_phone(conn, 5, 89211234)
        # change_client(conn)
        # delete_phone(conn, 3)
        # delete_client(conn, 5)
        find_client(conn)
conn.close()
