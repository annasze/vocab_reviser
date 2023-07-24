import tkinter.ttk as ttk

import customtkinter as ctk
import i18n

from src.settings import AppSettings


class WordList(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title(i18n.t("list.title"))
        self.resizable(False, False)
        self.style = ttk.Style()

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

    def fill_in_tree(self, dictionary: dict[str, str], scores: dict[str, int], max_phrase_length: int):
        # create custom heading
        values = [i18n.t("list.nb"), i18n.t("list.word"), i18n.t("list.translation"), i18n.t("list.points")]
        self.tree.insert("", "end", values=values, tags='custom_heading')

        # sort by scores
        scores_sorted = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # fill the tree in with data
        for i, (word, point) in enumerate(scores_sorted, start=1):
            self.tree.insert("", "end", values=(
                f"{i}.",
                self.divide_frase(word, max_phrase_length),
                self.divide_frase(dictionary[word], max_phrase_length),
                str(point)))

    @staticmethod
    def divide_frase(phrase: str, max_length: int):
        """ Divides a long phrase in half so that it fits in the table.
            TTk does not provide an automatic line breakage in treeview. """
        if len(phrase) <= max_length:
            return phrase

        inx = max(filter(lambda i: phrase[i] == " ", range(max_length + 1)))

        return phrase[:inx] + "\n" + phrase[inx + 1:]

    def configure_style(self, mode: str, settings: AppSettings):
        """ Treeview widget is not available in customtkinter,
            so manual style configuration is necessary
            to match the style in the entire app. """

        self.style.configure("Treeview", font=("Arial", 13), rowheight=40, **getattr(settings, mode.upper() + "_THEME"))
        self.tree.tag_configure('custom_heading', **getattr(settings, mode.upper() + "_THEME_HEADING"))
