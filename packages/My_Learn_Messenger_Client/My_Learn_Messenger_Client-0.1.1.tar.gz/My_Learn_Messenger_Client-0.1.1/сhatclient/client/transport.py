import binascii
import hashlib
import hmac
import json
import socket
import threading
import time

from PyQt5.QtCore import pyqtSignal, QObject


from chatclient.сhatclient.Log.client_log_config import client_log
from chatclient.сhatclient.Mainlib.JIM import send_message, get_message
from chatclient.сhatclient.Mainlib.exception import ServerError
from chatclient.сhatclient.Mainlib.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, PUBLIC_KEY, RESPONSE, \
	ERROR, DATA, RESPONSE_511, MESSAGE, SENDER, DESTINATION, MESSAGE_TEXT, GET_CONTACTS, LIST_INFO, USERS_REQUEST, \
	PUBLIC_KEY_REQUEST, ONLINE_USERS_REQUEST, ADD_CONTACT, REMOVE_CONTACT, EXIT

# Объект блокировки для работы с сокетом.
socket_lock = threading.Lock()


class ClientTransport(threading.Thread, QObject):
	"""
	The class that implements the transport subsystem of the client
	module. Responsible for interacting with the server.
	"""
	# Сигналы новое сообщение и потеря соединения
	new_message = pyqtSignal(dict)
	message_205 = pyqtSignal()
	connection_lost = pyqtSignal()
	
	def __init__(self, port, ip_address, database, username, passwd, keys):
		# Вызываем конструкторы предков
		threading.Thread.__init__(self)
		QObject.__init__(self)
		
		# Класс База данных - работа с базой
		self.database = database
		# Имя пользователя
		self.username = username
		# Пароль
		self.password = passwd
		# Сокет для работы с сервером
		self.transport = None
		# Набор ключей для шифрования
		self.keys = keys
		# Устанавливаем соединение:
		self.connection_init(port, ip_address)
		# Обновляем таблицы известных пользователей и контактов
		try:
			self.user_list_update()
			self.contacts_list_update()
		except OSError as err:
			if err.errno:
				client_log.critical(f'Потеряно соединение с сервером.')
				raise ServerError('Потеряно соединение с сервером!')
			client_log.error(
				'Timeout соединения при обновлении списков пользователей.')
		except json.JSONDecodeError:
			client_log.critical(f'Потеряно соединение с сервером.')
			raise ServerError('Потеряно соединение с сервером!')
		# Флаг продолжения работы транспорта.
		self.running = True
	
	def connection_init(self, port, ip):
		"""
		Method responsible for establishing a connection to the server
		:param port:
		:param ip:
		:return:
		"""
		# Инициализация сокета и сообщение серверу о нашем появлении
		self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		# Таймаут необходим для освобождения сокета.
		self.transport.settimeout(5)
		
		# Соединяемся, 5 попыток соединения, флаг успеха ставим в True если
		# удалось
		connected = False
		for i in range(5):
			client_log.info(f'Попытка подключения №{i + 1}')
			try:
				self.transport.connect((ip, port))
			except (OSError, ConnectionRefusedError):
				pass
			else:
				connected = True
				client_log.debug("Connection established.")
				break
			time.sleep(1)
		
		# Если соединится не удалось - исключение
		if not connected:
			client_log.critical('Не удалось установить соединение с сервером')
			raise ServerError('Не удалось установить соединение с сервером')
		
		client_log.debug('Starting auth dialog.')
		
		# Запускаем процедуру авторизации
		# Получаем хэш пароля
		passwd_bytes = self.password.encode('utf-8')
		salt = self.username.lower().encode('utf-8')
		passwd_hash = hashlib.pbkdf2_hmac('sha512', passwd_bytes, salt, 10000)
		passwd_hash_string = binascii.hexlify(passwd_hash)
		
		client_log.debug(f'Passwd hash ready: {passwd_hash_string}')
		
		# Получаем публичный ключ и декодируем его из байтов
		pubkey = self.keys.publickey().export_key().decode('ascii')
		
		# Авторизируемся на сервере
		with socket_lock:
			presense = {
				ACTION: PRESENCE,
				TIME: time.time(),
				USER: {
					ACCOUNT_NAME: self.username,
					PUBLIC_KEY: pubkey
				}
			}
			client_log.debug(f"Presense message = {presense}")
			# Отправляем серверу приветственное сообщение.
			try:
				send_message(self.transport, presense)
				ans = get_message(self.transport)
				client_log.debug(f'Server response = {ans}.')
				# Если сервер вернул ошибку, бросаем исключение.
				if RESPONSE in ans:
					if ans[RESPONSE] == 400:
						raise ServerError(ans[ERROR])
					elif ans[RESPONSE] == 511:
						# Если всё нормально, то продолжаем процедуру
						# авторизации.
						ans_data = ans[DATA]
						hash = hmac.new(passwd_hash_string, ans_data.encode('utf-8'), 'MD5')
						digest = hash.digest()
						my_ans = RESPONSE_511
						my_ans[DATA] = binascii.b2a_base64(
							digest).decode('ascii')
						send_message(self.transport, my_ans)
						self.process_server_ans(get_message(self.transport))
			except (OSError, json.JSONDecodeError) as err:
				client_log.debug(f'Connection error.', exc_info=err)
				raise ServerError('Сбой соединения в процессе авторизации.')
	
	def process_server_ans(self, message):
		"""
		Method to handle incoming messages from the server
		:param message:
		:return:
		"""
		client_log.debug(f'Разбор сообщения от сервера: {message}')
		
		# Если это подтверждение чего-либо
		if RESPONSE in message:
			if message[RESPONSE] == 200 or 202:
				return
			elif message[RESPONSE] == 400:
				raise ServerError(f'{message[ERROR]}')
			elif message[RESPONSE] == 205:
				self.user_list_update()
				self.contacts_list_update()
				self.message_205.emit()
			else:
				client_log.error(
					f'Принят неизвестный код подтверждения {message[RESPONSE]}')
		
		# Если это сообщение от пользователя добавляем в базу, даём сигнал о
		# новом сообщении
		elif ACTION in message and message[ACTION] == MESSAGE and SENDER in message and DESTINATION in message \
				and MESSAGE_TEXT in message and message[DESTINATION] == self.username:
			client_log.debug(
				f'Получено сообщение от пользователя {message[SENDER]}:{message[MESSAGE_TEXT]}')
			self.new_message.emit(message)
	
	def contacts_list_update(self):
		"""
		Method updating the list of contacts from the server.
		:return:
		"""
		self.database.contacts_clear()
		client_log.debug(f'Запрос контакт листа для пользователся {self.name}')
		req = {
			ACTION: GET_CONTACTS,
			TIME: time.time(),
			USER: self.username
		}
		client_log.debug(f'Сформирован запрос {req}')
		with socket_lock:
			send_message(self.transport, req)
			ans = get_message(self.transport)
		client_log.debug(f'Получен ответ {ans}')
		if RESPONSE in ans and ans[RESPONSE] == 202:
			for contact in ans[LIST_INFO]:
				self.database.add_contact(contact)
		else:
			client_log.error('Не удалось обновить список контактов.')
	
	def user_list_update(self):
		"""
		Method that updates the list of users from the server.
		:return:
		"""
		client_log.debug(f'Запрос списка известных пользователей {self.username}')
		req = {
			ACTION: USERS_REQUEST,
			TIME: time.time(),
			ACCOUNT_NAME: self.username
		}
		with socket_lock:
			send_message(self.transport, req)
			ans = get_message(self.transport)
		if RESPONSE in ans and ans[RESPONSE] == 202:
			self.database.add_users(ans[LIST_INFO])
		else:
			client_log.error('Не удалось обновить список известных пользователей.')
	
	def key_request(self, user):
		"""
		Method that requests the public key of the user from the server
		:param user:
		:return:
		"""
		client_log.debug(f'Запрос публичного ключа для {user}')
		req = {
			ACTION: PUBLIC_KEY_REQUEST,
			TIME: time.time(),
			ACCOUNT_NAME: user
		}
		with socket_lock:
			send_message(self.transport, req)
			ans = get_message(self.transport)
		if RESPONSE in ans and ans[RESPONSE] == 511:
			return ans[DATA]
		else:
			client_log.error(f'Не удалось получить ключ собеседника{user}.')
	
	def online_users_list_request(self):
		req = {
			ACTION: ONLINE_USERS_REQUEST,
			TIME: time.time()
		}
		with socket_lock:
			send_message(self.transport, req)
			self.process_server_ans(get_message(self.transport))
	
	def add_contact(self, contact):
		"""
		A method that sends information about adding a contact to the server.
		:param contact:
		:return:
		"""
		client_log.debug(f'Создание контакта {contact}')
		req = {
			ACTION: ADD_CONTACT,
			TIME: time.time(),
			USER: self.username,
			ACCOUNT_NAME: contact
		}
		with socket_lock:
			send_message(self.transport, req)
			self.process_server_ans(get_message(self.transport))
	
	def remove_contact(self, contact):
		"""
		Method that sends information about deleting a contact to the server
		:param contact:
		:return:
		"""
		client_log.debug(f'Удаление контакта {contact}')
		req = {
			ACTION: REMOVE_CONTACT,
			TIME: time.time(),
			USER: self.username,
			ACCOUNT_NAME: contact
		}
		with socket_lock:
			send_message(self.transport, req)
			self.process_server_ans(get_message(self.transport))
	
	def transport_shutdown(self):
		"""
		Method notifying the server when the client is finished
		:return:
		"""
		self.running = False
		message = {
			ACTION: EXIT,
			TIME: time.time(),
			ACCOUNT_NAME: self.username
		}
		with socket_lock:
			try:
				send_message(self.transport, message)
			except OSError:
				pass
		client_log.debug('Транспорт завершает работу.')
		time.sleep(0.5)
	
	def send_message(self, to, message):
		"""
		Method sending messages to the server for the user
		:param to:
		:param message:
		:return:
		"""
		message_dict = {
			ACTION: MESSAGE,
			SENDER: self.username,
			DESTINATION: to,
			TIME: time.time(),
			MESSAGE_TEXT: message
		}
		client_log.debug(f'Сформирован словарь сообщения: {message_dict}')
		# Необходимо дождаться освобождения сокета для отправки сообщения
		with socket_lock:
			send_message(self.transport, message_dict)
			self.process_server_ans(get_message(self.transport))
			client_log.info(f'Отправлено сообщение для пользователя {to}')
	
	def run(self):
		"""
		Method containing the main cycle of the transport stream
		:return:
		"""
		client_log.debug('Запущен процесс - приёмник собщений с сервера.')
		while self.running:
			# Отдыхаем секунду и снова пробуем захватить сокет.
			# если не сделать тут задержку, то отправка может достаточно долго
			# ждать освобождения сокета.
			time.sleep(1)
			message = None
			with socket_lock:
				try:
					self.transport.settimeout(0.5)
					message = get_message(self.transport)
				except OSError as err:
					if err.errno:
						client_log.critical(f'Потеряно соединение с сервером.')
						self.running = False
						self.connection_lost.emit()
				# Проблемы с соединением
				except (ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError, TypeError):
					client_log.debug(f'Потеряно соединение с сервером.')
					self.running = False
					self.connection_lost.emit()
				finally:
					self.transport.settimeout(5)
			
			# Если сообщение получено, то вызываем функцию обработчик:
			if message:
				client_log.debug(f'Принято сообщение с сервера: {message}')
				self.process_server_ans(message)
