import psycopg2

connect = psycopg2.connect(dbname='notebook', user='postgres', password='Qc305iy7*!', host='localhost')


def create():
    create_table = '''CREATE TABLE users (name VARCHAR(100) NOT NULL, phone VARCHAR(20) NOT NULL, email VARCHAR(50) NULL, id SERIAL PRIMARY KEY)'''
    cursor = connect.cursor()
    cursor.execute(create_table)
    cursor.close()
    connect.commit()


def add_something(name, phone, email):
    cursor = connect.cursor()
    insert = '''INSERT INTO users (name, phone, email) VALUES ('{}','{}','{}')'''.format(name, phone, email)
    cursor.execute(insert)
    connect.commit()


def select_all(table_name):
    cursor = connect.cursor()
    select = '''SELECT * FROM {} ORDER BY favourites, name'''.format(table_name)
    cursor.execute(select)
    return cursor.fetchall()


def update_record(id, **kwargs):
    cursor = connect.cursor()
    update = '''UPDATE users SET {} WHERE id='{}' '''.format(','.join([f"{k}='{v}'" for k, v in kwargs.items()]), id)
    cursor.execute(update)
    connect.commit()


def sort(field, fields):
    cursor = connect.cursor()
    select = '''SELECT * FROM users ORDER BY {} {} '''.format(field, fields)
    cursor.execute(select)
    return cursor.fetchall()


def print_select(field=None, fields=None):
    if field is not None:
        rows = sort(field, fields)
    else:
        rows = select_all('users')
    for i in rows:
        print(i)


def main():
    while True:
        ask = input("Выбор действия: \n1) Показать все\n2) Добавить контакт\n3) Редактировать пользователя\n4)Сортировка по полю\n"
                    "5)Добавить контакт в избранное\n6)Удалить контакт из избранного\n")
        if ask == '1':
            print_select()
        elif ask == '2':
            name = input("Имя: ")
            phone = input("Телефон: ")
            email = input("Email: ")
            add_something(name, phone, email)
        elif ask == '3':
            contact = {}
            id = input('ID: ')
            name = input("Имя: ")
            phone = input("Телефон: ")
            email = input("Email: ")
            if len(name) > 0:
                contact["name"] = name
            if len(phone) > 0:
                contact["phone"] = phone
            if len(email) > 0:
                contact["email"] = email
            else:
                print('Вы ввели ')
            update_record(id, **contact)
        elif ask == '4':
            sort = input('Sort field: ')
            fields = input('Fields: ASC or DESC ')
            print_select(sort, fields)
        elif ask == '5':
            fav = input('ВВедите ID: ')
            update_record(fav, favourites=True)
        elif ask == '6':
            remove = input('ВВедите ID: ')
            update_record(remove, favourites=False)


main()
