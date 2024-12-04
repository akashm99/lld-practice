from abc import ABC, abstractmethod
from collections import defaultdict
from typing import List, Dict

# Book and Line classes
class Line:
    def __init__(self, content: str):
        self.content = content

class Book:
    def __init__(self, title: str, author: str):
        self.title = title
        self.author = author

# Factory for creating books
class BookFactory:
    @staticmethod
    def create_book(title: str, author: str) -> Book:
        return Book(title, author)

# Strategy pattern for parsing
class ParsingStrategy(ABC):
    @abstractmethod
    def parse(self, line: Line) -> List[str]:
        pass

class SimpleWordParsingStrategy(ParsingStrategy):
    def parse(self, line: Line) -> List[str]:
        return line.content.split()

class CharacterParsingStrategy(ParsingStrategy):
    def __init__(self, characters: List[str]):
        self.characters = characters

    def parse(self, line: Line) -> List[str]:
        return [char for char in self.characters if char.lower() in line.content.lower()]

# Character Index
class CharacterIndex:
    def __init__(self):
        self.index = defaultdict(int)

    def update(self, characters: List[str]):
        for char in characters:
            self.index[char] += 1

    def get_count(self, character: str) -> int:
        return self.index[character]

    def get_all_counts(self) -> Dict[str, int]:
        return dict(self.index)

# Book Parser
class BookParser:
    def __init__(self, parsing_strategy: ParsingStrategy):
        self.parsing_strategy = parsing_strategy
        self.character_index = CharacterIndex()

    def parse_book(self, book: Book, get_lines_api):
        lines = get_lines_api(book)
        for line in lines:
            characters = self.parsing_strategy.parse(line)
            self.character_index.update(characters)

    def get_character_count(self, character: str) -> int:
        return self.character_index.get_count(character)

    def get_all_character_counts(self) -> Dict[str, int]:
        return self.character_index.get_all_counts()

# Controller
class BookParserController:
    def __init__(self):
        self.book_factory = BookFactory()
        self.parser = None

    def set_parsing_strategy(self, strategy: ParsingStrategy):
        self.parser = BookParser(strategy)

    def parse_books(self, book_data: List[Dict], get_lines_api):
        results = {}
        for data in book_data:
            book = self.book_factory.create_book(data['title'], data['author'])
            self.parser.parse_book(book, get_lines_api)
        return self.parser.get_all_character_counts()

# Usage
def get_lines_api(book: Book) -> List[Line]:
    # This is a mock function. In reality, this would be an API call.
    return [Line("Harry and Hermione went to Hogwarts."), 
            Line("Ron joined them later.")]

if __name__ == "__main__":
    controller = BookParserController()
    
    # Set up parsing strategy for Harry Potter characters
    hp_characters = ["Harry", "Hermione", "Ron"]
    hp_strategy = CharacterParsingStrategy(hp_characters)
    controller.set_parsing_strategy(hp_strategy)

    # Parse books
    books_to_parse = [
        {"title": "Harry Potter and the Philosopher's Stone", "author": "J.K. Rowling"},
        {"title": "Harry Potter and the Chamber of Secrets", "author": "J.K. Rowling"}
    ]

    character_counts = controller.parse_books(books_to_parse, get_lines_api)
    print(character_counts)
