import i18n

import main_handlers
from main_controller import MainController
from main_gui import MainGui
from repository import JSONRepository
from settings import settings


def main() -> None:

    # set the locale
    i18n.set("locale", settings.LOCALE["English"])
    i18n.load_path.append("locale")

    gui = MainGui()
    repository = JSONRepository(settings.DB_PATH)
    controller = MainController(gui, repository, main_handlers)
    controller.start_app()


if __name__ == "__main__":
    main()
