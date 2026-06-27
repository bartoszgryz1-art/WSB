class Book:
    def __init__(self, title, author, total_copies):
        self.title = title
        self.author = author
        self._total_copies = total_copies
        self._available_copies = total_copies
        self.reservations = 0

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
        return f"'{self.title}' autorstwa {self.author} (dostępne: {self.available_copies}/{self._total_copies}, rezerwacje: {self.reservations})"


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
        print("1. Przeglądaj książki (Sortowanie i Filtrowanie)")
        print("2. Wypożycz lub zarezerwuj książkę")
        print("3. Moje wypożyczenia")
        print("4. Poproś o przedłużenie")
        print("5. Wyloguj")


class Librarian(User):
    def __init__(self, login, password):
        super().__init__(login, password, "librarian")

    def show_menu(self):
        print("\n--- Menu Bibliotekarza ---")
        print("1. Przeglądaj książki (Sortowanie i Filtrowanie)")
        print("2. Lista wszystkich wypożyczeń")
        print("3. Obsługa próśb o przedłużenie")
        print("4. Statystyki")
        print("5. Wyloguj")


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


    def get_processed_books(self, predicate=lambda b: True, sort_key=None, reverse=False):
        processed = list(filter(predicate, self.books))
        if sort_key:
            processed = sorted(processed, key=sort_key, reverse=reverse)
        return processed

    def browse_books_menu(self):
        print("\nOpcje wyszukiwania i sortowania:")
        print("1. Pokaż wszystkie")
        print("2. Pokaż tylko dostępne (sztuki > 0)")
        print("3. Posortowane po tytule (A-Z)")
        print("4. Posortowane po dostępności (malejąco)")
        print("5. Szukaj po frazie (tytuł lub autor)")
        
        c = input("Wybierz opcję: ")
        
        if c == "1":
            return self.get_processed_books()
        elif c == "2":
            return self.get_processed_books(predicate=lambda b: b.available_copies > 0)
        elif c == "3":
            return self.get_processed_books(sort_key=lambda b: b.title)
        elif c == "4":
            return self.get_processed_books(sort_key=lambda b: b.available_copies, reverse=True)
        elif c == "5":
            phrase = input("Podaj szukaną frazę: ").lower()
            return self.get_processed_books(predicate=lambda b: phrase in b.title.lower() or phrase in b.author.lower())
        return []

    def print_books_list(self, books_list):
        if not books_list:
            print("Brak wyników.")
            return
        
        lines = [f"{i + 1}. {b}" for i, b in enumerate(books_list)]
        print("\nKatalog:")
        print("\n".join(lines))

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
                    books = self.browse_books_menu()
                    self.print_books_list(books)
                    
                elif choice == "2":
                    books = self.browse_books_menu()
                    self.print_books_list(books)
                    if not books: continue

                    try:
                        idx = int(input("\nPodaj numer książki do wypożyczenia/rezerwacji: ")) - 1
                        if 0 <= idx < len(books):
                            book = books[idx]
                            if book.borrow():
                                user.borrowed_books.append(book)
                                print(f"Wypożyczono: {book.title}")
                            else:
                                dec = input("Brak wolnych egzemplarzy. Czy chcesz ZAREZERWOWAĆ? (T/N): ").lower()
                                if dec == 't':
                                    book.reservations += 1
                                    print("Zarezerwowano.")
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
                    books = self.browse_books_menu()
                    self.print_books_list(books)
                    
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
                            if idx == -1: continue
                            
                            if 0 <= idx < len(requests):
                                u, req_title = requests[idx]
                                
                                book_obj = next((b for b in self.books if b.title == req_title), None)
                                if book_obj and book_obj.reservations > 0:
                                    print(f"BŁĄD: Nie można przedłużyć. Książka '{req_title}' posiada rezerwacje ({book_obj.reservations}).")
                                    u.extension_requests.remove(req_title)
                                else:
                                    dec = input("Zatwierdzić przedłużenie? (T/N): ").lower()
                                    if dec == 't':
                                        print(f"Zatwierdzono przedłużenie '{req_title}' dla {u.login}.")
                                        u.extension_requests.remove(req_title)
                                    elif dec == 'n':
                                        print(f"Odrzucono przedłużenie '{req_title}' dla {u.login}.")
                                        u.extension_requests.remove(req_title)
                            else:
                                print("Błędny numer.")
                        except ValueError:
                            print("Wpisz poprawną liczbę.")
                            
                elif choice == "4":
                    print("\n--- Statystyki Biblioteki ---")
                    
                    pop_book = sorted(self.books, key=lambda b: b._total_copies - b.available_copies, reverse=True)[0]
                    diff = pop_book._total_copies - pop_book.available_copies
                    print(f"Najpopularniejsza książka: '{pop_book.title}' ({diff} wypożyczonych)")

                    readers_only = [u for u in self.users if u.role == "reader"] # List comprehension
                    total_borrowed = sum(map(lambda r: len(r.borrowed_books), readers_only)) # Zastosowanie map + lambda
                    print(f"Liczba aktywnych wypożyczeń ogółem: {total_borrowed}")

                    print("\nRanking czytelników:")
                    stats_dict = {
                        r.login: len(r.borrowed_books) 
                        for r in sorted(readers_only, key=lambda r: len(r.borrowed_books), reverse=True)
                    }
                    for login, count in stats_dict.items():
                        print(f"- {login}: {count} szt.")

                elif choice == "5":
                    break


if __name__ == "__main__":
    library = Library()
    
    library.add_book(Book("Wiedźmin", "Andrzej Sapkowski", 3))
    library.add_book(Book("Lalka", "Bolesław Prus", 1))
    library.add_book(Book("Hobbit", "J.R.R. Tolkien", 2))
    
    library.add_user(Reader("student", "haslo123"))
    library.add_user(Librarian("admin", "admin123"))
    
    library.run()