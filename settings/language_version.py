from dataclasses import dataclass


@dataclass
class LanguageVersion:
    # main window
    manage_dicts_lb: str
    switch_dict_lb: str
    remove_dict_lb: str
    add_new_dict_lb: str
    first_lang_ent: str
    second_lang_ent: str
    browse_btn: str

    current_dict_lb: str
    show_list_btn: str
    show_session_list_btn: str
    reset_points: str
    start_btn: str
    notes_lb: str
    save_to_file_btn: str
    appearance_mode_lb: str
    words_per_session_lb: str
    sec_lb: str
    ignore_lb: str
    capitalization_switch: str
    punctuation: str
    add_word_lb: str
    remove_word_lb: str
    language_lb: str
    submit: str
    remove_word_lb2: str
    confirm: str
    show_info_chb: str
    reset_btn: str
    # session window
    clear_button_session_window: str
    show_first_letter_button_session_window: str
    title_session_window: str
    # filedialog titles and messages
    error: str
    exit: str
    success: str
    are_you_sure: str
    message1: str
    message2: str
    message3: str
    message4: str
    message5: str
    message6: str
    message7: str
    message8: str
    message9: str
    message10: str
    title1: str
    title2: str
    title3: str
    title4: str
    title5: str
    title6: str
    message_add_word: str
    # WordList window
    title_wordlist: str
    title_session_wordlist: str
    nr: str
    points: str
