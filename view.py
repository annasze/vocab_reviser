import tkinter.ttk as ttk
import time
from pathlib import Path
from tkinter import filedialog
from tkinter.messagebox import showinfo

import customtkinter as ctk

from settings.language_version import LanguageVersion
from settings import settings_functions

default_color_theme = "blue"


class View(ctk.CTk):
    def __init__(self, settings):
        super().__init__()
        # configure window
        self.title("Vocab Reviser")

        self.resizable(0, 0)
        #self.geometry("1600x900")
        
        width = 1000
        height = 600

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)

        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        
        #AM - Print the screen size - first display
        #print("Screen width:", screen_width)
        #print("Screen height:", screen_height)

        self.grid_columnconfigure([0, 2], weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.grid_columnconfigure([0, 2], weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.resizable(False, False)

        # create left frame with widgets
        self.left_frame = ctk.CTkFrame(self, corner_radius=0, width=200)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.manage_dicts_lb = ctk.CTkLabel(self.left_frame, font=ctk.CTkFont(size=14))
        self.manage_dicts_lb.grid(row=0, pady=20)
        self.switch_dict_lb = ctk.CTkLabel(self.left_frame)
        self.switch_dict_lb.grid(row=1, pady=(10, 5))
        self.switch_dict_om = ctk.CTkOptionMenu(self.left_frame, width=150, dynamic_resizing=False)
        self.switch_dict_om.grid(row=2, pady=(0, 20), padx=20)
        self.remove_dict_lb = ctk.CTkLabel(self.left_frame)
        self.remove_dict_lb.grid(row=3, pady=(20, 5))
        self.remove_dict_om = ctk.CTkOptionMenu(self.left_frame, width=150, dynamic_resizing=False)
        self.remove_dict_om.grid(row=4, pady=(0, 40), padx=20)
        self.add_new_dict_lb = ctk.CTkLabel(self.left_frame, width=150)
        self.add_new_dict_lb.grid(row=5, pady=5)
        self.first_lang_ent = ctk.CTkEntry(self.left_frame, width=150)
        self.first_lang_ent.grid(row=6, pady=(5, 10))
        self.second_lang_ent = ctk.CTkEntry(self.left_frame, width=150)
        self.second_lang_ent.grid(row=7, pady=(5, 10))
        self.browse_btn = ctk.CTkButton(self.left_frame, width=60)
        self.browse_btn.grid(row=8, sticky="e", padx=(0, 40), pady=(5, 10))
        self.show_info_var = ctk.BooleanVar()
        self.show_info_chb = ctk.CTkCheckBox(
            self.left_frame, variable=self.show_info_var, onvalue=True, offvalue=False,
            checkbox_width=15, checkbox_height=15, corner_radius=0, font=ctk.CTkFont(size=11))
        self.show_info_chb.grid(row=9, pady=5)

        # create right frame with widgets
        self.right_frame = ctk.CTkFrame(self, corner_radius=0, width=200)
        self.right_frame.grid(row=0, column=2, sticky="nsew")
        self.current_dict_lb = ctk.CTkLabel(self.right_frame, font=ctk.CTkFont(size=14))
        self.current_dict_lb.grid(row=0, pady=(25, 20))
        self.show_list_btn = ctk.CTkButton(self.right_frame, width=120)
        self.show_list_btn.grid(row=1, pady=10, padx=30)
        self.show_session_list_btn = ctk.CTkButton(self.right_frame, width=120, state="disabled")
        self.show_session_list_btn.grid(row=2, pady=10)
        self.reset_points = ctk.CTkButton(self.right_frame, width=120)
        self.reset_points.grid(row=3, pady=(10, 15))
        self.tabview = ctk.CTkTabview(self.right_frame, width=160, height=215)
        self.tabview.grid(row=4, sticky="ns", pady=15)
        self.tabview.add(name="+".center(5))
        self.tabview.add(name="-".center(5))
        self.add_word_lb = ctk.CTkLabel(self.tabview.tab(name="+".center(5)))
        self.add_word_lb.grid(row=0)
        self.word_ent = ctk.CTkEntry(self.tabview.tab(name="+".center(5)))
        self.word_ent.grid(row=1, pady=(15, 5))
        self.translation_ent = ctk.CTkEntry(self.tabview.tab(name="+".center(5)))
        self.translation_ent.grid(row=2, pady=5)
        self.add_word_btn = ctk.CTkButton(self.tabview.tab(name="+".center(5)), width=60)
        self.add_word_btn.grid(row=3, padx=20, pady=10, sticky="e")
        self.remove_word_lb = ctk.CTkLabel(self.tabview.tab(name="-".center(5)))
        self.remove_word_lb.grid(row=0, pady=(0, 10))
        self.remove_word_lb2 = ctk.CTkLabel(self.tabview.tab(name="-".center(5)), font=ctk.CTkFont(size=12))
        self.remove_word_lb2.grid(row=1, pady=(0, 5))
        self.remove_word_var = ctk.StringVar()
        self.remove_word_cb = ctk.CTkComboBox(self.tabview.tab(name="-".center(5)), variable=self.remove_word_var)
        self.remove_word_cb.grid(row=2, pady=(10, 5))
        self.confirm_btn = ctk.CTkButton(self.tabview.tab("-".center(5)), width=60)
        self.confirm_btn.grid(row=3, padx=20, pady=10, sticky="e")

        # create middle frame with widgets
        self.middle_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.middle_frame.grid(row=0, column=1, sticky="nsew")
        self.middle_frame.grid_columnconfigure(1, weight=0)
        self.middle_frame.grid_columnconfigure([0, 2], weight=1)
        self.logo_label = ctk.CTkLabel(self.middle_frame, text="Vocab Reviser",
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(column=1, row=0, pady=(50, 100))
        self.start_btn = ctk.CTkButton(self.middle_frame, width=200, height=50,
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.start_btn.grid(column=1, row=4)
        self.notes_lb = ctk.CTkLabel(self.middle_frame, font=ctk.CTkFont(size=14))
        self.notes_lb.grid(column=1, row=5, padx=(60, 0), pady=(40, 0), sticky="w")
        self.textbox = ctk.CTkTextbox(self.middle_frame, width=400, height=100)
        self.textbox.grid(column=1, row=6, padx=40, pady=(5, 15))
        self.save_to_file_btn = ctk.CTkButton(self.middle_frame, width=100)
        self.save_to_file_btn.grid(column=1, row=7, sticky="e", padx=(0, 90), pady=(0, 10))

        # create bottom frame with widgets
        self.bottom_frame = ctk.CTkFrame(self, corner_radius=0)
        self.bottom_frame.grid(column=0, columnspan=3, row=1, sticky="nsew", ipady=10)
        self.bottom_frame.grid_columnconfigure("all", weight=0)
        self.bottom_frame.grid_rowconfigure("all", weight=0)
        self.appearance_mode_lb = ctk.CTkLabel(self.bottom_frame)
        self.appearance_mode_lb.grid(column=0, row=0, padx=(25, 0), pady=(10, 0))
        self.appearance_mode_om = ctk.CTkOptionMenu(self.bottom_frame, width=100, dynamic_resizing=False)
        self.appearance_mode_om.grid(column=0, row=1, rowspan=2, padx=(25, 0))
        self.language_lb = ctk.CTkLabel(self.bottom_frame)
        self.language_lb.grid(column=1, row=0, padx=(25, 0), pady=(10, 0))
        self.current_app_language = ctk.CTkOptionMenu(self.bottom_frame, width=100, dynamic_resizing=False)
        self.current_app_language.grid(column=1, row=1, rowspan=2, padx=(25, 0))
        self.words_per_session_lb = ctk.CTkLabel(self.bottom_frame)
        self.words_per_session_lb.grid(column=2, row=0, padx=(25, 0), pady=(10, 0))
        self.words_per_session = ctk.IntVar()
        self.words_per_session_seg_btn = ctk.CTkSegmentedButton(self.bottom_frame, variable=self.words_per_session)
        self.words_per_session_seg_btn.grid(column=2, row=1, rowspan=2, padx=(25, 0))
        self.sec_lb = ctk.CTkLabel(self.bottom_frame)
        self.sec_lb.grid(row=0, column=4, padx=(25, 0), pady=(10, 0))
        self.seconds = ctk.IntVar()
        self.seconds_seg_btn = ctk.CTkSegmentedButton(self.bottom_frame, variable=self.seconds)
        self.seconds_seg_btn.grid(row=1, rowspan=2, column=4, padx=(25, 0))
        self.ignore_lb = ctk.CTkLabel(self.bottom_frame)
        self.ignore_lb.grid(column=5, row=0, padx=(25, 20), pady=(10, 0))
        self.ignore_capitalization = ctk.BooleanVar()
        self.capitalization_switch = ctk.CTkSwitch(self.bottom_frame, onvalue=True, offvalue=False,
                                                   variable=self.ignore_capitalization)
        self.capitalization_switch.grid(column=5, row=1, padx=(25, 20), sticky="w")
        self.ignore_punctuation = ctk.BooleanVar()
        self.punctuation_switch = ctk.CTkSwitch(self.bottom_frame, onvalue=True, offvalue=False,
                                                variable=self.ignore_punctuation)
        self.punctuation_switch.grid(column=5, row=2, padx=(25, 20), sticky="w")
        self.reset_btn = ctk.CTkButton(self.bottom_frame, width=70)
        self.reset_btn.grid(column=6, row=1, rowspan=2, padx=(25, 25))

        self.session_view = None
        self.word_list = None
        self.lang: LanguageVersion = settings_functions.read_lang_file(language=settings.app_language)

        self.configure_ui(settings=settings)
        self.set_app_language(lang=self.lang)
        self.update_placeholder_text()

    def configure_ui(self, settings) -> None:
        ctk.set_default_color_theme(default_color_theme)
        ctk.set_appearance_mode(settings.appearance_mode)
        self.words_per_session.set(value=settings.words_per_session)
        self.seconds.set(value=settings.seconds)
        self.ignore_capitalization.set(value=settings.ignore_capitalization)
        self.ignore_punctuation.set(value=settings.ignore_punctuation)
        self.textbox.delete("0.0", "end")
        self.textbox.insert(index="0.0", text=settings.textbox)
        self.switch_dict_om.set(value=settings.dictionary_name)
        self.remove_dict_om.set(value="----------")
        self.current_app_language.set(value=settings.app_language)
        self.show_info_var.set(value=settings.show_info_chb)
        self.current_app_language.configure(values=settings.app_language_versions)
        self.words_per_session_seg_btn.configure(values=settings.words_per_session_seg_btn)
        self.seconds_seg_btn.configure(values=settings.seconds_seg_btn)
        self.appearance_mode_om.configure(values=settings.appearance_mode_om)
        self.appearance_mode_om.set(value=settings.appearance_mode)

    def set_commands(self, controller):
        self.reset_points.configure(command=controller.reset_points)
        self.show_session_list_btn.configure(command=controller.show_session_list)
        self.add_word_btn.configure(command=controller.add_word)
        self.confirm_btn.configure(command=controller.remove_word)

        self.remove_dict_om.configure(command=controller.remove_dictionary)
        self.switch_dict_om.configure(command=controller.switch_dictionary)
        self.show_list_btn.configure(command=controller.show_list)
        self.browse_btn.configure(command=controller.add_new_dictionary)
        self.words_per_session_seg_btn.configure(command=controller.handle_words_per_session_with_info)
        self.save_to_file_btn.configure(command=self.save_textbox_data_to_file)
        self.current_app_language.configure(command=self.change_app_language)
        self.appearance_mode_om.configure(command=ctk.set_appearance_mode)
        self.show_info_chb.configure(command=self.handle_display_notification)
        self.reset_btn.configure(command=controller.factory_reset)

    def bind_events(self, controller):
        self.protocol("WM_DELETE_WINDOW", controller.exit_app)
        self.bind("<Return>", controller.start)
        self.start_btn.bind("<Button-1>", controller.start)
        self.textbox.bind('<Button-1>', controller.unbind_return_event)
        self.word_ent.bind('<Button-1>', controller.unbind_return_event)
        self.middle_frame.bind("<Button-1>", controller.bind_return_event)
        self.left_frame.bind("<Button-1>", controller.bind_return_event)
        self.right_frame.bind("<Button-1>", controller.bind_return_event)
        self.bottom_frame.bind("<Button-1>", controller.bind_return_event)
        self.remove_word_lb2.bind("<FocusIn>", controller.unbind_return_event)
        self.remove_word_lb2.bind("<Return>", controller.remove_word)
        self.translation_ent.bind("<FocusIn>", controller.unbind_return_event)
        self.translation_ent.bind("<Return>", controller.add_word)
        self.second_lang_ent.bind("<FocusIn>", controller.unbind_return_event)
        self.second_lang_ent.bind("<Return>", controller.add_new_dictionary)
        self.remove_word_cb.bind('<Leave>', controller.update_remove_word_cb)
        self.tabview.tab(name="-".center(5)).bind('<Enter>', controller.unbind_return_event)
        if self.show_info_var.get():
            self.first_lang_ent.bind("<Button-1>", self.show_info_add_word)

    def unbind_events(self) -> None:
        """Unbinds all events except for these related with adding new dict
           and closing the app"""
        self.unbind("<Return>")
        self.start_btn.unbind("<Button-1>")
        self.textbox.unbind('<Button-1>')
        self.word_ent.unbind('<Button-1>')
        self.middle_frame.unbind("<Button-1>")
        self.left_frame.unbind("<Button-1>")
        self.right_frame.unbind("<Button-1>")
        self.bottom_frame.unbind("<Button-1>")
        self.remove_word_lb2.unbind("<FocusIn>")
        self.remove_word_lb2.unbind("<Return>")
        self.translation_ent.unbind("<FocusIn>")
        self.translation_ent.unbind("<Return>")
        self.second_lang_ent.unbind("<FocusIn>")
        self.remove_word_cb.unbind('<Leave>')

    def set_app_language(self, lang):
        self.manage_dicts_lb.configure(text=lang.manage_dicts_lb)
        self.switch_dict_lb.configure(text=lang.switch_dict_lb)
        self.remove_dict_lb.configure(text=lang.remove_dict_lb)
        self.add_new_dict_lb.configure(text=lang.add_new_dict_lb)
        self.first_lang_ent.configure(placeholder_text=lang.first_lang_ent)
        self.second_lang_ent.configure(placeholder_text=lang.second_lang_ent)
        self.browse_btn.configure(text=lang.browse_btn)
        self.current_dict_lb.configure(text=lang.current_dict_lb)
        self.show_list_btn.configure(text=lang.show_list_btn)
        self.show_session_list_btn.configure(text=lang.show_session_list_btn)
        self.reset_points.configure(text=lang.reset_points)
        self.start_btn.configure(text=lang.start_btn)
        self.notes_lb.configure(text=lang.notes_lb)
        self.save_to_file_btn.configure(text=lang.save_to_file_btn)
        self.appearance_mode_lb.configure(text=lang.appearance_mode_lb)
        self.words_per_session_lb.configure(text=lang.words_per_session_lb)
        self.sec_lb.configure(text=lang.sec_lb)
        self.ignore_lb.configure(text=lang.ignore_lb)
        self.capitalization_switch.configure(text=lang.capitalization_switch)
        self.punctuation_switch.configure(text=lang.punctuation)
        self.language_lb.configure(text=lang.language_lb)
        self.add_word_btn.configure(text=lang.submit)
        self.remove_word_lb2.configure(text=lang.remove_word_lb2)
        self.add_word_lb.configure(text=lang.add_word_lb)
        self.remove_word_lb.configure(text=lang.remove_word_lb)
        self.show_info_chb.configure(text=lang.show_info_chb)
        self.reset_btn.configure(text=lang.reset_btn)
        self.confirm_btn.configure(text=lang.confirm)

    def update_placeholder_text(self):
        self.word_ent.configure(placeholder_text=self.get_languages_names()[0])
        self.translation_ent.configure(placeholder_text=self.get_languages_names()[1])

    def start_main_loop(self):
        # start the loop
        self.mainloop()

    def change_app_language(self, language):
        self.lang = settings_functions.read_lang_file(language=language)
        self.set_app_language(lang=self.lang)

    def set_up_partially_disabled_ui(self):
        self.switch_widgets_state(state="disabled")
        self.unbind_events()
        self.reset_btn.configure(fg_color="#116530")
        self.switch_dict_om.set(value="----------")
        self.show_session_list_btn.configure(state="disabled")

    def enable_partially_disabled_ui(self, controller):
        self.switch_widgets_state(state="normal")
        self.start_btn.bind("<Button-1>", controller.start)
        self.bind("<Return>", controller.start)
        self.reset_btn.configure(fg_color=('#3B8ED0', '#1F6AA5'))

    def switch_widgets_state(self, state: str):
        for widget in (
                self.switch_dict_om,
                self.remove_dict_om,
                self.show_list_btn,
                self.reset_points,
                self.start_btn,
                self.add_word_btn,
                self.word_ent,
                self.translation_ent,
                self.remove_word_lb2,
                self.words_per_session_seg_btn,
                self.remove_word_cb,
                self.confirm_btn
        ):
            widget.configure(state=state)

    def get_settings_dict(self) -> dict[str, str]:
        """get settings dict to set the same settings
        # during the next initialization of the app"""
        return {
            "appearance_mode": self.appearance_mode_om.get(),
            "dictionary_name": self.switch_dict_om.get(),
            "ignore_capitalization": self.ignore_capitalization.get(),
            "ignore_punctuation": self.ignore_punctuation.get(),
            "seconds": self.seconds.get(),
            "words_per_session": self.words_per_session.get(),
            "textbox": self.get_text_from_textbox(),
            "app_language": self.current_app_language.get(),
            "show_info_chb": self.show_info_var.get(),
            "app_language_versions": self.current_app_language.cget("values"),
            "words_per_session_seg_btn": self.words_per_session_seg_btn.cget("values"),
            "seconds_seg_btn": self.seconds_seg_btn.cget("values"),
            "appearance_mode_om": self.appearance_mode_om.cget("values")
        }

    # -------------------------------------------------------------------
    # handle Toplevel windows
    # -------------------------------------------------------------------
    def set_up_session_view(self, special_letters, word) -> None:
        if self.session_view:
            self.session_view.destroy()

        # set up the ctk window
        self.session_view = SessionView()
        self.session_view.create_special_letters_buttons(special_letters)
        self.session_view.set_app_language(self.lang)
        self.session_view.grab_set()
        # display first word
        self.session_view.displayed_word.set(word)

    def set_up_list(self, dictionary: dict[str, str], scores: dict[str, int],
                    title: str, str_len_limit: int):
        # load headings
        first_language, second_language = self.get_languages_names()
        headings = [self.lang.nr,
                    first_language,
                    second_language,
                    self.lang.points]

        # create WordList instance
        self.word_list = WordList(title=title)
        self.word_list.fill_in_tree(dictionary, scores, headings, length=str_len_limit)

        # set style accordingly to current appearance mode
        appearance_mode = self.appearance_mode_om.get()
        self.word_list.style.configure("Treeview", **self.word_list.themes[appearance_mode])
        self.word_list.tree.tag_configure('custom_heading', **self.word_list.heading_theme[appearance_mode])

    def get_languages_names(self) -> tuple[str, str]:
        first_language, second_language = self.switch_dict_om.get().split(sep="-")
        first_language = first_language.capitalize()
        second_language = second_language.capitalize()
        # if dictionary_name is of type "English-Spanish_2", truncate "_2"
        if not second_language.isalpha():
            second_language = "".join(char for char in second_language if char.isalpha())
        return first_language, second_language

    # -------------------------------------------------------------------
    # other
    # -------------------------------------------------------------------

    def update_fields_1(self, available_dicts: list[str], current_dict: str) -> None:
        # updates fields after adding new dict or removing a dict
        self.switch_dict_om.configure(values=available_dicts)
        self.switch_dict_om.set(value=current_dict)
        self.remove_dict_om.configure(values=available_dicts)
        self.remove_dict_om.set(value="----------")
        if self.first_lang_ent.get():
            self.first_lang_ent.delete(0, ctk.END)
        if self.second_lang_ent.get():
            self.second_lang_ent.delete(0, ctk.END)

    def update_fields_2(self, words: list[str], add: bool = False):
        # updates fields after adding new word or removing a word
        self.remove_word_var.set(value="")
        self.remove_word_cb.configure(values=words)
        if add:
            self.word_ent.delete(0, ctk.END)
            self.translation_ent.delete(0, ctk.END)

    def save_textbox_data_to_file(self) -> None:
        file = filedialog.asksaveasfilename(title="Save as",
                                            defaultextension=".txt",
                                            filetypes=(("txt files", "*.txt*"),)
                                            )
        if not file:
            return
        with open(file, "w", encoding="UTF-8") as file:
            file.write(self.get_text_from_textbox())

    def get_text_from_textbox(self):
        return self.textbox.get("0.0", "end").strip("\n")

    @staticmethod
    def browse_file() -> Path | None:
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File",
                                              filetypes=(("xls files", "*.xls*"),
                                                         ("all files", "*.*"))
                                              )
        return None if not filename else Path(filename)

    def show_info_add_word(self, event=None):
        return showinfo(title=self.lang.title4, message=self.lang.message_add_word)

    def handle_display_notification(self):
        if self.show_info_var.get():
            self.first_lang_ent.bind("<Button-1>", self.show_info_add_word)
        else:
            self.first_lang_ent.unbind("<Button-1>")


class SessionView(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.geometry("600x380+300+300")

        # create main frame with widgets
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(column=0, row=0)
        self.progressbar = ctk.CTkProgressBar(self.main_frame)
        self.progressbar.grid(row=0, pady=(10, 40))
        self.displayed_word = ctk.StringVar()
        self.word_label = ctk.CTkLabel(self.main_frame, textvariable=self.displayed_word,
                                       width=600, font=ctk.CTkFont(size=20))
        self.word_label.grid(row=1, pady=(0, 50))
        self.corr_ans = ctk.StringVar()
        self.correct_ans_lb = ctk.CTkLabel(self.main_frame, textvariable=self.corr_ans,
                                           width=500, font=ctk.CTkFont(size=18), text_color="#00FF00")
        self.correct_ans_lb.grid(row=2, pady=(0, 25))
        self.user_input = ctk.CTkEntry(self.main_frame, width=400, font=ctk.CTkFont(size=18), justify=ctk.CENTER)
        self.user_input.grid(row=3, pady=(0, 25))
        self.special_letters_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.special_letters_frame.grid(column=0, row=1, pady=(0, 20), padx=20)
        self.lower_buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.lower_buttons_frame.grid(column=0, row=2, pady=(0, 20))
        self.clear_button = ctk.CTkButton(self.lower_buttons_frame, width=80)
        self.clear_button.grid(column=0, row=0, padx=25)
        self.show_first_letter_button = ctk.CTkButton(self.lower_buttons_frame, width=80)
        self.show_first_letter_button.grid(column=1, row=0, padx=(0, 25))
        self.submit_button = ctk.CTkButton(self.lower_buttons_frame, width=80, state="disabled")
        self.submit_button.grid(column=2, row=0, padx=(0, 25))

    def configure_ui(self, controller):
        self.progressbar.set(value=0)
        self.progressbar.configure(determinate_speed=50 / controller.view.words_per_session.get())
        self.show_first_letter_button.configure(command=controller.show_first_letter)
        self.clear_button.configure(command=self.clear_user_input_field)
        self.submit_button.bind('<Button-1>', controller.submit)
        self.bind('<Return>', controller.submit)
        self.bind('<Key>', self.change_state_of_submit_btn)
        self.bind('<Motion>', self.change_state_of_submit_btn)

    def set_app_language(self, lang):
        self.clear_button.configure(text=lang.clear_button_session_window)
        self.show_first_letter_button.configure(text=lang.show_first_letter_button_session_window)
        self.submit_button.configure(text=lang.submit)
        self.title(lang.title_session_window)

    def create_special_letters_buttons(self, special_letters: list[str]) -> None:
        for i in range(len(special_letters)):
            ctk.CTkButton(master=self.special_letters_frame,
                          text=f"{special_letters[i]}",
                          command=lambda i=i: self.user_input.insert(self.user_input.index(ctk.INSERT),
                                                                     special_letters[i]),
                          font=ctk.CTkFont(size=14),
                          width=40
                          ).grid(column=i, row=0, padx=5)

    def handle_user_input(self, seconds: str, text_color: str | tuple[str], correct: bool = True,
                          correct_answer: str | None = None) -> None:
        if not correct:
            self.corr_ans.set(correct_answer)
            self.correct_ans_lb.focus()
        self.user_input.configure(text_color=text_color)
        self.user_input.update()
        time.sleep(seconds)
        self.user_input.delete(0, "end")
        self.corr_ans.set("")
        self.user_input.configure(text_color=("gray10", "#DCE4EE"))
        self.user_input.focus()

    def clear_user_input_field(self):
        self.user_input.delete(0, "end")
        self.user_input.focus()

    def insert_first_letter(self, first_letter):
        self.user_input.delete(0, "end")
        self.user_input.insert(0, first_letter)
        self.user_input.focus()

    @property
    def show_user_input(self):
        return self.user_input.get()

    def change_state_of_submit_btn(self, event=None):
        self.user_input.focus()
        if self.user_input.get():
            self.submit_button.configure(state="normal")
        else:
            self.submit_button.configure(state="disabled")


class WordList(ctk.CTkToplevel):
    def __init__(self, title: str):
        super().__init__()
        self.title(title)
        self.resizable(False, False)

        # create and configure ttk style
        self.style = ttk.Style()
        self.style.configure("Treeview", font=("Arial", 13), rowheight=40, border_color="yellow")

        self.themes = {
            "Dark": {"background": 'gray17', "foreground": "#DCE4EE"},
            "Light": {"background": 'gray86', "foreground": "black"}
        }
        self.heading_theme = {
            "Dark": {"background": '#1F6AA5', "foreground": "#DCE4EE"},
            "Light": {"background": '#3B8ED0', "foreground": "#DCE4EE"}
        }

        # create widgets
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical")
        self.scrollbar.pack(expand=False, fill="y", side="right")

        self.tree = ttk.Treeview(self, columns=("#1", "#2", "#3", "#4"), show='',
                                 yscrollcommand=self.scrollbar.set)
        self.tree.column("#1", anchor="center", width=70, stretch="no")
        self.tree.column("#2", anchor="w", width=270, stretch="yes")
        self.tree.column("#3", anchor="w", width=270, stretch="yes")
        self.tree.column("#4", anchor="center", width=70, stretch='no')
        self.tree.tag_configure('custom_heading', font=("Arial", 13, "bold"))
        self.tree.pack(fill="both", side="left")
        self.scrollbar.configure(command=self.tree.yview)
        self.grab_set()

    def fill_in_tree(self, dictionary: dict[str, str], scores: dict[str, int],
                     headings: list[str], length: int):
        # create custom heading
        self.tree.insert("", "end", values=headings, tags='custom_heading')

        # sort by scores
        scores_sorted = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # fill the tree in with data
        for i, (word, point) in enumerate(scores_sorted, start=1):
            self.tree.insert("", "end", values=(
                f"{i}.",
                self.divide_frase(word, length),
                self.divide_frase(dictionary[word], length),
                str(point)))

    @staticmethod
    def divide_frase(frase: str, length: int):
        if len(frase) < length:
            return frase
        prev_inx, curr_inx = -1, 0
        while curr_inx < length:
            curr_inx = frase.find(" ", prev_inx + 1)
            if curr_inx >= length or curr_inx < prev_inx:
                curr_inx = prev_inx
                break
            prev_inx = curr_inx

        return frase[:curr_inx] + "\n" + frase[curr_inx + 1:]
