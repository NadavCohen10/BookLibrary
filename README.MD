# README

**Authors: Nadav Cohen, Amnon Fuzailov**
## Project Overview
This project is a library management system implemented in Python, designed to manage books, users, and their interactions. It supports functionalities such as book lending, returning, user management, and book availability tracking. The system incorporates Object-Oriented Programming (OOP) principles to ensure scalability and maintainability.

## Instructions to Run the Project
1. Ensure you have Python 3.x installed on your machine.
2. Install any required dependencies using the following command:
   ```bash
   pip install -r requirements.txt
   ```
   *(If the `requirements.txt` file is missing, please ensure you install libraries like `pandas` manually.)*
3. Run the main application by executing:
   ```bash
   python main.py
   ```
4. Follow the on-screen instructions to navigate through the system functionalities.

## System Functionalities
### Library

1. **Book Management:**

   - Add new books.
   - Remove books (if not loaned).
   - View books.
   - Search books.

2. **Borrowing & Returning:**

   - Borrow available books.
   - Return loaned books.
   - Update CSV files accordingly.

3. **Waiting List Management:**

   - Add clients to the waiting list.
   - Notify users when books become available.

4. **Data Persistence:**

   - Load and save data using CSV files.
   - Maintain separate files for all, available, loaned, and waiting lists.

### Dashboard
- **User Dashboard:** Displays user-specific information, including borrowed books and notifications about the waiting list.


### Logs
- Tracks important system events like user login/logout, book loans, returns, and errors for system auditing purposes.

## Object-Oriented Programming (OOP) Patterns
The project employs several OOP patterns and principles to enhance code organization and maintainability. Below is a description of the patterns used:



### 1. **Encapsulation**
- Classes like `Book`, `Library` encapsulate data and provide controlled access through methods.
- Example: The `Book` class stores attributes like `title`, `author`, and `copies`, and access is provided via getter and setter methods.


### 2. **Abstraction**
- Abstracting complex logic into classes and methods hides implementation details from the user.
- Example: The `Library` class provides a simplified interface to interact with books, while managing underlying complexities like file handling and book availability.

### 3. **Observer Pattern**
- Implemented to notify users in the waiting list when a book becomes available.
- Example: The waiting list system sends notifications automatically when a book is returned.


### 4. **Composition**

- The `Library` class uses composition by including objects of the `Book` class.
- The `Book` class is instantiated and stored within the library, promoting a "has-a" relationship.
- Example:
  ```python
  book = bk(row["title"], row["author"], row["is_loaned"], row["copies"], row["genre"], row["year"])
  ```

### 5. **Strategy Pattern**
- **Intent:**
  - The Strategy Pattern is used to define a family of algorithms (search strategies), encapsulate them in separate classes, and make them interchangeable.
- **Structure:**
  - The pattern consists of the following components:
    - **Abstract Base Class (`SearchStrategy`)**: Defines the interface for all concrete search strategies.
    - **Concrete Strategies (`TitleSearchStrategy`, `AuthorSearchStrategy`, `CategorySearchStrategy`, `YearSearchStrategy`)**: Implement the search logic based on different criteria.
    - **Context Class (`SearchContext`)**: Maintains a reference to a search strategy and allows clients to switch strategies dynamically.

### 6. **Encapsulation and Abstraction**
- Each search functionality is encapsulated within its respective strategy class.
- The abstract base class provides abstraction, ensuring consistent behavior across different search strategies.

### 7. **Dependency Injection**
- The `SearchContext` class is designed to accept any search strategy via dependency injection, promoting loose coupling and high cohesion.

---

## Conclusion
This project demonstrates a robust application of OOP principles and design patterns to create a functional and maintainable library management system.

