import logging
import socket

from chatserver.сhatserver.Log.server_log_config import server_log
from chatserver.сhatserver.Mainlib.variables import ACTION, PRESENCE


def log(func_to_log):
	"""Decorator function."""
	
	def log_saver(*args, **kwargs):
		ret = func_to_log(*args, **kwargs)
		server_log.debug(f'Была вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}. '
						 f'Вызов из модуля {func_to_log.__module__}')
		return ret
	
	return log_saver


def login_required(func):
	"""
	A decorator that verifies that the client is authorized on the server.
	Checks that the passed socket object is in
	the list of authorized clients.
	Except for passing the dictionary-query
	for authorization. If the client is not authorized,
	throws a TypeError exception
	"""
	
	def checker(*args, **kwargs):
		# проверяем, что первый аргумент - экземпляр MessageProcessor
		# Импортить необходимо тут, иначе ошибка рекурсивного импорта.
		from chatserver.сhatserver.server.server_core import MessageProcessor
		if isinstance(args[0], MessageProcessor):
			found = False
			for arg in args:
				if isinstance(arg, socket.socket):
					# Проверяем, что данный сокет есть в списке names класса
					# MessageProcessor
					for client in args[0].names:
						if args[0].names[client] == arg:
							found = True
			
			# Теперь надо проверить, что передаваемые аргументы не presence
			# сообщение. Если presense, то разрешаем
			for arg in args:
				if isinstance(arg, dict):
					if ACTION in arg and arg[ACTION] == PRESENCE:
						found = True
			# Если не не авторизован и не сообщение начала авторизации, то
			# вызываем исключение.
			if not found:
				raise TypeError
		return func(*args, **kwargs)
	
	return checker
