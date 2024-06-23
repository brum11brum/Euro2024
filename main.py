from src import db_operations
from src.gui import App


if __name__ == '__main__':
    db_operations.check_predicitons_db()
    a = App()
    a.run()
