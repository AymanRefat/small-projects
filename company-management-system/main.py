from views.interface import Interface
from models.base import Base
from dotenv import load_dotenv
from views import menus
from settings import SESSION_MAKER, DB_ENGINE

if __name__ == "__main__":
    load_dotenv()
    Base.create_tabels(DB_ENGINE)
    Base._set_sessionmaker(SESSION_MAKER)
    inter = Interface(menus.home_menu)
    inter.start()
