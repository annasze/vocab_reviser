import sqlite3
from pathlib import Path

_user_db_path = Path.cwd() / "db/user.db"
_vocab_db_path = Path.cwd() / "db/vocab.db"


class SQLite3DB:
    def __init__(self) -> None:
        self.connection = sqlite3.connect(_user_db_path)
        self.cursor = self.connection.cursor()

    def load_table(self, table_name: str) -> list[tuple]:
        self.cursor.execute(f'SELECT * FROM "{table_name}"')
        return self.cursor.fetchall()

    def drop_table(self, table_name: str) -> None:
        self.cursor.execute(f'DROP table "{table_name}";')
        self.connection.commit()

    def create_table(self, table_name: str) -> None:
        self.cursor.execute(f"""CREATE table if not exists "{table_name}"(
                                word varchar not null primary key,
                                translation varchar not null,
                                points int default 0);""")

    def insert_data(self, table_name: str, data: dict[str, str]) -> None:
        for word in data:
            self.cursor.execute(f"""INSERT INTO "{table_name}"
                                    VALUES {(word, data[word], 0)};""")
        self.connection.commit()

    def delete_rows(self, table_name: str, lst: list[str]) -> None:
        for word in lst:
            self.cursor.execute(f"""DELETE FROM "{table_name}"
                                    WHERE word="{word}";""")
        self.connection.commit()

    def update_rows(self, table_name: str, lst: list[str], points: dict[str, int]) -> None:
        for word in lst:
            self.cursor.execute(f"""UPDATE "{table_name}"
                                    SET points = {points[word]}
                                    WHERE word = "{word}";""")
        self.connection.commit()

    def insert_rows(self, table_name: str, lst: list[str], data: dict[str, str]) -> None:
        for word in lst:
            self.cursor.execute(f"""INSERT INTO "{table_name}"
                                    VALUES {(word, data[word], 0)};""")
        self.connection.commit()

    @property
    def available_dictionaries(self) -> list[str]:
        self.cursor.execute(f"""SELECT name FROM sqlite_master
                               WHERE type='table';""")
        return [tup[0] for tup in self.cursor.fetchall()]

    def clear_user_db(self) -> None:
        """Removes all tables from user db. """
        if not self.available_dictionaries:
            return
        for table in self.available_dictionaries:
            self.drop_table(table)

    def copy_data_from_default_db(self, db_name: Path | str = _vocab_db_path) -> None:
        self.cursor.execute(f'ATTACH DATABASE "{db_name}" AS vocab;')
        dictionaries = self.cursor.execute("""SELECT name FROM vocab.sqlite_master
                                       WHERE type='table';""").fetchall()
        for table_name in dictionaries:
            self.create_table(table_name[0])
            self.cursor.execute(f"""INSERT INTO "{table_name[0]}"
                                    SELECT * FROM vocab."{table_name[0]}";""")
        self.connection.commit()
        self.cursor.execute("DETACH DATABASE vocab")
