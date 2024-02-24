from functions import (get_products, search_product, having_product, single_product, table_print, add_new_product,
                       import_product, get_statistics)


while True:
    print('1. Get all products\n'
          '2. Search product\n'
          '3. Add new product\n'
          '4. Import products\n'
          '5. Statistics\n'
          '6. Back')

    ans = input('Select: ')

    if ans == '1':
        get_products()
        if len(having_product()) != 0:
            ans1 = int(input("Select ID: "))
            single_product(ans1)

    if ans == '2':
        search = input('Enter name: ')
        table_print(search_product(search))
        if len(search_product(search)) != 0:
            ans2 = int(input("Select ID: "))
            single_product(ans2)

    if ans == '3':
        add_new_product()
    if ans == '4':
        ans4 = int(input("Product ID: "))
        pr_count = int(input('Count: '))
        import_product(ans4, pr_count)
    if ans == '5':
        get_statistics()
    if ans == '6':
        break


