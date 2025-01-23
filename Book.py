
class Book:

    # Constructor to initialize book properties
    def __init__(self, title, author,is_loaned,copies, genre, year):
        self.__title = title
        self.__author = author
        self.__year = int(year)
        self.__genre = genre
        self.__copies = int(copies)
        self.__is_loaned = is_loaned
        self.__available = self.__copies if self.__is_loaned == "No" else 0


    # Getter methods for book properties
    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_year(self):
        return self.__year

    def get_genre(self):
        return self.__genre

    def get_copies(self):
        return self.__copies

    def get_available(self):
        return self.__available
    
    def is_loaned(self):
        return str(self.__is_loaned)

    # Reduce available copies
    def reduce(self, amount):
        self.__available -= int(amount)

    # Reduce available copies by 1 if possible
    def reduce_available(self):
        if self.__available  - 1 >= 0:
            self.__available -= 1

    # Increase available copies by 1 if possible
    def increase_available(self):
        if self.__available + 1 <= self.__copies:
            self.__available += 1

    # Check if all copies are available
    def fully_available(self):
        return True if self.__available == self.__copies else False

    # Set loan status
    def set_loaned(self, t):
        self.__is_loaned = str(t)

    # Add copies to the book
    def add_copies(self,amount):
        self.__copies +=int(amount)
        self.__available += int(amount)

    # Check if book is available for loan
    def is_available(self):
        return True if self.__is_loaned == "No" else False

    # String representation of the book
    def __str__(self):
        return f'{self.__title}, {self.__author}, {self.__is_loaned}, {self.__copies},{self.__genre}, {self.__year}'

    # Representation method (same as __str__)
    def __repr__(self):
        return f'{self.__title}, {self.__author}, {self.__is_loaned}, {self.__copies},{self.__genre}, {self.__year}'

    # Convert book properties to dictionary
    def get_dict(self):
        return {'title':[self.__title],
            'author':[self.__author],
            'is_loaned':[self.__is_loaned],
            'copies':[self.__copies],
            'genre':[self.__genre],
            'year':[self.__year]}