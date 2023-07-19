from dataclasses import dataclass


@dataclass
class SessionSettings:
    __slots__ = ["words_per_session", "ignore_capitalization", "ignore_punctuation", "seconds"]
    words_per_session: int
    ignore_capitalization: bool
    ignore_punctuation: bool
    seconds: int




