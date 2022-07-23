import api
import book_module
from getpass import getpass
import time
from IPython.display import clear_output
from IPython.display import Image
from IPython.display import display

class Start():
    def login(email):
        clear_output()
        password=getpass("Password: ")
        user = api.login_user(email, password) 
        print(user)
        time.sleep(3)
        return user

    def delete_account(user):
        api.delete_user(user['token'])
        time.sleep(4)

    def register():
        clear_output()
        print("Registration:")
        email = input("Email: ")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        password = input("Password: ")
        
        user_dict={
            "email":email,
            "first_name":first_name,
            "last_name":last_name,
            "password":password
        }
        return api.register_user(user_dict)

    def edit(user):
        prompt = input('What would you like to edit: first name, last name, or password?\n')
        if prompt == "first name":
            first = input('Enter your new first name: \n')
            edit_payload={
            "first_name":first,           
            }
            return api.edit_user(user['token'], edit_payload)            
            
        elif prompt == 'last name':
            last = input('Enter your new last name: \n')
            edit_payload={
            "last_name":last,           
            }
            return api.edit_user(user['token'], edit_payload)

        elif prompt == 'password':
            password = input('Enter your new password: \n')
            edit_payload={
            "password":password,           
            }            
            return api.edit_user(user['token'], edit_payload)

def main():
    reading_list = book_module.ReadingList()
    books = api.get_books()
    user = {}
    
    while True:
        clear_output()
        print("Welcome to the Bookstore")
        email = input("Type your email to login or Type `register` to Register ")
        if email == 'register':
            success_register=Start.register()
            if success_register:
                print(f"{user['first_name'].title()}, you have successfully registered")
                time.sleep(3)
                continue
            else:
                print("Failed to register")
                time.sleep(3)
        elif email.lower() == "quit":
            print(f"Goodbye {user['first_name'].title()}")
            break
        else:
            try:
                user = Start.login(email)
            except:
                print("Invalid Username/Password combo")
                time.sleep(2)
                continue
        # First Scene of our app (above)

        while True:
            clear_output()
            print("""
Welcome to the Repository            
You can:            
1. Browse All Books
2. Browse Book by Category
3. View Reading List
4. Remove Book From Reading List
5. Quit     
6. Delete user account
7. Edit User Account
""")
            command = input(f"Hello {user['first_name'].title()}, welcome to the bootstore. Select an option. ")
            if command == "1":
                book_module.browse_books(books, reading_list)
            elif command == "2":
                while True:
                    print(" | ".join(book_module.get_category_list(books)))
                    cat = input("Category: ").title()
                    if cat in book_module.get_category_list(books):
                        book_module.browse_books(books, reading_list, cat)
                        break
                    print("Invalid Category")
                    time.sleep(2)
                    continue
            elif command == "3":
                reading_list.show_book_list()
                input("Press Enter To Return")
                continue
            elif command == "4":
                while True:
                    clear_output()
                    reading_list.show_book_list()
                    garbage = input(f"Hello {user['first_name'].title()}, what book ID would you like to remove? [BACK to back out]")
                    if garbage.lower() == "back":
                        break
                    elif garbage.isnumeric() and int(garbage) in map(lambda book: book['id'], reading_list.reading_list):
                        reading_list.remove_book(list(filter(lambda book: book['id']==int(garbage), reading_list.reading_list))[0])
                        print(f'{garbage} has been removed')
                        time.sleep(2)
                        break
                    else:
                        print(f"{user['first_name'].title()}, {garbage} is not in your collection")
                        time.sleep(2)
                        break
                continue   
                    
            elif command == "5":
                print("Goodbye")
                break

            elif command == "6":
                prompt = input("Type 'delete' to delete your account.\n")
                if prompt == "delete":
                    prompt = input('Enter your email.\n')

                    if Start.delete_account(user):
                        print(f"Deleting account - goodbye, {user['first_name'].title()}!")
                    else:
                        print('Try again, fool.')
                    break
                else:
                    print('Glad you changed your mind.')

            elif command == "7":
                if Start.edit(user):
                    print('Name change successful.')
                    time.sleep(2)
                else:
                    print('You suck, try again.')
                    time.sleep(2)
                continue
            else:
                print("Invalid Selection")
                time.sleep(2)
                continue
        break        

main()            