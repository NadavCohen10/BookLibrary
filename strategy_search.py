
from abc import ABC, abstractmethod
from typing import List, Dict
from Book import Book


# הגדרת הממשק עבור אסטרטגיית חיפוש
class SearchStrategy(ABC):
    @abstractmethod
    def search(self, data: List[Dict], query: str) -> List[Dict]:
        pass


# אסטרטגיית חיפוש לפי שם
class TitleSearchStrategy(SearchStrategy):


     def search(self, data: List[Dict], query: str) -> List[Dict]:
         return [item for item in data if query.lower() in item.get_title().lower()]


# אסטרטגיית חיפוש לפי מחבר
class AuthorSearchStrategy(SearchStrategy):
    def search(self, data: List[Dict], query: str) -> List[Dict]:
        return [item for item in data if query.lower() in item.get_author().lower()]


# אסטרטגיית חיפוש לפי קטגוריה
class CategorySearchStrategy(SearchStrategy):
    def search(self, data: List[Dict], query: str) -> List[Dict]:
        return [item for item in data if query.lower() in item.get_genre().lower()]


# אסטרטגיית חיפוש לפי שנה
class YearSearchStrategy(SearchStrategy):
    def search(self, data: List[Dict], query: str) -> List[Dict]:
        return [item for item in data if query in str(item.get_year())]



# מחלקת הקשר (Context) לניהול האסטרטגיות
class SearchContext:
    def __init__(self, strategy: SearchStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: SearchStrategy):
        self.strategy = strategy

    def search(self, data: List[Dict], query: str) -> List[Dict]:
        return self.strategy.search(data, query)

