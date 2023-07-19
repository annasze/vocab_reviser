from typing import Protocol

import customtkinter as ctk
import i18n


default_color_theme = "blue"

LOCALE = {
    "polski": "pl",
    "English": "en",
    "español": "es"
}


class SessionGuiProtocol(Protocol):
    def configure_ui(self, controller) -> None:
        ...

    def set_texts(self) -> None:
        ...

    def create_special_letters_buttons(self, special_letters: list[str]) -> None:
        ...

    def clear_user_input_field(self) -> None:
        ...

    def change_color_of_user_input_field(self, color: str | tuple[str]):
        ...

    def insert_first_letter(self, first_letter: str):
        ...

    def show_correct_answer(self, correct_answer: str):
        ...

    def clear_correct_answer_label(self):
        ...

    def display_word(self, word: str):
        ...

    @property
    def get_user_input(self) -> str:
        ...

    def change_state_of_submit_btn(self, event=None) -> None:
        ...

    def step_progressbar(self):
        ...


class SessionGui(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.geometry("600x380+300+300")

        # create widgets
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
                                           width=500, font=ctk.CTkFont(size=20), text_color="#00FF00")
        self.correct_ans_lb.grid(row=2, pady=(0, 25))
        self.user_input = ctk.CTkEntry(self.main_frame, width=400, font=ctk.CTkFont(size=20), justify=ctk.CENTER)
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
        self.set_texts()

    def configure_ui(self, controller) -> None:
        self.progressbar.set(value=0)
        self.progressbar.configure(determinate_speed=50 / controller.settings.words_per_session)
        self.show_first_letter_button.configure(command=controller.show_first_letter)
        self.clear_button.configure(command=self.clear_user_input_field)
        self.submit_button.bind('<Button-1>', controller.handle_submit)
        self.bind('<Return>', controller.handle_submit)
        self.bind('<Key>', self.change_state_of_submit_btn)
        self.bind('<Motion>', self.change_state_of_submit_btn)

    def set_texts(self) -> None:
        self.clear_button.configure(text=i18n.t("session.clear"))
        self.show_first_letter_button.configure(text=i18n.t("session.show_first_letter"))
        self.submit_button.configure(text=i18n.t("session.submit"))
        self.title(i18n.t("session.title"))

    def create_special_letters_buttons(self, special_letters: list[str]) -> None:
        for i in range(len(special_letters)):
            ctk.CTkButton(
                master=self.special_letters_frame,
                text=f"{special_letters[i]}",
                command=lambda i=i: self.user_input.insert(self.user_input.index(ctk.INSERT), special_letters[i]),
                font=ctk.CTkFont(size=14),
                width=40
            ).grid(column=i, row=0, padx=5)

    def clear_user_input_field(self) -> None:
        self.user_input.delete(0, "end")
        self.user_input.focus()

    def change_color_of_user_input_field(self, color: str | tuple[str]):
        self.user_input.configure(text_color=color)
        self.user_input.update()

    def insert_first_letter(self, first_letter: str):
        self.user_input.delete(0, "end")
        self.user_input.insert(0, first_letter)
        self.user_input.focus()

    def show_correct_answer(self, correct_answer: str):
        self.corr_ans.set(correct_answer)
        self.correct_ans_lb.update()
        self.correct_ans_lb.focus()

    def clear_correct_answer_label(self):
        self.corr_ans.set("")

    def display_word(self, word: str):
        self.displayed_word.set(word)

    @property
    def get_user_input(self) -> str:
        return self.user_input.get()

    def change_state_of_submit_btn(self, event=None) -> None:
        self.user_input.focus()
        if self.user_input.get():
            self.submit_button.configure(state="normal")
        else:
            self.submit_button.configure(state="disabled")

    def step_progressbar(self):
        self.progressbar.step()
