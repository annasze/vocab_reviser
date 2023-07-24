import json
from pathlib import Path


from src.settings import UserSettings, AppSettings
from src.handlers.new_dictionary_handler import NewDictHandlerForJSONRepo


def get_user_settings(file: str):
    settings_dict = json.loads(Path(file).read_text(encoding="utf-8"))
    return UserSettings(**settings_dict)


def get_app_settings(file: str):
    settings_dict = json.loads(Path(file).read_text(encoding="utf-8"))
    return AppSettings(**settings_dict)


def save_user_settings(settings_dict: dict[str, str], file: Path) -> None:
    with open(file, "w", encoding='utf-8') as settings_file:
        json.dump(settings_dict, settings_file, indent=4)


def get_data(
        name: str,
        taken_names: list[str],
        settings: AppSettings
) -> tuple[str, dict]:
    return (
        NewDictHandlerForJSONRepo(name, taken_names, settings.MAX_PHRASE_LENGTH)
        .validate_name(name)
        .set_file_path()
        .load_raw_file()
        .set_validated_data()
        .get_data()
    )
