from tkinter.messagebox import askyesnocancel, showerror, showinfo
from typing import Protocol

import customtkinter as ctk
import i18n


class MainGuiProtocol(Protocol):
    def set_texts(self) -> None:
        ...

    def configure_ui(self, user_settings) -> None:
        ...

    def set_commands(self, controller):
        ...

    def bind_events(self, controller):
        ...

    def update_widgets(self, available_dicts: list[str], current_dict: str, words: list[str]) -> None:
        ...

    @property
    def settings(self) -> dict[str, str]:
        ...

    @property
    def session_settings(self):
        ...

    def change_words_per_session_value(self, new_value):
        ...

    @staticmethod
    def get_user_confirmation(title: str):
        ...

    @staticmethod
    def show_error(title: str, message: str):
        ...

    @staticmethod
    def show_info(title: str, message: str):
        ...

    def unfocus_current_widget(self):
        ...

    def start_main_loop(self):
        ...

    @property
    def word_to_add(self):
        ...

    @property
    def word_to_remove(self):
        ...

    @property
    def new_dictionary_name(self):
        ...

    @property
    def words_per_session(self):
        ...

    @property
    def appearance_mode(self):
        ...


class MainGui(ctk.CTk):
    def __init__(self):
        super().__init__()
        # configure window
        self.title("Vocab Reviser")
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
        self.new_dict_name = ctk.CTkEntry(self.left_frame, width=150)
        self.new_dict_name.grid(row=7, pady=(5, 10))
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
        self.reset_scores = ctk.CTkButton(self.right_frame, width=120)
        self.reset_scores.grid(row=3, pady=(10, 15))
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

        # create bottom frame with widgets
        self.bottom_frame = ctk.CTkFrame(self, corner_radius=0)
        self.bottom_frame.grid(column=0, columnspan=3, row=1, sticky="nsew", ipady=10)
        self.bottom_frame.grid_columnconfigure("all", weight=0)
        self.bottom_frame.grid_rowconfigure("all", weight=0)
        self.appearance_mode_lb = ctk.CTkLabel(self.bottom_frame)
        self.appearance_mode_lb.grid(column=0, row=0, padx=(25, 0), pady=(10, 0))
        self.appearance_mode_om = ctk.CTkOptionMenu(self.bottom_frame, width=110, dynamic_resizing=False)
        self.appearance_mode_om.grid(column=0, row=1, rowspan=2, padx=(25, 0))
        self.language_lb = ctk.CTkLabel(self.bottom_frame)
        self.language_lb.grid(column=1, row=0, padx=(25, 0), pady=(10, 0))
        self.current_app_language = ctk.CTkOptionMenu(self.bottom_frame, width=110, dynamic_resizing=False)
        self.current_app_language.grid(column=1, row=1, rowspan=2, padx=(25, 0))
        self.words_per_session_lb = ctk.CTkLabel(self.bottom_frame)
        self.words_per_session_lb.grid(column=2, row=0, padx=(100, 0), pady=(10, 0))
        self.words_per_session_var = ctk.IntVar()
        self.words_per_session_seg_btn = ctk.CTkSegmentedButton(self.bottom_frame, variable=self.words_per_session_var,
                                                                width=130, dynamic_resizing=False)
        self.words_per_session_seg_btn.grid(column=2, row=1, rowspan=2, padx=(100, 0))
        self.sec_lb = ctk.CTkLabel(self.bottom_frame)
        self.sec_lb.grid(row=0, column=4, padx=(25, 0), pady=(10, 0))
        self.seconds = ctk.IntVar()
        self.seconds_seg_btn = ctk.CTkSegmentedButton(self.bottom_frame, variable=self.seconds, width=130,
                                                      dynamic_resizing=False)
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
        self.set_texts()

    def set_texts(self) -> None:
        self.manage_dicts_lb.configure(text=i18n.t("main.manage_dicts_lb"))
        self.switch_dict_lb.configure(text=i18n.t("main.switch_dict_lb"))
        self.remove_dict_lb.configure(text=i18n.t("main.remove_dict_lb"))
        self.add_new_dict_lb.configure(text=i18n.t("main.add_new_dict_lb"))
        self.new_dict_name.configure(placeholder_text=i18n.t("main.new_dict_name"))
        self.browse_btn.configure(text=i18n.t("main.browse_btn"))
        self.current_dict_lb.configure(text=i18n.t("main.current_dict_lb"))
        self.show_list_btn.configure(text=i18n.t("main.show_list_btn"))
        self.reset_scores.configure(text=i18n.t("main.reset_scores"))
        self.start_btn.configure(text=i18n.t("main.start_btn"))
        self.notes_lb.configure(text=i18n.t("main.notes_lb"))
        self.appearance_mode_lb.configure(text=i18n.t("main.appearance_mode_lb"))
        self.words_per_session_lb.configure(text=i18n.t("main.words_per_session_lb"))
        self.sec_lb.configure(text=i18n.t("main.sec_lb"))
        self.ignore_lb.configure(text=i18n.t("main.ignore_lb"))
        self.capitalization_switch.configure(text=i18n.t("main.capitalization_switch"))
        self.punctuation_switch.configure(text=i18n.t("main.punctuation"))
        self.language_lb.configure(text=i18n.t("main.language_lb"))
        self.add_word_btn.configure(text=i18n.t("main.submit"))
        self.remove_word_lb2.configure(text=i18n.t("main.remove_word_lb2"))
        self.add_word_lb.configure(text=i18n.t("main.add_word_lb"))
        self.remove_word_lb.configure(text=i18n.t("main.remove_word_lb"))
        self.word_ent.configure(placeholder_text=i18n.t("main.your_lang"))
        self.translation_ent.configure(placeholder_text=i18n.t("main.foreign_lang"))
        self.show_info_chb.configure(text=i18n.t("main.show_info_chb"))
        self.confirm_btn.configure(text=i18n.t("main.confirm"))

    def configure_ui(self, user_settings, app_settings) -> None:
        ctk.set_default_color_theme(app_settings.DEFAULT_COLOR_THEME)
        ctk.set_appearance_mode(user_settings.appearance_mode)
        self.words_per_session_var.set(value=user_settings.words_per_session)
        self.seconds.set(value=user_settings.seconds)
        self.ignore_capitalization.set(value=user_settings.ignore_capitalization)
        self.ignore_punctuation.set(value=user_settings.ignore_punctuation)
        self.textbox.delete("0.0", "end")
        self.textbox.insert(index="0.0", text=user_settings.textbox)
        self.switch_dict_om.set(value=user_settings.dictionary_name)
        self.remove_dict_om.set(value="----------")
        self.current_app_language.set(value=user_settings.app_language)
        self.show_info_var.set(value=user_settings.show_info_chb)
        self.current_app_language.configure(values=user_settings.app_language_versions)
        self.words_per_session_seg_btn.configure(values=user_settings.words_per_session_seg_btn)
        self.seconds_seg_btn.configure(values=user_settings.seconds_seg_btn)
        self.appearance_mode_om.configure(values=user_settings.appearance_mode_om)
        self.appearance_mode_om.set(value=user_settings.appearance_mode)

    def set_commands(self, controller):
        self.reset_scores.configure(command=controller.reset_scores)
        self.add_word_btn.configure(command=controller.add_word)
        self.current_app_language.configure(command=controller.change_app_language)
        self.appearance_mode_om.configure(command=ctk.set_appearance_mode)
        self.remove_dict_om.configure(command=controller.remove_dictionary)
        self.switch_dict_om.configure(command=controller.switch_dictionary)
        self.browse_btn.configure(command=controller.add_new_dictionary)
        self.show_list_btn.configure(command=controller.show_word_list)
        self.words_per_session_seg_btn.configure(command=controller.change_word_per_session)

    def bind_events(self, controller):
        self.protocol("WM_DELETE_WINDOW", controller.exit_app)
        self.bind("<Return>", controller.create_session)
        self.start_btn.bind("<Button-1>", controller.create_session)
        self.textbox.bind('<Button-1>', controller.unbind_return_event)
        self.word_ent.bind('<Button-1>', controller.unbind_return_event)
        self.middle_frame.bind("<Button-1>", controller.bind_return_event)
        self.left_frame.bind("<Button-1>", controller.bind_return_event)
        self.right_frame.bind("<Button-1>", controller.bind_return_event)
        self.bottom_frame.bind("<Button-1>", controller.bind_return_event)
        self.remove_word_lb2.bind("<FocusIn>", controller.unbind_return_event)
        self.remove_word_lb2.bind("<Return>", controller.remove_word)
        self.remove_word_cb.bind('<Leave>', controller.filter_remove_word_combobox)
        self.confirm_btn.bind("<Button-1>", controller.remove_word)
        self.translation_ent.bind("<FocusIn>", controller.unbind_return_event)
        self.translation_ent.bind("<Return>", controller.add_word)
        self.new_dict_name.bind("<FocusIn>", controller.unbind_return_event)
        self.new_dict_name.bind("<Return>", controller.add_new_dictionary)
        self.tabview.tab(name="-".center(5)).bind('<Enter>', controller.unbind_return_event)
        self.new_dict_name.bind("<Button-1>", self.show_notification_for_new_dictionary)

    def update_widgets(self, available_dicts: list[str], current_dict: str, words: list[str]) -> None:
        self.switch_dict_om.configure(values=available_dicts)
        self.switch_dict_om.set(value=current_dict)
        self.remove_dict_om.configure(values=available_dicts)
        self.remove_dict_om.set(value="----------")
        if self.new_dict_name.get():
            self.new_dict_name.delete(0, ctk.END)
        self.remove_word_var.set(value="")
        self.remove_word_cb.configure(values=words)
        if self.word_ent.get():
            self.word_ent.delete(0, ctk.END)
        if self.translation_ent.get():
            self.translation_ent.delete(0, ctk.END)

    @property
    def settings(self) -> dict[str, str]:
        return {
            "appearance_mode": self.appearance_mode_om.get(),
            "dictionary_name": self.switch_dict_om.get(),
            "ignore_capitalization": self.ignore_capitalization.get(),
            "ignore_punctuation": self.ignore_punctuation.get(),
            "seconds": self.seconds.get(),
            "words_per_session": self.words_per_session_var.get(),
            "textbox": self.textbox.get("0.0", "end").strip("\n"),
            "app_language": self.current_app_language.get(),
            "show_info_chb": self.show_info_var.get(),
            "app_language_versions": self.current_app_language.cget("values"),
            "words_per_session_seg_btn": self.words_per_session_seg_btn.cget("values"),
            "seconds_seg_btn": self.seconds_seg_btn.cget("values"),
            "appearance_mode_om": self.appearance_mode_om.cget("values")
        }

    @property
    def session_settings(self):
        return {
            "seconds": self.seconds.get(),
            "words_per_session": self.words_per_session_var.get(),
            "ignore_capitalization": self.ignore_capitalization.get(),
            "ignore_punctuation": self.ignore_punctuation.get(),
        }

    def change_words_per_session_value(self, new_value):
        self.words_per_session_var.set(value=new_value)

    @staticmethod
    def get_user_confirmation(title: str):
        return askyesnocancel(title=i18n.t("main.%s" % title), message=i18n.t("main.are_you_sure"))

    @staticmethod
    def show_error(title: str, message: str):
        return showerror(title=i18n.t("main.%s" % title), message=i18n.t("main.%s" % message))

    @staticmethod
    def show_info(title: str, message: str):
        return showinfo(title=i18n.t("main.%s" % title), message=i18n.t("main.%s" % message))

    def unfocus_current_widget(self):
        self.middle_frame.focus()

    def start_main_loop(self):
        # start the loop
        self.mainloop()

    @property
    def word_to_add(self):
        return dict(
            word=self.word_ent.get().strip(),
            translation=self.translation_ent.get().strip()
        )

    @property
    def word_to_remove(self):
        return self.remove_word_var.get().strip()

    @property
    def new_dictionary_name(self):
        return self.new_dict_name.get()

    @property
    def words_per_session(self):
        return self.words_per_session_var.get()

    @property
    def appearance_mode(self):
        return self.appearance_mode_om.get()

    def show_notification_for_new_dictionary(self, event=None):
        if self.show_info_var.get():
            return showinfo(title=i18n.t("main.info"), message=i18n.t("main.note"))

    def filter_remove_word_combobox(self, new_values: list[str]):
        self.remove_word_cb.configure(values=new_values)
