import json
from pathlib import Path
from typing import Protocol


class RepositoryProtocol(Protocol):
    def get_dictionary(self, name: str):
        ...

    def get_all_dictionaries(self) -> dict[str, dict[str, str]]:
        ...

    def add_dictionary(self, name, **data):
        ...

    def update_dictionary(self, name, **data):
        ...

    def delete_dictionary(self, name: str):
        ...

    @property
    def available_dictionaries(self) -> list[str]:
        ...


class JSONRepository:
    def __init__(self, path: Path):
        self.path = path

    def get_all_dictionaries(self) -> dict[str, dict[str, str]]:
        with open(self.path, "r", encoding="UTF-8") as db:
            return json.load(db)

    def get_dictionary(self, name: str):
        return self.get_all_dictionaries()[name]

    def add_dictionary(self, name, **data):
        db_data = self.get_all_dictionaries()
        db_data[name] = dict(data)
        with open(self.path, "w", encoding="UTF-8") as db:
            json.dump(db_data, db, indent=4)

    def update_dictionary(self, name, **data):
        return self.add_dictionary(name, **data)

    def delete_dictionary(self, name: str):
        data = self.get_all_dictionaries()
        data.pop(name)
        with open(self.path, "w", encoding="UTF-8") as db:
            json.dump(data, db, indent=4)

    @property
    def available_dictionaries(self) -> list[str]:
        with open(self.path, "r", encoding="UTF-8") as db:
            return list(json.load(db))


