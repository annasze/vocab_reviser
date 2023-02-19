from view import View
from models_handler import ModelsHandler
from sqlite3_db import SQLite3DB
from controller import Controller
from settings.settings_functions import read_settings_file


def main():
    # load settings file
    settings = read_settings_file()

    # create MVC and start the app
    model = ModelsHandler(db=SQLite3DB())
    view = View(settings)
    controller = Controller(model, view)
    controller.start_app(name=settings.dictionary_name)


if __name__ == "__main__":
    main()
