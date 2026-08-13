import db
from models import Product

def view_products():
    products = db.get_all_products()

    for product in products:
        print(product)

def add_product():

    name = input("Enter product name: >  ")
    category = input("Enter product category: >  ")

    while True:
        try:
            quantity = int(input("Enter product quantity: >  "))
            break
        except ValueError:
            print("Quantity must be a number.. Try again")

    while True:            
        try:
            reorder_level = int(input("Enter product reorder_level: >  "))
            break
        except ValueError:
            print("reorder_level must be a number.. Try again")

    while True:                   
        try:
            unit_price = int(input("Enter product unit_price (enter in pence): >  "))
            break
        except ValueError:
            print("unit_price must be a number.. Try again")           

    new_product = Product(name, category, quantity, reorder_level, unit_price, None)

    check_correct = input(
f"""
Please check details of product are correct:
{new_product}
Continue to add product? (y/n): >   
""").strip().lower()

    while True:
        if check_correct == "y":
            db.add_item(new_product)
            print("Product added")
            break
        elif check_correct== "n":
            print("Returning to menu")
            break
        else:
            check_correct = input("invalid input detected, please enter ""y"" or ""n"": >   ").strip().lower()
            
def update_product():

    while True:
        product_to_update = input(
            'Please enter product ID to update or type "view" '
            'to see the list of products and their IDs: >  '
        )

        if product_to_update.strip().lower() == "view":
            view_products()
            continue

        product = db.get_one_product(product_to_update)

        if product is None:
            print("No valid product selected")
            continue
        
        field_types = {
            "category":str,
            "name":str,
            "reorder_level":int,
            "unit_price":int
        }
        while True:
            column_to_update = input(
                "Please state the column to update: >   "
            ).strip().lower()
            try:
                value_type = field_types[column_to_update]
                break
            except KeyError:
                print("Available columns = category, name, reorder_level, unit_price..Please try again.")
                continue

        confirm = input(
            f"Editing {column_to_update} on item ID:{product_to_update}, "
            "continue (y/n)? >   "
        )

        if confirm.strip().lower() == "y":
            while True:
                try:
                    new_value = value_type(input("Please input new value: >  "))
                    break
                except ValueError:
                    print("If editing category or name then value should be string.\n If editing reorder_level or unit_price then value should be integer.")

            try:
                db.update_column(product, column_to_update, new_value)
                print("Product updated.")
                break
            except ValueError as error:
                print(error)
                continue

        else:
            continue

def delete_product():

    while True:
        product_to_delete = input("Please enter product ID to delete or type ""view"" to see the list of products and their IDs: >  ").strip().lower()

        if product_to_delete == "view":
            view_products()
            continue

        product = db.get_one_product(product_to_delete)

        if product is None:
            print("No valid product selected")
            continue
                
        confirm = input(f"Are you sure you wish to delete product with item ID:{product_to_delete}, continue (y/n)? >   ").strip().lower()
        if confirm == 'y':
            db.del_item(product)
            print("Product deleted.")
            break
        else:
            continue

def low_stock_report():

    zero_stock_items = []
    very_lowstock_items =[]
    all_other_lowstock_items = []

    products = db.get_lowstock_products()

    if not products:
        print("No low stock products! \nReturning to menu..")
        return

    for product in products:
        if product.quantity == 0:
            zero_stock_items.append(product)
            continue
        if (product.quantity / product.reorder_level) < 0.35:
            very_lowstock_items.append(product)
            continue
        else:
            all_other_lowstock_items.append(product)

    print("""
------------------------------
    Low Stock Report
------------------------------
ALERT! PRODUCTS WITH 0 STOCK:
    """)

    for product in zero_stock_items:
        print(f"{product} \n")

    print("------------------------------")

    print("Caution! VERY LOW STOCK PRODUCTS:\n")
    for product in very_lowstock_items:
        print(f"{product} \n")

    print("------------------------------")

    print("OTHER LOW STOCK PRODUCTS:\n")
    for product in all_other_lowstock_items:
        print(f"{product} \n")

    print("""
------------------------------
    END OF REPORT
------------------------------
    """)
    
def add_subtract_stock():
    while True:

        choose_product = input("Please enter product ID to change stock level of or type ""view"" to see the list of products and their IDs: >  ").strip().lower()

        if choose_product == "view":
            view_products()
            continue
        
        product = db.get_one_product(choose_product)

        if product is None:
            print("No valid product selected")
            continue

        while True:            
            try:
                quantity_to_move = int(input("Please enter the number of items you wish to add or remove. A negative number will remove stock: >   "))
                break
            except ValueError:
                print("value must be a number.. Try again")

        
        try:
            db.stock_movement(product, quantity_to_move)
            break
        except ValueError as error:
            print(error)
            while True:
                check_continue = input("Would you like to try again? (y/n) >  ").strip().lower()
                if check_continue == "y":
                    break
                elif check_continue== "n":
                    print("Returning to menu")
                    return
                else:
                    print("invalid input detected, please enter ""y"" or ""n"" ")
            
def main():
    db.create_table()

    while True:

        print("""
-------------------------
FOX PRODUCTS DATABASE
-------------------------
1. VIEW PRODUCTS
2. ADD PRODUCT
3. UPDATE PRODUCT
4. DELETE PRODUCT
5. STOCK MOVEMENT
6. LOW STOCK REPORT
7. QUIT
    """)

        choice = input(">  ")

        if choice == "1":
            view_products()
        elif choice == "2":
            add_product()
        elif choice == "3":
            update_product()
        elif choice == "4":
            delete_product()
        elif choice == "5":
            add_subtract_stock()
        elif choice == "6":
            low_stock_report()
        elif choice == "7":
            print(
                """
---------------------------------------
Closing Fox Inventory.... Thank you.
---------------------------------------"""
            )
            break
        else:
            print("Invalid option detected")
            continue
    
if __name__ == "__main__":
    main()






