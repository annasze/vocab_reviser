import json
from pathlib import Path

from settings.language_version import LanguageVersion
from settings.settings import Settings


__settings_path = Path.cwd() / "settings/settings.json"
__lang_path = Path.cwd() / "settings/lang.json"


def read_lang_file(language: str, file: Path = __lang_path) -> LanguageVersion:
    lang_dict = json.loads(file.read_text(encoding="utf-8"))
    return LanguageVersion(**lang_dict[language])


def read_settings_file(file: Path = __settings_path) -> Settings:
    settings_dict = json.loads(file.read_text(encoding="utf-8"))
    return Settings(**settings_dict)


def save_settings_file(settings_dict: dict[str, str], file: Path = __settings_path) -> None:
    with open(file, "w", encoding='utf-8') as settings:
        json.dump(settings_dict, settings, indent=4)


@property
def load_available_language_versions() -> list[str]:
    lang_dict = json.loads(__lang_path.read_text(encoding="utf-8"))
    return list(lang_dict.keys())

