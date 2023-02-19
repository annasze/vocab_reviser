from pathlib import Path
from tkinter.messagebox import showwarning, askyesnocancel, showinfo
from typing import Callable

from openpyxl.utils.exceptions import InvalidFileException

import correctness_checker
from models_handler import ModelsHandler
from settings import settings_functions
from view import View

_default_settings_path = Path.cwd() / "settings/default_settings.json"


class Controller:
    def __init__(self, models_handler: ModelsHandler, view: View):
        self.model = models_handler
        self.view = view

    # -------------------------------------------------------------------
    # handle start & exit
    # -------------------------------------------------------------------
    def start_app(self, name: str) -> None:
        """A function called at each initialization of the app."""
        # configure view
        self.view.set_commands(self)
        self.view.bind_events(self)
        # partially disable app if the is no data in the db
        if not name or name not in self.model.db.available_dictionaries:
            self.view.set_up_partially_disabled_ui()
        # load model
        else:
            self.model.create_model(name)
            self.view.update_fields_1(self.model.db.available_dictionaries,
                                      self.model.model.name)
            self.view.update_fields_2(self.model.model.dictionary)
        # start the loop
        self.view.start_main_loop()

    def exit_app(self) -> None:
        """A function called at each termination of the app."""
        # save settings file for the next initialization of the app
        settings_functions.save_settings_file(
            settings_dict=self.view.get_settings_dict())

        # if no changes to be committed to db, close the app
        if not self.model.model or not self.model.model.changes_made:
            self.view.destroy()
            return

        # ask on exit whether user wants to save changes
        user_choice = askyesnocancel(title=self.view.lang.exit,
                                     message=self.view.lang.message1)
        # user clicked 'yes'
        if user_choice:
            self.model.push_changes_to_db()

        # user clicked 'cancel'
        elif user_choice is None:
            return
        self.view.destroy()

    # -------------------------------------------------------------------
    # handle clicks - main window
    # -------------------------------------------------------------------
    def start(self, event=None) -> None:
        """A function called when the end user requests to start the session."""
        # fill in session list and dict
        self.model.model.create_session(
            words_per_session=self.view.words_per_session.get())
        self.model.model.fill_in_session_dict()

        # set up CTk session window
        self.view.set_up_session_view(
            special_letters=self.model.model.special_letters,
            word=self.model.model.word)
        self.view.session_view.configure_ui(self)
        self.view.show_session_list_btn.configure(state="normal")

    def switch_dictionary(self, chosen_dict) -> None:
        """ Switches dictionary on user's demand.
            Notifies self.view to update ui accordingly."""
        if self.model.model.changes_made:
            # ask whether user wants to save changes
            user_choice = askyesnocancel(title=self.view.lang.title1,
                                         message=self.view.lang.message1)
            if user_choice:  # user clicked 'yes'
                self.model.push_changes_to_db()
            elif user_choice is None:  # user clicked 'cancel'
                self.view.switch_dict_om.set(value=self.model.model.name)
                return
        # switch model
        self.model.create_model(name=chosen_dict)
        self.handle_words_per_session(value=self.view.words_per_session.get())
        self.view.show_session_list_btn.configure(state="disabled")
        self.update_remove_word_cb()
        self.view.update_placeholder_text()

    def remove_dictionary(self, chosen_dict: str) -> None:
        """ Removes dictionary on user's demand.
            Notifies self.model to update the db.
            Notifies self.view to update the ui."""
        # ask for confirmation
        if not askyesnocancel(
                title=self.view.lang.title2,
                message=self.view.lang.are_you_sure):
            return
        # update db
        self.model.db.drop_table(table_name=chosen_dict)

        # update fields
        self.view.update_fields_1(
            self.model.db.available_dictionaries,
            self.model.model.name)
        self.view.update_placeholder_text()

        # switch model if applicable
        if chosen_dict == self.model.model.name:
            self.switch_model_after_deletion()

    def add_new_dictionary(self, event=None):
        """ Adds new dictionary on user's demand.
            Notifies self.model to update the db.
            Notifies self.view to update the ui.
            Shows info to the user if no errors occur."""
        # set valid dict_name
        name = self.set_dict_name()
        if name == "ok":    # warning message popped up, user didn't enter first and/or second lang name
            return

        # get file path
        file_path = self.view.browse_file()
        if file_path is None:     # user clicked cancel or closed the window
            return

        # validate the data and add it to db
        if self.add_data_to_db(file_path, name) == "ok":    # warning message popped up, error during adding data
            return

        # show info that data has been successfully added
        showinfo(title=self.view.lang.success,
                 message=self.view.lang.message4.format(name))

        # enable widgets and create model if applicable
        if len(self.model.db.available_dictionaries) == 1:
            self.view.switch_widgets_state(state="normal")
            self.model.create_model(name)

        # clear entry fields, update option menus
        self.view.update_fields_1(self.model.db.available_dictionaries,
                                  self.model.model.name)

    def show_list(self):
        """Creates a TopLevel window (list of all words)."""
        self.view.set_up_list(dictionary=self.model.model.dictionary,
                              scores=self.model.model.scores,
                              title=self.view.lang.title_wordlist)

    def show_session_list(self):
        """Creates a TopLevel window (list of words from last session)."""
        self.view.set_up_list(dictionary=self.model.model.dictionary,
                              scores=self.model.model.session_dict,
                              title=self.view.lang.title_session_wordlist)

    def reset_points(self):
        """Resets scores dict on user's demand."""
        if askyesnocancel(title=self.view.lang.title5,
                          message=self.view.lang.are_you_sure):
            self.model.model.clear_scores_dict()

    def add_word(self, event=None):
        """Handles adding word to the current dict.
            Notifies self.model to update its model attribute.
            Notifies self.view to update the ui."""
        word = self.view.word_ent.get().strip()
        translation = self.view.translation_ent.get().strip()
        if not word or not translation:
            return

        elif word in self.model.model.dictionary:
            return showwarning(title=self.view.lang.error,
                               message=self.view.lang.message6.format(word))

        self.model.model.add_word_to_dictionary(word, translation)
        self.view.update_fields_2(self.model.model.dictionary.keys(), True)

        # bind <Return> to START button
        self.bind_return_event()

    def remove_word(self, event=None):
        """ Handles removing a word from the current dict.
            Notifies self.model to update its model attribute.
            Notifies self.view to update the ui.
            Updated words_per_session if necessary. """
        if not self.view.remove_word_var.get():
            return
        if len(self.model.model.dictionary) <= 10:
            return showwarning(title=self.view.lang.title3,
                               message=self.view.lang.message10)
        self.model.model.remove_word_from_dictionary(self.view.remove_word_var.get())
        self.view.update_fields_2(self.model.model.dictionary.keys())
        self.handle_words_per_session(value=self.view.words_per_session.get())
        self.bind_return_event()

    def factory_reset(self):
        """ Handles a factory reset.
            Notifies model to clear user_db, copy data from default_db and
            overwrite its model attribute.
            Notifies self.view to update the ui.
            Updated words_per_session if necessary. """

        if not askyesnocancel(title=self.view.lang.title3, message=self.view.lang.message7):
            return
        self.model.db.clear_user_db()
        self.model.db.copy_data_from_default_db()
        self.model.create_model(name=self.model.db.available_dictionaries[-1])

        self.view.configure_ui(
            settings=settings_functions.read_settings_file(file=_default_settings_path))
        self.view.enable_partially_disabled_ui(self)
        self.view.update_fields_1(self.model.db.available_dictionaries,
                                  self.model.model.name)
        self.update_remove_word_cb()
        self.handle_words_per_session(value=self.view.words_per_session.get())

    # -------------------------------------------------------------------
    # others
    # -------------------------------------------------------------------
    def handle_words_per_session(self, value: int) -> bool | None:
        """Adjusts words_per_session value after switching dictionary, so that
           it doesn't exceed the len of the current dictionary."""
        if value > len(self.model.model.dictionary):
            self.view.words_per_session.set(
                value=len(self.model.model.dictionary) // 10 * 10)
            return True

    def handle_words_per_session_with_info(self, value: int) -> str | None:
        """If the value chosen by the user is higher than the len
           of the user dict, rounds down the value and shows info."""
        if self.handle_words_per_session(value):
            showinfo(title=self.view.lang.title6, message=self.view.lang.message8)

    def switch_model_after_deletion(self):
        """Handles model switching after user removes the dictionary that was in use.
           Notifies self.model to retrieve data from any available table in user_db. If it's empty,
           notifies self.view to disable some of its features and shows warning to the end user."""
        available_models = self.model.db.available_dictionaries
        if available_models:
            self.model.create_model(name=available_models[-1])
            return
        # user deleted all dicts from db, disable widgets and show warning
        self.view.set_up_partially_disabled_ui()
        self.model.model = None
        return showwarning(title=self.view.lang.title3, message=self.view.lang.message2)

    def set_dict_name(self) -> str | Callable:
        """Notifies self.model to set a valid name for a new dictionary.
           Shows warning to the end user if applicable."""
        first_lang = self.view.first_lang_ent.get()
        second_lang = self.view.second_lang_ent.get()
        if not first_lang or not second_lang:
            return showwarning(title=self.view.lang.error,
                               message=self.view.lang.message3)
        return self.model.get_model_name(first_lang, second_lang)

    def add_data_to_db(self, path, dict_name) -> str | None:
        """Notifies self.model to create a new table in the db.
           Returns None if data has been successfully added.
           Otherwise, returns str (shows warning to the end user)"""
        try:
            data = self.model.validate_data(path)
            if data is None:    # too little data; must be at least 10 rows
                return showwarning(self.view.lang.title6,
                                   self.view.lang.message9)
            self.model.db.create_table(table_name=dict_name)
            self.model.db.insert_data(table_name=dict_name, data=data)
        except (ValueError, InvalidFileException):
            return showwarning(title=self.view.lang.error,
                               message=self.view.lang.message5)

    def bind_return_event(self, event=None):
        """ A helper function which binds <Return> event when necessary. """
        self.view.bind("<Return>", self.start)
        # unfocus current widget
        self.view.middle_frame.focus()

    def unbind_return_event(self, event=None):
        """ A helper function which unbinds <Return> event when necessary. """
        self.view.unbind("<Return>")

    def update_remove_word_cb(self, event=None):
        """ Updates combobox (in delete word tab) in order to display
            an up-to-date list of words/phrases to the end user. """
        curr_values = self.model.model.dictionary.keys()
        # end user didn't narrow the list, display all values
        if not self.view.remove_word_var.get():
            self.view.remove_word_cb.configure(values=curr_values)
        # narrow the list
        else:
            new_values = [word for word in curr_values if self.view.remove_word_var.get().lower() in word.lower()]
            self.view.remove_word_cb.configure(values=new_values)

    # -------------------------------------------------------------------
    # handle clicks - session window
    # -------------------------------------------------------------------
    def submit(self, event=None) -> None:
        """ Configures SessionView window once user clicks 'Submit'.
            Changes font color, shows correct answer if applicable,
            makes step in progressbar, updates model. """

        # do not proceed if user_input field is empty (accidental clicks,etc.)
        if not self.view.session_view.show_user_input:
            return

        # evaluate the answer
        dld, evaluation = correctness_checker.evaluate_user_input(
                            ignore_capitalization=self.view.ignore_capitalization.get(),
                            ignore_punctuation=self.view.ignore_punctuation.get(),
                            correct_answer=self.model.model.correct_answer,
                            user_input=self.view.session_view.show_user_input)

        if dld == 0:    # correct answer
            self.model.model.update(point=1)
            self.view.session_view.handle_user_input(seconds=1,
                                                     text_color="#00FF00")
        elif evaluation is True:    # minor mistake
            self.view.session_view.handle_user_input(seconds=self.view.seconds.get(),
                                                     text_color=("gray10", "#DCE4EE"),
                                                     correct_answer=self.model.model.correct_answer,
                                                     correct=False)
        else:    # incorrect answer
            self.model.model.update(point=-1)
            self.view.session_view.handle_user_input(seconds=self.view.seconds.get(),
                                                     text_color="red",
                                                     correct_answer=self.model.model.correct_answer,
                                                     correct=False)
        self.view.session_view.progressbar.step()
        self.view.session_view.submit_button.configure(state="disabled")

        self.manage_session_flow()

    def manage_session_flow(self) -> None:
        """ Terminates session once the session_list is empty. """
        self.model.model.session_list.pop()
        if len(self.model.model.session_list) > 0:
            self.view.session_view.displayed_word.set(
                self.model.model.word)
        else:
            self.view.session_view.destroy()

    def show_first_letter(self) -> None:
        """ Inserts first letter in user_input entry. """
        self.view.session_view.insert_first_letter(
            first_letter=self.model.model.first_letter)
        # change state of submit button as user input is no longer empty
        self.view.session_view.submit_button.configure(state="normal")
