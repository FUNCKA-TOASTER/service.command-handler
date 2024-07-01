from sqlalchemy.orm import sessionmaker

# TODO: Сделать какую-то оболочку над кастомными скриптами
# Вероятнее всего декоратор @script
# Который в контексте функции будет вызывать Session maker, и передавать сессию в декорируемый обьект


# Функция для создания сессии
def create_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# Декоратор @script
def script(func):
    def wrapper(*args, **kwargs):
        session = create_session()
        try:
            result = func(session, *args, **kwargs)
            session.commit()  # Коммитим изменения в базу данных
            return result
        except Exception as e:
            session.rollback()  # Откатываем транзакцию в случае ошибки
            raise e
        finally:
            session.close()  # Закрываем сессию

    return wrapper
