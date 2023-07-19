import random
from collections import Counter


class LearningData:
    def __init__(self, name: str, dictionary: dict[str, str], scores: dict[str, int]):
        self.name = name
        self.dictionary = dictionary
        self.scores = Counter(scores)
        self.session_list = None

    def fill_in_session_list(self, words_per_session: int):
        if words_per_session * 2 >= len(self.dictionary):
            self.session_list = random.sample([elem[0] for elem in self.scores.most_common()[-2*words_per_session:]],
                                              words_per_session)
        else:
            self.session_list = random.sample(list(self.dictionary.keys()), words_per_session)

    def add_word(self, word: str, translation: str) -> None:
        self.dictionary[word] = translation
        self.scores[word] = 0

    def remove_word(self, word: str) -> None:
        if not self.dictionary.get(word):
            return
        self.dictionary.pop(word)
        self.scores.pop(word)

    def update_score(self, point: int) -> None:
        self.scores[self.word] += point

    def clear_scores(self) -> None:
        self.scores = Counter({k: 0 for k in self.dictionary})

    def pop_word(self):
        self.session_list.pop()

    @property
    def is_session_list_empty(self):
        return not bool(self.session_list)

    @property
    def first_letter(self) -> str:
        return self.dictionary[self.session_list[-1]][0]

    @property
    def correct_answer(self) -> str:
        return self.dictionary[self.session_list[-1]]

    @property
    def word(self) -> str:
        return self.session_list[-1]
