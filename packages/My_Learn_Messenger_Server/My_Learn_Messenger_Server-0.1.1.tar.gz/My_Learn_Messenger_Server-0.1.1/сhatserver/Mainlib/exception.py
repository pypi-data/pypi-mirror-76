class IncorrectDataRecivedError(Exception):
    """
    Exception - Invalid data received from socket
    """

    def __str__(self):
        return 'Принято некорректное сообщение от удалённого компьютера.'


class ServerError(Exception):
    """
    Exception - Server Error
    """

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class NonDictInputError(Exception):
    """
    Exception - is the function argument is not a dictionary.
    """

    def __str__(self):
        return 'Аргумент функции должен быть словарём.'


class ReqFieldMissingError(Exception):
    """
    Error - a required field is missing in the accepted dictionary
    """

    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'В принятом словаре отсутствует обязательное поле {self.missing_field}.'


class DataBaseInteractiveError(Exception):
    """
    Database communication error
    """

    def __str__(self):
        return 'Ошибка взаимодействия с базой данных'
