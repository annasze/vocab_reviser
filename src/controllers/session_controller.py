import time

from src.GUIs.session_gui import SessionGui
from src.data.learning_data import LearningData
from src.data.repository import RepositoryProtocol
from src.settings import SessionSettings, AppSettings


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
            session_settings: SessionSettings,
            app_settings: AppSettings
    ):
        self.gui = gui
        self.repository = repository
        self.handlers = handlers
        self.session_settings = session_settings
        self.app_settings = app_settings
        self.learning_data: LearningData = learning_data

    def start_session(self):
        self.learning_data.fill_in_session_list(self.session_settings.words_per_session)
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
        self.gui.change_color_of_user_input_field(tuple(self.app_settings.DARK_THEME.values()))

    def handle_partially_correct_answer(self):
        self.gui.show_correct_answer(self.learning_data.correct_answer)
        time.sleep(self.session_settings.seconds)
        self.gui.clear_user_input_field()
        self.gui.clear_correct_answer_label()

    def handle_incorrect_answer(self):
        self.learning_data.update_score(-1)
        self.gui.show_correct_answer(self.learning_data.correct_answer)
        self.gui.change_color_of_user_input_field(color="red")
        time.sleep(self.session_settings.seconds)
        self.gui.change_color_of_user_input_field(tuple(self.app_settings.DARK_THEME.values()))
        self.gui.clear_user_input_field()
        self.gui.clear_correct_answer_label()

    def handle_submit(self, event=None):
        self.gui.disable_submit_btn()
        result = self.handlers.evaluate_user_input(
            ignore_capitalization=self.session_settings.ignore_capitalization,
            ignore_punctuation=self.session_settings.ignore_punctuation,
            correct_answer=self.learning_data.correct_answer,
            user_input=self.gui.get_user_input,
            transposition_cost=self.app_settings.TRANSPOSITION_COST,
            threshold=self.app_settings.THRESHOLD
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
