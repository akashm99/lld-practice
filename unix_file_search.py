# Simulated File System (in-memory database)
mock_files_db = [
    {"name": "file1.txt", "extension": ".txt", "size": 500},
    {"name": "file2.log", "extension": ".log", "size": 1500},
    {"name": "script.py", "extension": ".py", "size": 100},
    {"name": "report.doc", "extension": ".doc", "size": 1200},
    {"name": "image.png", "extension": ".png", "size": 3000}
]

from abc import ABC, abstractmethod

# Abstract strategy for searching files
class SearchStrategy(ABC):
    @abstractmethod
    def search(self, files_db: list) -> list:
        pass

# Concrete strategy for searching by file name
class NameSearchStrategy(SearchStrategy):
    def __init__(self, file_name: str):
        self.file_name = file_name

    def search(self, files_db: list) -> list:
        # Search files that match the given file name
        return [file for file in files_db if self.file_name in file["name"]]

# Concrete strategy for searching by file extension
class ExtensionSearchStrategy(SearchStrategy):
    def __init__(self, extension: str):
        self.extension = extension

    def search(self, files_db: list) -> list:
        # Search files that match the given extension
        return [file for file in files_db if file["extension"] == self.extension]


# Abstract decorator class for adding additional filtering functionality
class SearchDecorator(SearchStrategy):
    def __init__(self, search_strategy: SearchStrategy):
        self._search_strategy = search_strategy

    def search(self, files_db: list) -> list:
        return self._search_strategy.search(files_db)

# Concrete decorator for filtering files by size
class SizeFilterDecorator(SearchDecorator):
    def __init__(self, search_strategy: SearchStrategy, min_size: int, max_size: int):
        super().__init__(search_strategy)
        self.min_size = min_size
        self.max_size = max_size

    def search(self, files_db: list) -> list:
        # Filter files based on size constraints after initial search
        files = super().search(files_db)
        return [file for file in files if self.min_size <= file["size"] <= self.max_size]


# Command interface for executing the search
class SearchCommand:
    def __init__(self, strategy: SearchStrategy):
        self.strategy = strategy

    def execute(self, files_db: list) -> list:
        return self.strategy.search(files_db)

# Concrete command for executing a search
class ExecuteSearchCommand(SearchCommand):
    def execute(self, files_db: list) -> list:
        print("Executing search...")
        return super().execute(files_db)

# Factory for creating the search strategy based on input type
class SearchFactory:
    @staticmethod
    def create_search(strategy_type: str, param: str) -> SearchStrategy:
        if strategy_type == "name":
            return NameSearchStrategy(param)
        elif strategy_type == "extension":
            return ExtensionSearchStrategy(param)
        else:
            raise ValueError(f"Unknown search strategy: {strategy_type}")


# Controller that handles the search request and execution
class SearchController:
    def __init__(self, files_db: list):
        self.files_db = files_db

    def search(self, strategy_type: str, param: str, min_size: int = None, max_size: int = None) -> list:
        # Step 1: Create the appropriate search strategy via the factory
        strategy = SearchFactory.create_search(strategy_type, param)
        
        # Step 2: Optionally apply a size filter decorator
        if min_size is not None and max_size is not None:
            strategy = SizeFilterDecorator(strategy, min_size, max_size)

        # Step 3: Execute the search command
        command = ExecuteSearchCommand(strategy)
        result = command.execute(self.files_db)
        
        # Step 4: Return the result
        return result

# Example usage:
controller = SearchController(mock_files_db)

# Search by name
result_by_name = controller.search(strategy_type="name", param="file")
print("Search by name result:", result_by_name)

# Search by extension
result_by_extension = controller.search(strategy_type="extension", param=".py")
print("Search by extension result:", result_by_extension)

# Search by extension with size filtering
result_with_size = controller.search(strategy_type="extension", param=".log", min_size=1000, max_size=2000)
print("Search by extension with size filter result:", result_with_size)
