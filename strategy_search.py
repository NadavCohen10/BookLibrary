
from abc import ABC, abstractmethod
from typing import List, Dict
from Book import Book


# Abstract base class defining the search strategy interface
class SearchStrategy(ABC):
    @abstractmethod
    def search(self, data: List[Dict], query: str) -> List[Dict]:
        # Abstract method to be implemented by specific search strategies
        pass


# Search strategy for finding books by title
class TitleSearchStrategy(SearchStrategy):

     def search(self, data: List[Dict], query: str) -> List[Dict]:
         # Searches for books where the query matches (case-insensitive) the book's title
         return [item for item in data if query.lower() in item.get_title().lower()]


# Search strategy for finding books by author
class AuthorSearchStrategy(SearchStrategy):
    def search(self, data: List[Dict], query: str) -> List[Dict]:
        # Searches for books where the query matches (case-insensitive) the book's author
        return [item for item in data if query.lower() in item.get_author().lower()]


# Search strategy for finding books by category
class CategorySearchStrategy(SearchStrategy):
    def search(self, data: List[Dict], query: str) -> List[Dict]:
        # Searches for books where the query matches (case-insensitive) the book's genre
        return [item for item in data if query.lower() in item.get_genre().lower()]


# Search strategy for finding books by publication year
class YearSearchStrategy(SearchStrategy):
    def search(self, data: List[Dict], query: str) -> List[Dict]:
        # Searches for books where the query matches the book's publication year
        return [item for item in data if query in str(item.get_year())]



# Context class to manage and execute search strategies
class SearchContext:
    def __init__(self, strategy: SearchStrategy):
        # Initialize the search context with a specific search strategy
        self.strategy = strategy

    def set_strategy(self, strategy: SearchStrategy):
        # Allow changing the search strategy dynamically
        self.strategy = strategy

    def search(self, data: List[Dict], query: str) -> List[Dict]:
        # Execute the current search strategy on the given data
        return self.strategy.search(data, query)