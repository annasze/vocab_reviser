from dataclasses import dataclass, field
from pathlib import Path

from new_dictionary_handler import NewDictHandlerForJSONRepo


@dataclass
class SessionSettings:
    __slots__ = ["words_per_session", "ignore_capitalization", "ignore_punctuation", "seconds"]
    words_per_session: int
    ignore_capitalization: bool
    ignore_punctuation: bool
    seconds: int


@dataclass
class UserSettings:
    __slots__ = ["appearance_mode", "dictionary_name", "ignore_capitalization", "ignore_punctuation", "app_language",
                 "seconds", "textbox", "words_per_session", "show_info_chb", "app_language_versions",
                 "words_per_session_seg_btn", "seconds_seg_btn", "appearance_mode_om"]
    # user settings
    appearance_mode: str
    dictionary_name: str
    ignore_capitalization: bool
    ignore_punctuation: bool
    app_language: str
    seconds: int
    textbox: str
    words_per_session: int
    show_info_chb: bool
    app_language_versions: field(default_factory=list[str])
    words_per_session_seg_btn: field(default_factory=list[str])
    seconds_seg_btn: field(default_factory=list[str])
    appearance_mode_om: field(default_factory=list[str])


@dataclass
class AppSettings:
    DEFAULT_COLOR_THEME: str = "blue"
    LIGHT_THEME: dict[str, str] = field(default_factory=lambda: dict(background="gray86", foreground="black"))
    DARK_THEME: dict[str, str] = field(default_factory=lambda: dict(background="gray17", foreground="#DCE4EE"))
    LIGHT_THEME_HEADING: dict[str, str] = field(default_factory=lambda: dict(background="#3B8ED0", foreground="#DCE4EE"))
    DARK_THEME_HEADING: dict[str, str] = field(default_factory=lambda: dict(background="#1F6AA5", foreground="#DCE4EE"))
    LOCALE: dict[str, str] = field(default_factory=lambda: dict(polski="pl", English="en", español="es"))
    DB_PATH: Path = Path("json_db.json")
    USER_SETTINGS_PATH: str = Path("settings.json")
    MAX_PHRASE_LENGTH: int = 60
    NEW_DICT_HANDLER = NewDictHandlerForJSONRepo


settings = AppSettings()
