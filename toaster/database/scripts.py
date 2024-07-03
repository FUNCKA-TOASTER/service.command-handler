from typing import Callable, Optional
from .database import Database


def script(func: Callable, auto_commit: bool = True) -> Callable:
    """A decorator that implements a custom script wrapper.

    The decorator allows you to mark a function
    as a custom script for sqlalchemy. Using
    this mechanism, you can conveniently call
    the desired set of actions in the right place.
    It is enough only to transfer the instance of
    the database class to the script.

    Example: ::

        @script(auto_commit=False)
        def add_user(session: Session, name: str, age: int):
            new_user = User(name=name, age=age)
            session.add(new_user)
            session.commit()
    """

    def wrapper(db_instance: Database, *args, **kwargs) -> Optional:
        session = db_instance.make_session()
        try:
            result = func(session, *args, **kwargs)

            if auto_commit:
                session.commit()

            return result

        except Exception as error:
            session.rollback()
            raise error

        finally:
            session.close()

    return wrapper
