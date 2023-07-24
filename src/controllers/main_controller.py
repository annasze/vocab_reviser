from tkinter import Event
from typing import Optional
import i18n
from openpyxl.utils.exceptions import InvalidFileException

from src.handlers import session_handlers
from src.data.learning_data import LearningData
from src.GUIs.list_gui import WordList
from src.GUIs.main_gui import MainGui
from src.data.repository import RepositoryProtocol
from src.controllers.session_controller import SessionController
from src.GUIs.session_gui import SessionGui
from src.settings import AppSettings, SessionSettings


class MainController:
    def __init__(self, gui: MainGui, repository: RepositoryProtocol, handlers, settings: AppSettings):
        self.session_controller = None
        self.gui = gui
        self.repository = repository
        self.learning_data: LearningData = None
        self.handlers = handlers
        self.settings = settings

    def start_app(self, name: Optional[str] = None):
        if name not in self.repository.available_dictionaries:
            name = self.repository.available_dictionaries[0]
        self.learning_data = LearningData(name=name, **self.repository.get_dictionary(name))
        self.update_widgets()
        self.gui.set_commands(self)
        self.gui.bind_events(self)
        self.change_word_per_session()

        self.gui.mainloop()

    def exit_app(self):
        self.handlers.save_user_settings(self.gui.settings, self.settings.USER_SETTINGS_PATH)
        self.repository.update_dictionary(
            name=self.learning_data.name,
            dictionary=self.learning_data.dictionary,
            scores=self.learning_data.scores
        )
        self.gui.destroy()

    def create_session(self, event=None):
        self.session_controller = SessionController(
            gui=SessionGui(),
            repository=self.repository,
            learning_data=self.learning_data,
            handlers=session_handlers,
            session_settings=SessionSettings(**self.gui.session_settings),
            app_settings=self.settings
        )
        self.session_controller.start_session()

    def add_new_dictionary(self, event=None):
        try:
            # get_validated_data
            data = self.handlers.get_data(
                name=self.gui.new_dictionary_name,
                taken_names=self.repository.available_dictionaries,
                settings=self.settings
            )
            # add data to db
            self.repository.add_dictionary(**data)

            self.gui.show_info(title="success", message="added")
            self.update_widgets()
        except (ValueError, InvalidFileException):
            return self.gui.show_error(title="error", message="error_loading_file")

    def remove_dictionary(self, name: str):
        if len(self.repository.available_dictionaries) == 1:
            return self.gui.show_error(title="error", message="forbidden")
        if not self.gui.get_user_confirmation(i18n.t("remove_dict_lb")):
            return
        self.repository.delete_dictionary(name)
        # restart the app
        self.start_app()

    def switch_dictionary(self, name: str):
        self.start_app(name)

    def add_word(self, event=None):
        self.learning_data.add_word(**self.gui.word_to_add)
        self.update_widgets()

    def remove_word(self, event=None):
        self.learning_data.remove_word(self.gui.word_to_remove)
        self.update_widgets()
        self.change_word_per_session()

    def reset_scores(self):
        if not self.gui.get_user_confirmation(i18n.t("reset_scores")):
            return
        self.learning_data.clear_scores()
        self.repository.update_dictionary(**self.learning_data.__dict__)

    def change_word_per_session(self, unused_value: Optional[int] = None):
        max_len = len(self.learning_data.dictionary)
        if self.gui.words_per_session > max_len:
            self.gui.change_words_per_session_value(max_len // 10 * 10)

    def update_widgets(self):
        self.gui.update_widgets(
            self.repository.available_dictionaries,
            self.learning_data.name,
            self.learning_data.all_words
        )

    def show_word_list(self):
        word_list = WordList()
        word_list.fill_in_tree(self.learning_data.dictionary, self.learning_data.scores, self.settings.MAX_PHRASE_LENGTH//2)
        word_list.configure_style(self.gui.appearance_mode, self.settings)

    def change_app_language(self, language: str):
        i18n.set("locale", self.settings.LOCALE[language])
        self.gui.set_texts()

    def filter_remove_word_combobox(self, event: Event):
        if not hasattr(self.gui, "filter_remove_word_combobox"):
            return
        if value := event.widget.get():
            self.gui.filter_remove_word_combobox(list(filter(lambda word: value in word, self.learning_data.all_words)))
        else:
            self.gui.filter_remove_word_combobox(self.learning_data.all_words)

    def bind_return_event(self, event=None):
        self.gui.bind("<Return>", self.create_session)
        self.gui.unfocus_current_widget()

    def unbind_return_event(self, event=None):
        self.gui.unbind("<Return>")


