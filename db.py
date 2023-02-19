from pathlib import Path
from typing import Protocol


_db_path = ""


class DB(Protocol):
    def load_table(self, table_name: str) -> list[tuple]:
        ...

    def drop_table(self, table_name: str) -> None:
        ...

    def create_table(self, table_name: str) -> None:
        ...

    def insert_data(self, table_name: str, data: dict[str, str]) -> None:
        ...

    def delete_rows(self, table_name: str, lst: list[str]) -> None:
        ...

    def update_rows(self, table_name: str, lst: list[str], points: dict[str, int]) -> None:
        ...

    def insert_rows(self, table_name: str, lst: list[str], data: dict[str, str]) -> None:
        ...

    @property
    def available_dictionaries(self) -> list[str]:
        return ...

    def clear_user_db(self) -> None:
        ...

    def copy_data_from_default_db(self, db_name: Path | str = _db_path) -> None:
        ...
