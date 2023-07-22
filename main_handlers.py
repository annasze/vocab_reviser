import json
from pathlib import Path


from settings import settings, UserSettings


def get_user_settings(file: Path):
    settings_dict = json.loads(file.read_text(encoding="utf-8"))
    return UserSettings(**settings_dict)


def save_user_settings(settings_dict: dict[str, str], file: Path) -> None:
    with open(file, "w", encoding='utf-8') as settings_file:
        json.dump(settings_dict, settings_file, indent=4)


def get_data(
        name: str,
        taken_names: list[str],
        max_word_length: int = settings.MAX_PHRASE_LENGTH
) -> tuple[str, dict]:
    return (
        settings.NEW_DICT_HANDLER(name, taken_names, max_word_length)
        .validate_name(name)
        .set_file_path()
        .load_raw_file()
        .set_validated_data()
        .get_data()
    )
