import string
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from openpyxl import load_workbook

from model import Model
from db import DB


@dataclass
class ModelsHandler:
    model: Model = None
    db: DB = None

    def create_model(self, name: str) -> None:
        """A method called at each initialization of the app
        or while changing the dictionary"""
        data = self.db.load_table(name)
        dictionary = {elem[0]: elem[1] for elem in data}
        scores = Counter({elem[0]: elem[2] for elem in data})
        special_letters = self.extract_special_letters(words=[elem[1] for elem in data])
        self.model = Model(name=name,
                           dictionary=dictionary,
                           scores=scores,
                           special_letters=special_letters)

    def push_changes_to_db(self) -> None:
        """Commits changes to db at each termination of the app
        or while changing the dictionary"""
        if self.model.added_words:
            self.db.insert_rows(self.model.name, self.model.added_words,
                                self.model.dictionary)
            self.db.update_rows(self.model.name, self.model.added_words,
                                self.model.scores)
        if self.model.deleted_words:
            self.db.delete_rows(self.model.name, self.model.deleted_words)
        if self.model.scores_to_update:
            self.db.update_rows(self.model.name, self.model.scores_to_update,
                                self.model.scores)

    def get_model_name(self, first_lang, second_lang) -> str | Callable:
        """Returns a valid model_name of a new dictionary added by the user"""
        name = f"{first_lang}-{second_lang}"
        if name not in self.db.available_dictionaries:
            return name
        return self.set_model_name(first_lang, second_lang)

    def set_model_name(self, first_language, second_language, i=2) -> str | Callable:
        """Sets name of a new dictionary added by the user if the default name already exists"""
        name = f"{first_language}-{second_language}_{i}"
        if name in self.db.available_dictionaries:
            return self.set_model_name(first_language, second_language, i + 1)
        return name

    @staticmethod
    def validate_data(file_path: Path, str_len_limit: int) -> dict[str, str] | None:
        """Validates data from the file provided by end user.
           str_len_limit - max len of string allowed.
           Returns a dict of word: translation pairs of up to 1000 pairs.
           Returns None if less than 10 pairs."""
        dictionary = {}
        worksheet = load_workbook(filename=file_path).worksheets[0]
        for row in worksheet.rows:
            if not row[0].value or not row[1].value:
                continue
            if len(row[0].value.strip()) > str_len_limit or len(row[0].value.strip()) > str_len_limit:
                continue
            if row[0].value.strip() not in dictionary:
                dictionary[row[0].value.strip()] = row[1].value.strip()
                if len(dictionary) == 1000:
                    break
        return dictionary if len(dictionary) >= 10 else None

    @staticmethod
    def extract_special_letters(words=list[str]) -> list[str]:
        """Returns a list of non-ascii characters present in self.dictionary.values()"""
        special_letters = []
        for word in words:
            for letter in word:
                if letter not in string.printable and letter not in special_letters:
                    special_letters.append(letter)
        return special_letters
