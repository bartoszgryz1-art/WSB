class Book:
    def __init__(self, title, author, total_copies):
        self.title = title
        self.author = author
        self._total_copies = total_copies
        self._available_copies = total_copies

    @property
    def available_copies(self):
        return self._available_copies

    def borrow(self):
        if self._available_copies > 0:
            self._available_copies -= 1
            return True
        return False

    def return_book(self):
        if self._available_copies < self._total_copies:
            self._available_copies += 1

    def __str__(self):
        return f"'{self.title}' autorstwa {self.author} (dostępne: {self.available_copies}/{self._total_copies})"


class User:
    def __init__(self, login, password, role):
        self._login = login
        self._password = password
        self.role = role

    @property
    def login(self):
        return self._login

    def check_password(self, password):
        return self._password == password


class Reader(User):
    def __init__(self, login, password):
        super().__init__(login, password, "reader")
        self.borrowed_books = [] 
        self.extension_requests = [] 

    def show_menu(self):
        print("\n--- Menu Czytelnika ---")
        print("1. Przeglądaj książki")
        print("2. Wypożycz książkę")
        print("3. Moje wypożyczenia")
        print("4. Poproś o przedłużenie")
        print("5. Wyloguj")


class Librarian(User):
    def __init__(self, login, password):
        super().__init__(login, password, "librarian")

    def show_menu(self):
        print("\n--- Menu Bibliotekarza ---")
        print("1. Przeglądaj książki")
        print("2. Lista wszystkich wypożyczeń")
        print("3. Obsługa próśb o przedłużenie")
        print("4. Wyloguj")


class Library:
    def __init__(self):
        self.books = []
        self.users = []

    def add_book(self, book):
        self.books.append(book)

    def add_user(self, user):
        self.users.append(user)

    def find_user(self, login, password):
        for user in self.users:
            if user.login == login and user.check_password(password):
                return user
        return None

    def show_all_books(self):
        print("\nKatalog książek:")
        for i, book in enumerate(self.books):
            print(f"{i + 1}. {book}")

    def run(self):
        print("Witaj w systemie bibliotecznym!")
        while True:
            print("\n1. Zaloguj się\n2. Wyjdź")
            choice = input("Wybierz opcję: ")
            
            if choice == "1":
                login = input("Login: ")
                password = input("Hasło: ")
                user = self.find_user(login, password)
                
                if user:
                    print(f"\nZalogowano pomyślnie. Rola: {user.role}.")
                    self.user_session(user)
                else:
                    print("Błędny login lub hasło.")
            elif choice == "2":
                print("Do widzenia!")
                break
            else:
                print("Nieprawidłowa opcja.")

    def user_session(self, user):
        while True:
            user.show_menu()
            choice = input("Wybierz opcję: ")
            
            if user.role == "reader":
                if choice == "1":
                    self.show_all_books()
                elif choice == "2":
                    self.show_all_books()
                    try:
                        idx = int(input("Podaj numer książki do wypożyczenia: ")) - 1
                        if 0 <= idx < len(self.books):
                            book = self.books[idx]
                            if book.borrow():
                                user.borrowed_books.append(book)
                                print(f"Wypożyczono: {book.title}")
                            else:
                                print("Brak wolnych egzemplarzy.")
                        else:
                            print("Błędny numer.")
                    except ValueError:
                        print("Wpisz poprawną liczbę.")
                elif choice == "3":
                    print("\nTwoje wypożyczenia:")
                    if not user.borrowed_books:
                        print("Brak wypożyczonych książek.")
                    for b in user.borrowed_books:
                        print(f"- {b.title}")
                elif choice == "4":
                    if not user.borrowed_books:
                        print("Nie masz żadnych książek do przedłużenia.")
                        continue
                    print("\nWybierz książkę do przedłużenia:")
                    for i, b in enumerate(user.borrowed_books):
                        print(f"{i + 1}. {b.title}")
                    try:
                        idx = int(input("Numer: ")) - 1
                        if 0 <= idx < len(user.borrowed_books):
                            book = user.borrowed_books[idx]
                            if book.title not in user.extension_requests:
                                user.extension_requests.append(book.title)
                                print("Wysłano prośbę o przedłużenie.")
                            else:
                                print("Prośba o tę książkę jest już w systemie.")
                        else:
                            print("Błędny numer.")
                    except ValueError:
                        print("Wpisz poprawną liczbę.")
                elif choice == "5":
                    break
                    
            elif user.role == "librarian":
                if choice == "1":
                    self.show_all_books()
                elif choice == "2":
                    print("\nLista wszystkich wypożyczeń:")
                    found_any = False
                    for u in self.users:
                        if u.role == "reader" and u.borrowed_books:
                            found_any = True
                            for b in u.borrowed_books:
                                print(f"Użytkownik: {u.login} | Książka: {b.title}")
                    if not found_any:
                        print("Brak wypożyczeń w systemie.")
                elif choice == "3":
                    print("\nKolejka próśb o przedłużenie:")
                    requests = []
                    for u in self.users:
                        if u.role == "reader":
                            for req in u.extension_requests:
                                requests.append((u, req))
                                
                    if not requests:
                        print("Brak próśb do obsłużenia.")
                    else:
                        for i, (u, req) in enumerate(requests):
                            print(f"{i + 1}. Użytkownik {u.login} prosi o przedłużenie '{req}'")
                        try:
                            idx = int(input("Podaj numer prośby do obsłużenia (lub 0 aby wrócić): ")) - 1
                            if idx == -1:
                                continue
                            if 0 <= idx < len(requests):
                                u, req = requests[idx]
                                dec = input("Zatwierdzić przedłużenie? (T/N): ").lower()
                                if dec == 't':
                                    print(f"Zatwierdzono przedłużenie '{req}' dla {u.login}.")
                                    u.extension_requests.remove(req)
                                elif dec == 'n':
                                    print(f"Odrzucono przedłużenie '{req}' dla {u.login}.")
                                    u.extension_requests.remove(req)
                            else:
                                print("Błędny numer.")
                        except ValueError:
                            print("Wpisz poprawną liczbę.")
                elif choice == "4":
                    break


if __name__ == "__main__":
    library = Library()
    
    library.add_book(Book("Wiedźmin", "Andrzej Sapkowski", 3))
    library.add_book(Book("Lalka", "Bolesław Prus", 1))
    library.add_book(Book("Hobbit", "J.R.R. Tolkien", 2))
    
    library.add_user(Reader("student", "haslo123"))
    library.add_user(Librarian("admin", "admin123"))
    
    library.run()
