# -*- coding: utf-8 -*-
import argparse
import os
import sys

from Cryptodome.PublicKey import RSA
from PyQt5.QtWidgets import QApplication, QMessageBox

from chatclient.сhatclient.Log.Log_decorators import log

from chatclient.сhatclient.Log.client_log_config import client_log
from chatclient.сhatclient.Mainlib.exception import ServerError
from chatclient.сhatclient.client.Client_DataBase import ClientDatabase
from chatclient.сhatclient.client.client_main_window import ClientMainWindow
from chatclient.сhatclient.client.start_dialog_window import UserNameDialog
from chatclient.сhatclient.client.transport import ClientTransport


# Парсер аргументов коммандной строки

@log
def arg_parser():
	"""
    Parser for command line arguments, returns a tuple of 4 elements
    server address, port, username, password.
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('addr', default='127.0.0.1', nargs='?')
	parser.add_argument('port', default=7777, type=int, nargs='?')
	parser.add_argument('-n', '--name', default=None, nargs='?')
	parser.add_argument('-p', '--password', default='', nargs='?')
	namespace = parser.parse_args(sys.argv[1:])
	server_address = namespace.addr
	server_port = namespace.port
	client_name = namespace.name
	client_passwd = namespace.password
	
	return server_address, server_port, client_name, client_passwd


# Основная функция клиента
if __name__ == '__main__':
	# Загружаем параметы коммандной строки
	server_address, server_port, client_name, client_passwd = arg_parser()
	client_log.debug('Args loaded')
	
	# Создаём клиентское приложение
	client_app = QApplication(sys.argv)
	
	# Если имя пользователя не было указано в командной строке то запросим его
	start_dialog = UserNameDialog()
	if not client_name or not client_passwd:
		client_app.exec_()
		# Если пользователь ввёл имя и нажал ОК, то сохраняем введённое и
		# удаляем объект, иначе выходим
		if start_dialog.ok_pressed:
			client_name = start_dialog.client_name.text()
			client_passwd = start_dialog.client_passwd.text()
			client_log.debug(f'Using USERNAME = {client_name}, PASSWD = {client_passwd}.')
		else:
			sys.exit(0)
	
	# Записываем логи
	client_log.info(
		f'Запущен клиент с параметрами: адрес сервера: {server_address} , порт: {server_port}, имя пользователя: {client_name}')
	
	# Загружаем ключи с файла, если же файла нет, то генерируем новую пару.
	dir_path = os.getcwd()
	key_file = os.path.join(dir_path, f'{client_name}.key')
	if not os.path.exists(key_file):
		keys = RSA.generate(2048, os.urandom)
		with open(key_file, 'wb') as key:
			key.write(keys.export_key())
	else:
		with open(key_file, 'rb') as key:
			keys = RSA.import_key(key.read())
	
	# !!!keys.publickey().export_key()
	client_log.debug("Keys sucsessfully loaded.")
	# Создаём объект базы данных
	database = ClientDatabase(client_name)
	# Создаём объект - транспорт и запускаем транспортный поток
	try:
		transport = ClientTransport(
			server_port,
			server_address,
			database,
			client_name,
			client_passwd,
			keys)
		client_log.debug("Transport ready.")
	except ServerError as error:
		message = QMessageBox()
		message.critical(start_dialog, 'Ошибка сервера', error.text)
		sys.exit(1)
	transport.setDaemon(True)
	transport.start()
	
	# Удалим объект диалога за ненадобностью
	del start_dialog
	
	# Создаём GUI
	main_window = ClientMainWindow(database, transport, keys)
	main_window.make_connection(transport)
	main_window.setWindowTitle(f'Чат Клиент alpha release - {client_name}')
	client_app.exec_()
	
	# Раз графическая оболочка закрылась, закрываем транспорт
	transport.transport_shutdown()
	transport.join()
