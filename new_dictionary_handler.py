from pathlib import Path
from tkinter import filedialog
from typing import Any, Self, Protocol

from openpyxl import load_workbook


class NewDictHandlerProtocol(Protocol):
    def validate_name(self, new_name: str, i=2) -> Self:
        ...

    def set_file_path(self) -> Self:
        ...

    def load_raw_file(self) -> Self:
        ...

    def set_validated_data(self) -> Self:
        ...

    def get_data(self) -> Any:
        ...


class NewDictHandlerForJSONRepo:
    def __init__(self, name: str, taken_names: list[str], max_word_length: int):
        self.name = name
        self.taken_names = taken_names
        self.max_word_length = max_word_length
        self.validated_name = None
        self.file_path = None
        self.raw_file = None
        self.validated_data = None

    def validate_name(self, new_name: str, i=2) -> Self:
        if new_name not in self.taken_names:
            self.validated_name = new_name
            return self
        return self.validate_name(f"{self.name}({i})", i + 1)

    def set_file_path(self) -> Self:
        filename = filedialog.askopenfilename(
            initialdir="/",
            title="Select a File",
            filetypes=(("xls files", "*.xls*"),
                       ("all files", "*.*"))
        )
        self.file_path = Path(filename)
        return self

    def load_raw_file(self) -> Self:
        self.raw_file = load_workbook(filename=self.file_path).worksheets[0]
        return self

    def set_validated_data(self) -> Self:
        dictionary = {}
        for row in self.raw_file.rows:
            if not row[0].value or not row[1].value:
                continue
            if (len(row[0].value.strip()) > self.max_word_length or
                    len(row[1].value.strip()) > self.max_word_length):
                continue
            if row[0].value.strip() not in dictionary:
                dictionary[row[0].value.strip()] = row[1].value.strip()
                if len(dictionary) == 200:
                    break
        self.validated_data = dictionary if len(dictionary) >= 10 else None
        return self

    def get_data(self) -> Any:
        return dict(
            name=self.validated_name,
            dictionary={key: value for key, value in self.validated_data.items()},
            scores={key: 0 for key in self.validated_data}
        )
