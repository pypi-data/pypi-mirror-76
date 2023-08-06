# -*- coding: utf-8 -*-
import argparse
import configparser
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from chatserver.сhatserver.Log.Log_decorators import log
from chatserver.сhatserver.Log.server_log_config import server_log
from chatserver.сhatserver.Mainlib.variables import default_port
from chatserver.сhatserver.server.Server_DataBase import ServerDB
from chatserver.сhatserver.server.main_window import MainWindow
from chatserver.сhatserver.server.server_core import MessageProcessor


@log
def arg_parser(default_port, default_address):
	"""
	Parser for command line arguments
	:param default_port:
	:param default_address:
	:return:
	"""
	server_log.debug(
		f'Инициализация парсера аргументов коммандной строки: {sys.argv}')
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', default=default_port, type=int, nargs='?')
	parser.add_argument('-a', default=default_address, nargs='?')
	namespace = parser.parse_args(sys.argv[1:])
	listen_address = namespace.a
	listen_port = namespace.p
	server_log.debug('Аргументы успешно загружены.')
	return listen_address, listen_port


@log
def config_load():
	"""
	Configuration ini file parser
	:return:
	"""
	config = configparser.ConfigParser()
	dir_path = os.getcwd()
	config.read(f"{dir_path}/{'server.ini'}")
	# Если конфиг файл загружен правильно, запускаемся, иначе конфиг по
	# умолчанию.
	if 'SETTINGS' in config:
		return config
	else:
		config.add_section('SETTINGS')
		config.set('SETTINGS', 'Default_port', str(default_port))
		config.set('SETTINGS', 'Listen_Address', '')
		config.set('SETTINGS', 'Database_path', '')
		config.set('SETTINGS', 'Database_file', 'server_dataBase.db3')
		return config


@log
def main():
	"""
	Main server function
	:return:
	"""
	# Загрузка файла конфигурации сервера
	config = config_load()
	
	# Загрузка параметров командной строки, если нет параметров, то задаём
	# значения по умоланию.
	listen_address, listen_port = arg_parser(
		config['SETTINGS']['default_port'], config['SETTINGS']['default_address'])
	
	# Инициализация базы данных
	database = ServerDB('server_dataBase.db3')
	
	# Создание экземпляра класса - сервера и его запуск:
	server = MessageProcessor(listen_address, listen_port, database)
	server.daemon = True
	server.start()
	
	# Создаём графическое окуружение для сервера:
	server_app = QApplication(sys.argv)
	server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
	main_window = MainWindow(database, server, config)
	
	# Запускаем GUI
	server_app.exec_()
	
	# По закрытию окон останавливаем обработчик сообщений
	server.running = False


if __name__ == '__main__':
	main()
