import random
from collections import Counter
from dataclasses import dataclass, field


@dataclass
class Model:
    """
        A class to store and manage the data when the app is run.
        ...

        Attributes
        ----------
        name: str
            name of the dictionary, same as in db
        dictionary: dict[str, str]
            a dict of word/frase: translation pairs

        scores: dict[str, int]
            a dict of word/frase: score pairs
            the score for a particular word/frase determines how often it appears
            in session.
        session_list: list[str]
            a queue containing a list of words/frases for current session. The words
            are popped from right one by one. Once it's empty, the session ends.
        special_letters: list[str]
            a list of non-ascii chars used in a dictionary, f.e. ["ą", 'ś", "ź", "ń"]
        session_dict: dict[str, int]
            a dict which stores all words from prev sessions and obtained scores
        scores_to_update, deleted_words, added_words: list[str]
            lists that keep track of all changes committed during the session,
            so that only the rows that changed are updated in the db and not the entire db.


        Methods
        described in methods __doc__
        -------
        """
    name: str = None
    dictionary: dict[str, str] = field(default_factory=dict)
    scores: Counter[str, int] = field(default_factory=Counter)
    session_list: list[str] = field(default_factory=list)
    special_letters: list[str] = field(default_factory=list)
    session_dict: dict[str, int] = field(default_factory=dict)
    scores_to_update: list[str, int] = field(default_factory=list)
    deleted_words: list[str] = field(default_factory=list)
    added_words: list[str] = field(default_factory=list)

    def create_session(self, words_per_session: int) -> None:
        """Fill in session_list. If there are enough words/frases to choose from,
        choose random sample from 2*sample least known words/frases."""
        if words_per_session * 2 >= len(self.dictionary):
            self.session_list = random.sample([elem[0] for elem in self.scores.most_common()[-2*words_per_session:]],
                                              words_per_session)
        else:
            self.session_list = random.sample(list(self.dictionary.keys()), words_per_session)

    def fill_in_session_dict(self) -> None:
        """Fill in session_dict."""
        self.session_dict = {word: 0 for word in self.session_list}

    def clear_scores_dict(self) -> None:
        """Clear scores on user's demand; update scores_to_update accordingly."""
        self.scores = Counter({k: 0 for k in self.dictionary})
        self.scores_to_update.extend([word for word in self.scores if word not in self.scores_to_update])

    def add_word_to_dictionary(self, word: str, translation: str) -> None:
        self.dictionary[word] = translation
        self.scores[word] = 0
        self.added_words.append(word)

    def remove_word_from_dictionary(self, word: str) -> None:
        self.dictionary.pop(word)
        self.scores.pop(word)
        self.deleted_words.append(word)

    def update(self, point: int) -> None:
        """Update the appropriates attributes when end user submits the answer"""
        self.scores[self.word] += point
        self.session_dict[self.word] += point
        if self.word not in self.scores_to_update:
            self.scores_to_update.append(self.word)

    @property
    def first_letter(self) -> str:
        return self.dictionary[self.session_list[-1]][0]

    @property
    def correct_answer(self) -> str:
        return self.dictionary[self.session_list[-1]]

    @property
    def word(self) -> str:
        return self.session_list[-1]

    @property
    def changes_made(self) -> bool:
        """Determine whether the db needs to be updated"""
        return self.scores_to_update or self.added_words or self.deleted_words









