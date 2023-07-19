import time
from pathlib import Path

from session_gui import SessionGui
from learning_data import LearningData
from repository import RepositoryProtocol
from settings import SessionSettings


PATH = Path.cwd() / "settings.json"
MAX_WORD_LENGTH = 60


class SessionControllerProtocol:
    def start_session(self, name: str):
        ...

    def handle_correct_answer(self):
        ...

    def handle_partially_correct_answer(self):
        ...

    def handle_incorrect_answer(self):
        ...

    def handle_submit(self, event=None):
        ...

    def manage_session_flow(self):
        ...

    def show_first_letter(self):
        ...


class SessionController:
    def __init__(
            self,
            gui: SessionGui,
            repository: RepositoryProtocol,
            learning_data: LearningData,
            handlers,
            settings: SessionSettings
    ):
        self.gui = gui
        self.repository = repository
        self.handlers = handlers
        self.settings = settings
        self.learning_data: LearningData = learning_data

    def start_session(self):
        self.learning_data.fill_in_session_list(self.settings.words_per_session)

        self.gui.create_special_letters_buttons(
            self.handlers.extract_special_letters(list(self.learning_data.dictionary.values())))
        self.gui.configure_ui(self)
        self.gui.display_word(self.learning_data.word)
        self.gui.mainloop()

    def handle_correct_answer(self):
        self.learning_data.update_score(1)
        self.gui.change_color_of_user_input_field(color="#00FF00")
        time.sleep(1)
        self.gui.clear_user_input_field()
        self.gui.change_color_of_user_input_field(("gray10", "#DCE4EE"))

    def handle_partially_correct_answer(self):
        self.gui.show_correct_answer(self.learning_data.correct_answer)
        time.sleep(self.settings.seconds)
        self.gui.clear_user_input_field()
        self.gui.clear_correct_answer_label()

    def handle_incorrect_answer(self):
        self.learning_data.update_score(-1)
        self.gui.show_correct_answer(self.learning_data.correct_answer)
        self.gui.change_color_of_user_input_field(color="red")
        time.sleep(self.settings.seconds)
        self.gui.change_color_of_user_input_field(("gray10", "#DCE4EE"))
        self.gui.clear_user_input_field()
        self.gui.clear_correct_answer_label()

    def handle_submit(self, event=None):
        result = self.handlers.evaluate_user_input(
            ignore_capitalization=self.settings.ignore_capitalization,
            ignore_punctuation=self.settings.ignore_punctuation,
            correct_answer=self.learning_data.correct_answer,
            user_input=self.gui.get_user_input
        )
        getattr(self, "handle_" + result)()
        self.manage_session_flow()

    def manage_session_flow(self):
        self.learning_data.pop_word()
        self.gui.step_progressbar()
        if self.learning_data.is_session_list_empty:
            self.gui.destroy()
            self.repository.update_dictionary(**self.learning_data.__dict__)
            return
        self.gui.display_word(self.learning_data.word)

    def show_first_letter(self):
        self.gui.insert_first_letter(self.learning_data.first_letter)

