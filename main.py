import i18n

import session_handlers
from repository import JSONRepository
from session_controller import SessionController
from session_gui import SessionGui
from settings import SessionSettings

LOCALE = {
    "Polski": "pl",
    "English": "en",
    "espanol": "es"
}


def main() -> None:

    # set the locale
    i18n.set("locale", LOCALE["English"])
    i18n.load_path.append("locale")

    # some attributes hardcoded for now for easier checking
    gui = SessionGui()
    repository = JSONRepository("json_db.json")
    learning_data = repository.get_dictionary("SPANISH")
    settings = SessionSettings(5, True, True, 1)
    controller = SessionController(gui, repository, learning_data, session_handlers, settings)
    controller.start_session()


if __name__ == "__main__":
    main()