import datetime
import os

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.exc import DisconnectionError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import default_comparator

# Класс - база данных клиента.
from chatclient.сhatclient.Log.client_log_config import client_log


class ClientDatabase:
	"""
    The class is a wrapper for working with the client database.
    Uses SQLite database, implemented with
    SQLAlchemy ORM and use a declarative approach
    """
	CDB_Base = declarative_base()
	
	class KnownUsers(CDB_Base):
		"""
        Class displaying all known users
        """
		__tablename__ = 'known_users'
		id = Column(Integer, primary_key=True)
		username = Column(String)
		
		def __init__(self, user):
			self.id = None
			self.username = user
	
	class MessageHistory(CDB_Base):
		"""
        Class displaying message history
        """
		__tablename__ = 'message_history'
		id = Column(Integer, primary_key=True)
		contact = Column(String)
		direction = Column(String)
		message = Column(Text)
		date = Column(DateTime)
		
		def __init__(self, contact, direction, message):
			self.id = None
			self.contact = contact
			self.direction = direction
			self.message = message
			self.date = datetime.datetime.now()
	
	# Класс - отображение списка контактов
	class Contacts(CDB_Base):
		"""
        Class displaying a list of contacts
        """
		__tablename__ = 'contacts'
		id = Column(Integer, primary_key=True)
		name = Column(String, unique=True)
		
		def __init__(self, contact):
			self.id = None
			self.name = contact
	
	def __init__(self, name):
		# Создаём движок базы данных, поскольку разрешено несколько клиентов одновременно, каждый должен иметь свою БД
		# Поскольку клиент мультипоточный необходимо отключить проверки на подключения с разных потоков,
		# иначе sqlite3.ProgrammingError
		path = os.getcwd()
		filename = f'client_{name}.db3'
		self.database_engine = create_engine(f'sqlite:///{os.path.join(path, filename)}',
											 echo=False,
											 pool_recycle=7200,
											 connect_args={
												 'check_same_thread': False})
		
		self.CDB_Base.metadata.create_all(self.database_engine)
		
		# Создаём сессию
		Session = sessionmaker(bind=self.database_engine)
		self.session = Session()
		self.session.commit()
		
		# Необходимо очистить таблицу контактов, т.к. при запуске они подгружаются с сервера.
		self.session.query(self.Contacts).delete()
		self.session.commit()
	
	def check_connection(self):
		"""
        Checking the database connection
        :return:
        """
		global conn_db
		result = False
		try:
			conn_db = self.database_engine.connect()
			result = True
		except DisconnectionError:
			client_log.critical(f'Нет соединения с базой данных. Test connection {result}')
			print(f'Нет соединения с базой данных. Test connection {result}')
		finally:
			conn_db.close()
		print(f'Test connection {result}')
		return result
	
	def add_contact(self, contact):
		"""
        Add contacts function
        :param contact:
        :return:
        """
		if not self.session.query(self.Contacts).filter_by(name=contact).count():
			contact_row = self.Contacts(contact)
			self.session.add(contact_row)
			self.session.commit()
	
	def del_contact(self, contact):
		"""
        Contact delete function
        :param contact:
        :return:
        """
		self.session.query(self.Contacts).filter_by(name=contact).delete()
	
	def contacts_clear(self):
		"""
		Method for clearing a table with a contact list
		"""
		self.session.query(self.Contacts).delete()
	
	def add_users(self, users_list):
		"""
        Feature of adding famous users. Users are retrieved only from the server, so the table is cleared
        :param users_list:
        :return:
        """
		self.session.query(self.KnownUsers).delete()
		for user in users_list:
			user_row = self.KnownUsers(user)
			self.session.add(user_row)
		self.session.commit()
	
	def save_message(self, contact, direction, message):
		"""
        Save message function
        :param contact:
        :param direction:
        :param message:
        :return:
        """
		message_row = self.MessageHistory(contact, direction, message)
		self.session.add(message_row)
		self.session.commit()
	
	def get_contacts(self):
		"""
        Returning contacts function
        :return:
        """
		return [contact[0] for contact in self.session.query(self.Contacts.name).all()]
	
	def get_users(self):
		"""
        Function that returns a list of known users
        :return:
        """
		return [user[0] for user in self.session.query(self.KnownUsers.username).all()]
	
	def check_user(self, user):
		"""
        A function that checks the presence of a user in known
        :param user:
        :return:
        """
		if self.session.query(self.KnownUsers).filter_by(username=user).count():
			return True
		else:
			return False
	
	def check_contact(self, contact):
		"""
        Function that checks the presence of a user in contacts
        :param contact:
        :return:
        """
		if self.session.query(self.Contacts).filter_by(name=contact).count():
			return True
		else:
			return False
	
	def get_history(self, contact):
		"""
        Function that returns the conversation history
        :param contact: this field from
        :return:
        """
		query = self.session.query(
			self.MessageHistory).filter_by(
			contact=contact)
		return [(history_row.contact, history_row.direction, history_row.message, history_row.date)
				for history_row in query.all()]


if __name__ == '__main__':
	test_db = ClientDatabase('test55')
	# for i in ['test3', 'test4', 'test5']:
	#     test_db.add_contact(i)
	# test_db.check_connection()
	# test_db.add_contact('test4')
	# test_db.add_users(['test1', 'test2', 'test3', 'test4', 'test5'])
	# test_db.save_message('test1', 'test2', f'Привет! я тестовое сообщение от {datetime.datetime.now()}!')
	# test_db.save_message('test2', 'test1', f'Привет! я другое тестовое сообщение от {datetime.datetime.now()}!')
	# print(test_db.get_contacts())
	# print(test_db.get_users())
	# print(test_db.check_user('test1'))
	# print(test_db.check_user('test10'))
	# print(test_db.get_history('test2'))
	# print(test_db.get_history(contact='test2'))
	# print(test_db.get_history('test3'))
	# test_db.del_contact('test4')
	# print(test_db.get_contacts())
