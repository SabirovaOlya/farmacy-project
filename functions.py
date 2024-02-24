import psycopg2
import tabulate
from database import db_connection
from datetime import datetime


def get_current_date():
    current_date_time = datetime.now()
    formatted_date = current_date_time.strftime("%Y-%m-%d")
    return formatted_date


def table_print(array: list):
    if len(array) == 0:
        print('No product')
    else:
        header = ('ID', 'name', 'price', 'description', 'country', 'created_date', 'expiration_date', 'count')
        table = tabulate.tabulate(array, headers=header, tablefmt='grid')
        print(table)


def st_print(array: list):
    if len(array) == 0:
        print('No product')
    else:
        header = ('Product name', 'count')
        table = tabulate.tabulate(array, headers=header, tablefmt='grid')
        print(table)


def having_product():
    try:
        conn = db_connection()
        cur = conn.cursor()
        query = '''
                select p.id, p.name, p.price, p.description, p.country, p.created_date, p.expiration_date, s.count from product p
                inner join stock s on s.product_id = p.id
                where p.expiration_date > current_date and s.count > 0;
            '''
        cur.execute(query)
        result = cur.fetchall()
        return result
    except(Exception, psycopg2.Error) as error:
        return []


def get_products():
    try:
        conn = db_connection()
        cur = conn.cursor()
        query = '''
                select p.id, p.name, p.price, p.description, p.country, p.created_date, p.expiration_date, s.count from product p
                inner join stock s on s.product_id = p.id
                where p.expiration_date > current_date and s.count > 0
                order by p.id;
            '''
        cur.execute(query)
        result = cur.fetchall()
        table_print(result)
    except(Exception, psycopg2.Error) as error:
        print(error)


def search_product(name):
    try:
        conn = db_connection()
        cur = conn.cursor()
        query = '''
                    SELECT p.id, p.name, p.price, p.description, p.country, p.created_date, p.expiration_date, s.count 
                    FROM product p
                    INNER JOIN stock s ON s.product_id = p.id
                    WHERE p.name LIKE %(name)s AND p.expiration_date > current_date AND s.count > 0
                    order by p.id;
                    '''
        cur.execute(query, {'name': f'%{name}%'})
        result = cur.fetchall()
        return result
    except(Exception, psycopg2.Error) as error:
        print(error)


def find_product(id):
    try:
        conn = db_connection()
        cur = conn.cursor()
        query = '''
                select p.id, p.name, p.price, p.description, p.country, p.created_date, p.expiration_date, s.count from product p
                inner join stock s on s.product_id = p.id
                where p.id = %(id)s and s.count > 0 and p.expiration_date > current_date
            '''
        cur.execute(query, {'id': id})
        result = cur.fetchall()
        return result
    except(Exception, psycopg2.Error) as error:
        print(error)


def buy_product(product_id, count):
    try:
        conn = db_connection()
        cur = conn.cursor()
        queue = '''
                    insert into orders(product_id, count, date) values(%s, %s, %s)
                '''
        cur_date = get_current_date()
        values = (product_id, count, cur_date)
        cur.execute(queue, values)
        conn.commit()
        print('Successfully saled\n')
    except(Exception, psycopg2.Error) as error:
        print(error)


def edit_product(product_id):
    name = input('Enter name: ')
    price = float(input('Enter price: '))
    description = input('Enter description: ')
    country = input('Enter country: ')
    created_date = input('Enter created_date(yyyy-mm-dd): ')
    expiration_date = input('Enter expiration_date(yyyy-mm-dd): ')

    try:
        conn = db_connection()
        cur = conn.cursor()
        queue = '''
                    update product set name = %s, price = %s,  description = %s, country = %s, created_date = %s, 
                    expiration_date = %s where id = %s
                '''
        values = (name, price, description, country, created_date, expiration_date, product_id)
        cur.execute(queue, values)
        conn.commit()
        print('Successfully edited\n')
    except(Exception, psycopg2.Error) as error:
        print(error)


def add_new_product():
    name = input('Enter name: ')
    price = float(input('Enter price: '))
    description = input('Enter description: ')
    country = input('Enter country: ')
    created_date = input('Enter created_date(yyyy-mm-dd): ')
    expiration_date = input('Enter expiration_date(yyyy-mm-dd): ')

    try:
        conn = db_connection()
        cur = conn.cursor()
        queue = '''
                    insert into product(name, price, description, country, created_date, expiration_date) values(%s, %s, %s, %s, %s, %s)
                '''
        values = (name, price, description, country, created_date, expiration_date,)
        cur.execute(queue, values)
        conn.commit()
        print('Successfully added\n')
    except(Exception, psycopg2.Error) as error:
        print(error)


def import_product(product_id, count):
    try:
        conn = db_connection()
        cur = conn.cursor()
        queue = '''
                    insert into imports(product_id, count, date) values(%s, %s, %s)
                '''
        cur_date = get_current_date()
        values = (product_id, count, cur_date)
        cur.execute(queue, values)
        conn.commit()
        print('Successfully added\n')
    except(Exception, psycopg2.Error) as error:
        print(error)


def delete_product(product_id):
    conn = db_connection()
    cur = conn.cursor()
    queue = '''
                update stock set count = 0 where product_id = %s
            '''
    cur.execute(queue, {'product_id': product_id})
    conn.commit()
    print('Deleted \n')


def single_product(id):
    if not find_product(id):
        print('There no such product\n')
    else:
        select_product = find_product(id)
        print('---------------------- Product -----------------\n')
        table_print(select_product)
        print('\n1. Buy product\n'
              '2. Edit product\n'
              '3. Delete product\n')

        ans = input("Select: ")
        if ans == '1':
            product_count = int(input('Enter count: '))
            buy_product(select_product[0][0], product_count)
        if ans == '2':
            edit_product(select_product[0][0])
        if ans == '3':
            delete_product(select_product[0][0])


def get_statistics():
    try:
        conn = db_connection()
        cur = conn.cursor()
        query = '''
                select p.name, count(*) from product p
                inner join orders o on o.product_id = p.id
                group by p.name;
            '''
        cur.execute(query)
        result = cur.fetchall()
        print('Sold product')
        st_print(result)
    except(Exception, psycopg2.Error) as error:
        print(error)
    print()

    try:
        conn = db_connection()
        cur = conn.cursor()
        query = '''
                select p.name, count(*) from product p
                inner join imports i on i.product_id = p.id
                group by p.name;
            '''
        cur.execute(query)
        result = cur.fetchall()
        print('Imported product')
        st_print(result)
    except(Exception, psycopg2.Error) as error:
        print(error)

    print()
