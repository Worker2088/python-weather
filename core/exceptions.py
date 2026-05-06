"""
Модуль содержит базовое исключение

"""

class BaseAppException(Exception):
    """
    Базовый класс для всех кастомных исключений приложения.
    """
    def __init__(self, message: str, status_code: int = 500) -> None:
        """
        Инициализирует исключение.

        Args:
            message (str): Сообщение об ошибке.
            status_code (int): HTTP статус-код ошибки.
        """
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ExternalServiceError(BaseAppException):
    """
    """
    def __init__(self, match_uuid: str) -> None:
        """
        """
        pass
        # super().__init__(f"Матч с UUID {match_uuid} не найден", status_code=404)



# class PlayerError(BaseAppException): pass
# class PlayerNotFound(PlayerError): pass
# class DuplicatePlayerName(PlayerError): pass
#
# class MatchError(BaseAppException): pass
# class MatchNotFound(MatchError): pass
# class MatchAlreadyFinished(MatchError): pass
#
# class InfrastructureError(BaseAppException): pass
# class DatabaseConnectionError(InfrastructureError): pass