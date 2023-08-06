import logging
import os
import sys

from logging.handlers import TimedRotatingFileHandler

# создаём формировщик логов (formatter):
server_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Подготовка имени файла для логирования
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'server.log')

# создаём потоки вывода логов
steam = logging.StreamHandler(sys.stderr)
steam.setFormatter(server_formatter)
steam.setLevel(logging.INFO)
log_file = logging.handlers.TimedRotatingFileHandler(path, encoding='utf8', interval=1, when='D')
log_file.setFormatter(server_formatter)

# создаём регистратор и настраиваем его
server_log = logging.getLogger('server')
server_log.addHandler(steam)
server_log.addHandler(log_file)
server_log.setLevel(logging.DEBUG)

# отладка
if __name__ == '__main__':
    server_log.critical('Test critical event')
    server_log.error('Test error ivent')
    server_log.debug('Test debug ivent')
    server_log.info('Test info ivent')
