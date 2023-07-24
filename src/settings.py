from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class AppSettings:
    __slots__ = ['DEFAULT_COLOR_THEME', 'LIGHT_THEME', 'DARK_THEME', 'LIGHT_THEME_HEADING', 'DARK_THEME_HEADING',
                 'LOCALE', 'DB_PATH', 'USER_SETTINGS_PATH', 'MAX_PHRASE_LENGTH', 'THRESHOLD', 'TRANSPOSITION_COST']
    DEFAULT_COLOR_THEME: str
    LIGHT_THEME: dict[str, str]
    DARK_THEME: dict[str, str]
    LIGHT_THEME_HEADING: dict[str, str]
    DARK_THEME_HEADING: dict[str, str]
    LOCALE: dict[str, str]
    DB_PATH: Path
    USER_SETTINGS_PATH: str
    MAX_PHRASE_LENGTH: int
    THRESHOLD: float
    TRANSPOSITION_COST: float | int


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
class SessionSettings:
    __slots__ = ["words_per_session", "ignore_capitalization", "ignore_punctuation", "seconds"]
    words_per_session: int
    ignore_capitalization: bool
    ignore_punctuation: bool
    seconds: int


