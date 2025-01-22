
class Book:


    def __init__(self, title, author,is_loaned,copies, genre, year):
        self.__title = title
        self.__author = author
        self.__year = int(year)
        self.__genre = genre
        self.__copies = int(copies)
        #
        self.__is_loaned = is_loaned
        self.__available = self.__copies if self.__is_loaned == "No" else 0

        #
        #self.__copy_list = list()
        self.__is_popular = 0

        # for i in range(self.__copies):
        #     self.__copy_list.append({'Key' : is_loaned, 'value': i})
        #     #self.__is_loaned = dict(key= is_loaned,value = 0)
        # else:
        #     self.__is_loaned = is_loaned


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
    
    def is_loaned(self):
        return str(self.__is_loaned)

    def reduce(self, amount):
        self.__available -= int(amount)

    def reduce_available(self):
        if self.__available  - 1 >= 0:
            self.__available -= 1

    def increase_available(self):
        if self.__available + 1 <= self.__copies:
            self.__available += 1

    def get_available(self):
        return self.__available

    def fully_available(self):
        # for i in range(self.__copies):
        #     if self.__copy_list[i]['Key'] == "Yes":
        #         return False
        # return True
        return True if self.__available == self.__copies else False

    def set_loaned(self, t):
        self.__is_loaned = str(t)


    def add_copies(self,amount):
        self.__copies +=int(amount)
        self.__available += int(amount)


    def is_available(self):
        return True if self.__is_loaned == "No" else False


    def __str__(self):
        return f'{self.__title}, {self.__author}, {self.__is_loaned}, {self.__copies},{self.__genre}, {self.__year}'


    def __repr__(self):
        return f'{self.__title}, {self.__author}, {self.__is_loaned}, {self.__copies},{self.__genre}, {self.__year}'


    def get_dict(self):
        return {'title':[self.__title],
            'author':[self.__author],
            'is_loaned':[self.__is_loaned],
            'copies':[self.__copies],
            'genre':[self.__genre],
            'year':[self.__year]}