import json
from pathlib import Path
from typing import Protocol, Optional

from learning_data import LearningData


class RepositoryProtocol(Protocol):
    def get_dictionary(self, name: str):
        ...

    def get_all_dictionaries(self) -> dict[str, dict[str, str]]:
        ...

    def add_dictionary(self, name, dictionary: dict[str, str], scores: Optional[dict[str, int]]):
        ...

    def update_dictionary(self, name, dictionary: dict[str, str], scores: dict[str, int], **extras):
        ...

    def delete_dictionary(self, name: str):
        ...

    @property
    def dictionaries_names(self) -> list[str]:
        ...


class JSONRepository:
    def __init__(self, path: Path):
        self.path = path

    def get_dictionary(self, name: str):
        with open(self.path, "r", encoding="UTF-8") as db:
            data = json.load(db)[name]
            return LearningData(name=name, dictionary=data["dictionary"], scores=data["scores"])

    def get_all_dictionaries(self) -> dict[str, dict[str, str]]:
        with open(self.path, "r", encoding="UTF-8") as db:
            return json.load(db)

    def add_dictionary(self, name, dictionary: dict[str, str], scores: Optional[dict[str, int]]):
        db_data = self.get_all_dictionaries()
        if scores:
            data_to_add = dict(dictionary={key: value for key, value in dictionary.items()},
                               scores={key: value for key, value in scores.items()})
        else:
            data_to_add = dict(dictionary={key: value for key, value in dictionary.items()},
                               scores={key: 0 for key in dictionary})
        db_data[name] = data_to_add
        with open(self.path, "w", encoding="UTF-8") as db:
            json.dump(db_data, db, indent=4)

    def update_dictionary(self, name, dictionary: dict[str, str], scores: dict[str, int], **extras):
        return self.add_dictionary(name, dictionary, scores)

    def delete_dictionary(self, name: str):
        data = self.get_all_dictionaries()
        data.pop(name)
        with open(self.path, "w", encoding="UTF-8") as db:
            json.dump(data, db, indent=4)

    @property
    def dictionaries_names(self) -> list[str]:
        with open(self.path, "r", encoding="UTF-8") as db:
            return list(json.load(db))

