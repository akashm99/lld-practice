from abc import ABC, abstractmethod
from typing import List, Optional

# State Pattern
class EditingState(ABC):
    @abstractmethod
    def handle_input(self, document: 'Document', input_text: str):
        pass

class NormalState(EditingState):
    def handle_input(self, document: 'Document', input_text: str):
        document.append_text(input_text)

class UppercaseState(EditingState):
    def handle_input(self, document: 'Document', input_text: str):
        document.append_text(input_text.upper())

# Command Pattern
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class AppendTextCommand(Command):
    def __init__(self, document: 'Document', text: str):
        self.document = document
        self.text = text

    def execute(self):
        self.document.state.handle_input(self.document, self.text)

    def undo(self):
        self.document.remove_text(len(self.text))

# Builder Pattern
class DocumentBuilder:
    def __init__(self):
        self.title = ""
        self.sections = []

    def set_title(self, title: str):
        self.title = title
        return self

    def add_section(self, section: str):
        self.sections.append(section)
        return self

    def build(self) -> 'Document':
        document = Document()
        document.set_title(self.title)
        for section in self.sections:
            document.append_text(section + "\n")
        return document

# Document class
class Document:
    def __init__(self):
        self.content = ""
        self.title = ""
        self.state: EditingState = NormalState()
        self.command_history: List[Command] = []

    def set_title(self, title: str):
        self.title = title

    def set_state(self, state: EditingState):
        self.state = state

    def append_text(self, text: str):
        self.content += text

    def remove_text(self, length: int):
        self.content = self.content[:-length]

    def handle_input(self, input_text: str):
        command = AppendTextCommand(self, input_text)
        command.execute()
        self.command_history.append(command)

    def undo(self):
        if self.command_history:
            command = self.command_history.pop()
            command.undo()

    def get_content(self):
        return f"Title: {self.title}\n\n{self.content}"

# Editor class to manage the document
class Editor:
    def __init__(self):
        self.document: Optional[Document] = None

    def create_document(self, builder: DocumentBuilder):
        self.document = builder.build()

    def write(self, text: str):
        if self.document:
            self.document.handle_input(text)

    def switch_to_uppercase(self):
        if self.document:
            self.document.set_state(UppercaseState())

    def switch_to_normal(self):
        if self.document:
            self.document.set_state(NormalState())

    def undo(self):
        if self.document:
            self.document.undo()

    def get_document_content(self):
        return self.document.get_content() if self.document else "No document created"

# Usage
if __name__ == "__main__":
    editor = Editor()

    # Using Builder to create a document
    doc_builder = DocumentBuilder()
    doc_builder.set_title("My Document").add_section("Introduction").add_section("Main Content")
    editor.create_document(doc_builder)

    # Writing in normal state
    editor.write("This is normal text. ")

    # Switching to uppercase state
    editor.switch_to_uppercase()
    editor.write("this will be uppercase. ")

    # Switching back to normal state
    editor.switch_to_normal()
    editor.write("Back to normal. ")

    # Undoing the last action
    editor.undo()

    # Printing the final content
    print(editor.get_document_content())