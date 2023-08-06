import ipaddress

from chatserver.сhatserver.Log.server_log_config import server_log


class Port:
    """
    For port number descriptor: Validating the port.

    """

    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            server_log.critical(
                f'Недопустимый порт {value}. Допустимы порты с 1024 до 65535.')
            exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class IPAddress:
    """
    The descriptor for the IP address: Validating the IP address
    """

    def __set__(self, instance, value):
        try:
            if value == str(ipaddress.ip_address(value)):
                instance.__dict__[self.name] = value
        except ValueError:
            server_log.critical(f'{value} не является корректным IP-адресом')
            raise Exception(f'{value} не является корректным IP-адресом')

    def __set_name__(self, owner, name):
        self.name = name
