from dataclasses import dataclass, field


@dataclass
class Settings:
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
