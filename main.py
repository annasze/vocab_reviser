from pathlib import Path

import i18n

from src.handlers import main_handlers
from src.controllers.main_controller import MainController
from src.GUIs.main_gui import MainGui
from src.data.repository import JSONRepository

APP_SETTINGS_PATH = Path("settings/app_settings.json")
USER_SETTINGS_PATH = Path("settings/user_settings.json")


def main() -> None:
    # get settings
    app_settings = main_handlers.get_app_settings(APP_SETTINGS_PATH)
    user_settings = main_handlers.get_user_settings(USER_SETTINGS_PATH)

    # set the locale
    i18n.set("locale", app_settings.LOCALE[user_settings.app_language])
    i18n.load_path.append("locale")

    gui = MainGui()
    gui.configure_ui(user_settings, app_settings)
    repository = JSONRepository(app_settings.DB_PATH)
    controller = MainController(gui, repository, main_handlers, app_settings)
    controller.start_app()


if __name__ == "__main__":
    main()
