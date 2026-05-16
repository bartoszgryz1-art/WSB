
books_data = [
    {"title": "Władca Pierścieni", "author": "J.R.R. Tolkien", "quantity": 3},
    {"title": "Hobbit", "author": "J.R.R. Tolkien", "quantity": 1},
    {"title": "Diuna", "author": "Frank Herbert", "quantity": 2},
    {"title": "Solaris", "author": "Stanisław Lem", "quantity": 0},
    {"title": "Cyberiada", "author": "Stanisław Lem", "quantity": 5}
]

users_data = [
    {"username": "janek", "password": "123", "role": "czytelnik", "borrowed": []},
    {"username": "ania", "password": "qwe", "role": "czytelnik", "borrowed": []},
    {"username": "piotr", "password": "zxc", "role": "czytelnik", "borrowed": []}
]


def login(users):
    attempts = 0
    while attempts < 3:
        login_input = input("Podaj login: ")
        password_input = input("Podaj hasło: ")
        
        for user in users:
            if user["username"] == login_input and user["password"] == password_input:
                print(f"\nZalogowano pomyślnie jako {login_input}.")
                return user
                
        print("Nieprawidłowy login lub hasło. Spróbuj ponownie.")
        attempts += 1
        
    print("\nPrzekroczono limit prób logowania. Program kończy działanie.")
    return None


def show_catalog(books):
    print("\n--- KATALOG KSIĄŻEK ---")
    for book in books:
        print(f"Tytuł: {book['title']}, Autor: {book['author']}, Dostępne sztuki: {book['quantity']}")
    print("-----------------------")


def borrow_book(books, current_user):
    title_to_borrow = input("Podaj tytuł książki, którą chcesz wypożyczyć: ")
    
    for book in books:
        if book["title"].lower() == title_to_borrow.lower():
            if book["quantity"] > 0:
                book["quantity"] -= 1
                current_user["borrowed"].append(book["title"])
                print(f"Pomyślnie wypożyczono książkę: '{book['title']}'.")
            else:
                print("Niestety, brak dostępnych sztuk tej książki.")
            return
            
    print("Nie znaleziono książki o takim tytule w katalogu.")


def show_my_borrowed(current_user):
    print("\n--- MOJE WYPOŻYCZENIA ---")
    if len(current_user["borrowed"]) == 0:
        print("Nie masz aktualnie żadnych wypożyczonych książek.")
    else:
        for title in current_user["borrowed"]:
            print(f"- {title}")
    print("-------------------------")


def main_menu(books, current_user):
    while True:
        print("\n=== MENU GŁÓWNE ===")
        print("1. Przeglądaj katalog")
        print("2. Wypożycz książkę")
        print("3. Moje wypożyczenia")
        print("4. Wyloguj")
        
        choice = input("Wybierz opcję (1-4): ")
        
        if choice == '1':
            show_catalog(books)
        elif choice == '2':
            borrow_book(books, current_user)
        elif choice == '3':
            show_my_borrowed(current_user)
        elif choice == '4':
            print("Wylogowano pomyślnie.")
            break
        else:
            print("Niepoprawny wybór. Wpisz liczbę od 1 do 4.")


def main():
    current_user = login(users_data)
    
    if current_user is not None:
        main_menu(books_data, current_user)


if __name__ == "__main__":
    main()
