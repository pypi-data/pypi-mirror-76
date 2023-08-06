import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import default_comparator


# Класс - база данных сервера

class ServerDB:
	"""
    The class is a wrapper for working with the server database.
    Uses SQLite database, implemented with
    SQLAlchemy ORM and use a declarative approach.
    """
	DB_Base = declarative_base()
	
	class AllUsers(DB_Base):
		"""
        Class to display all users
        """
		__tablename__ = 'Users'
		id = Column(Integer, primary_key=True)
		name = Column(String, unique=True)
		last_login = Column(DateTime)
		passwd_hash = Column(String)
		pubkey = Column(Text)
		
		def __init__(self, username, passwd_hash):
			self.name = username
			self.last_login = datetime.datetime.now()
			self.passwd_hash = passwd_hash
			self.pubkey = None
			self.id = None
	
	class ActiveUsers(DB_Base):
		"""
        Class displaying all active users
        """
		__tablename__ = 'Active_users'
		id = Column(Integer, primary_key=True)
		user = Column(String, ForeignKey('Users.id'), unique=True)
		ip_address = Column(String)
		port = Column(Integer)
		login_time = Column(DateTime)
		
		def __init__(self, user_id, ip_address, port, login_time):
			self.user = user_id
			self.ip_address = ip_address
			self.port = port
			self.login_time = login_time
			self.id = None
	
	class LoginHistory(DB_Base):
		"""
        Class to display login history.
        """
		__tablename__ = 'login_history'
		id = Column(Integer, primary_key=True)
		name = Column(String, ForeignKey('Users.id'), unique=True)
		date_time = Column(DateTime)
		ip = Column(String)
		port = Column(Integer)
		
		def __init__(self, name, date, ip, port):
			self.id = None
			self.name = name
			self.date_time = date
			self.ip = ip
			self.port = port
	
	# Класс - отображение таблицы контактов пользователей
	class UsersContacts(DB_Base):
		"""
        Class for displaying user contacts table
        """
		__tablename__ = 'Contacts'
		id = Column(Integer, primary_key=True)
		user = Column(String, ForeignKey('Users.id'))
		contact = Column(String, ForeignKey('Users.id'))
		
		def __init__(self, user, contact):
			self.id = None
			self.user = user
			self.contact = contact
	
	# Класс отображение таблицы истории действий (статистики) пользователя
	class UsersHistory:
		"""
        Class displaying the table of the history of actions (statistics) of the user
        """
		__tablename__ = 'History'
		id = Column(Integer, primary_key=True)
		user = Column(String, ForeignKey('Users.id'))
		sent = Column(Integer)
		accepted = Column(Integer)
		
		def __init__(self, user):
			self.id = None
			self.user = user
			self.sent = 0
			self.accepted = 0
	
	def __init__(self, path):
		self.engine = create_engine(f'sqlite:///{path}', echo=False, pool_recycle=7200,
									connect_args={'check_same_thread': False})
		
		self.DB_Base.metadata.create_all(self.engine)
		Session = sessionmaker(bind=self.engine)
		self.session = Session()
		print(Session)
		
		# Если в таблице активных пользователей есть записи, то их необходимо удалить
		# Когда устанавливаем соединение, очищаем таблицу активных пользователей
		self.session.query(self.ActiveUsers).delete()
		self.session.commit()
	
	def user_login(self, username, ip_address, port, key):
		"""
        The function executed when the user logs in, writes the fact of login to the database
        :param username:
        :param ip_address:
        :param port:
        :param key:
        :return:
        """
		# Запрос в таблицу пользователей на наличие там пользователя с таким именем
		rez = self.session.query(self.AllUsers).filter_by(name=username)
		print(rez)
		# Если имя пользователя уже присутствует в таблице, обновляем время последнего входа
		if rez.count():
			user = rez.first()
			user.last_login = datetime.datetime.now()
			if user.pubkey != key:
				user.pubkey = key
		# Если нет, то генерируем исключение
		else:
			raise ValueError('Пользователь не зарегистрирован.')
		
		# Теперь можно создать запись в таблицу активных пользователей о факте входа.
		# Создаем экземпляр класса self.ActiveUsers, через который передаем данные в таблицу
		new_active_user = self.ActiveUsers(user.id, ip_address, port, datetime.datetime.now())
		self.session.add(new_active_user)
		
		# и сохранить в историю входов
		# Создаем экземпляр класса self.LoginHistory, через который передаем данные в таблицу
		history = self.LoginHistory(user.id, datetime.datetime.now(), ip_address, port)
		self.session.add(history)
		
		# Сохраняем изменения
		self.session.commit()
	
	def user_logout(self, username):
		"""
        User disconnection locking function
        :param username:
        :return:
        """
		# Запрашиваем пользователя, что покидает нас
		# получаем запись из таблицы AllUsers
		user = self.session.query(self.AllUsers).filter_by(name=username).first()
		
		# Удаляем его из таблицы активных пользователей.
		# Удаляем запись из таблицы ActiveUsers
		self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
		
		# Применяем изменения
		self.session.commit()
	
	def users_list(self):
		"""
        The function returns a list of known users with the time of the last login
        :return:
        """
		query = self.session.query(
			self.AllUsers.name,
			self.AllUsers.last_login,
		)
		# Возвращаем список кортежей
		return query.all()
	
	def active_users_list(self):
		"""
        The function returns a list of active users
        :return:
        """
		# Запрашиваем соединение таблиц и собираем кортежи имя, адрес, порт, время.
		query = self.session.query(
			self.AllUsers.name,
			self.ActiveUsers.ip_address,
			self.ActiveUsers.port,
			self.ActiveUsers.login_time
		).join(self.AllUsers)
		# Возвращаем список кортежей
		return query.all()
	
	def login_history(self, username=None):
		"""
        Function that returns login history for one user or all users
        :param username:
        :return:
        """
		# Запрашиваем историю входа
		query = self.session.query(self.AllUsers.name,
								   self.LoginHistory.date_time,
								   self.LoginHistory.ip,
								   self.LoginHistory.port
								   ).join(self.AllUsers)
		# Если было указано имя пользователя, то фильтруем по нему
		if username:
			query = query.filter(self.AllUsers.name == username)
		return query.all()
	
	def process_message(self, sender, recipient):
		"""
        The function records the transmission of the message and makes the appropriate marks in the database
        :param sender:
        :param recipient:
        :return:
        """
		# Получаем ID отправителя и получателя
		sender = self.session.query(self.AllUsers).filter_by(name=sender).first().id
		recipient = self.session.query(self.AllUsers).filter_by(name=recipient).first().id
		# Запрашиваем строки из истории и увеличиваем счётчики
		sender_row = self.session.query(self.UsersHistory).filter_by(user=sender).first()
		sender_row.sent += 1
		recipient_row = self.session.query(self.UsersHistory).filter_by(user=recipient).first()
		recipient_row.accepted += 1
		
		self.session.commit()
	
	def add_user(self, name, passwd_hash):
		"""
        User registration function. Accepts a name and a password hash, creates an entry in the statistics table.
        :param name:
        :param passwd_hash:
        :return:
        """
		user_row = self.AllUsers(name, passwd_hash)
		self.session.add(user_row)
		self.session.commit()
		history_row = self.UsersHistory(user_row.id)
		self.session.add(history_row)
		self.session.commit()
	
	def remove_user(self, name):
		"""
        The function of removing a user from the database
        :param name:
        :return:
        """
		user = self.session.query(self.AllUsers).filter_by(name=name).first()
		self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
		self.session.query(self.LoginHistory).filter_by(name=user.id).delete()
		self.session.query(self.UsersContacts).filter_by(user=user.id).delete()
		self.session.query(
			self.UsersContacts).filter_by(
			contact=user.id).delete()
		self.session.query(self.UsersHistory).filter_by(user=user.id).delete()
		self.session.query(self.AllUsers).filter_by(name=name).delete()
		self.session.commit()
	
	def get_hash(self, name):
		"""
        Function for obtaining a hash of a user's password
        :param name:
        :return:
        """
		user = self.session.query(self.AllUsers).filter_by(name=name).first()
		return user.passwd_hash
	
	def get_pubkey(self, name):
		"""
        Function for obtaining the public key of a user
        :param name:
        :return:
        """
		user = self.session.query(self.AllUsers).filter_by(name=name).first()
		return user.pubkey
	
	def check_user(self, name):
		"""
        Function for checking user existence
        :param name:
        :return:
        """
		if self.session.query(self.AllUsers).filter_by(name=name).count():
			return True
		else:
			return False
	
	def user_is_online(self, user):
		""""""
		if self.session.query(self.ActiveUsers).filter_by(user=user).count():
			return True
		else:
			return False
	
	def add_contact(self, user, contact):
		"""
        The function adds a contact for the user
        :param user:
        :param contact:
        :return:
        """
		# Получаем ID пользователей
		user = self.session.query(self.AllUsers).filter_by(name=user).first()
		contact = self.session.query(self.AllUsers).filter_by(name=contact).first()
		
		# Проверяем что не дубль и что контакт может существовать (полю пользователь мы доверяем)
		if not contact or self.session.query(self.UsersContacts).filter_by(user=user.id, contact=contact.id).count():
			return
		
		# Создаём объект и заносим его в базу
		contact_row = self.UsersContacts(user.id, contact.id)
		self.session.add(contact_row)
		self.session.commit()
	
	def remove_contact(self, user, contact):
		"""
        The function removes a contact from the database
        :param user:
        :param contact:
        :return:
        """
		# Получаем ID пользователей
		user = self.session.query(self.AllUsers).filter_by(name=user).first()
		contact = self.session.query(self.AllUsers).filter_by(name=contact).first()
		
		# Проверяем что контакт может существовать (полю пользователь мы доверяем)
		if not contact:
			return
		
		# Удаляем требуемое
		print(self.session.query(self.UsersContacts).filter(
			self.UsersContacts.user == user.id,
			self.UsersContacts.contact == contact.id
		).delete())
		self.session.commit()
	
	def get_contacts(self, username):
		"""
        The function returns the user's contact list
        :param username:
        :return:
        """
		# Запрашивааем указанного пользователя
		user = self.session.query(self.AllUsers).filter_by(name=username).one()
		
		# Запрашиваем его список контактов
		query = self.session.query(self.UsersContacts, self.AllUsers.name).filter_by(user=user.id). \
			join(self.AllUsers, self.UsersContacts.contact == self.AllUsers.id)
		
		# выбираем только имена пользователей и возвращаем их.
		return [contact[1] for contact in query.all()]
	
	def message_history(self):
		"""
        The function returns the number of messages sent and received
        :return:
        """
		query = self.session.query(
			self.AllUsers.name,
			self.AllUsers.last_login,
			self.UsersHistory.sent,
			self.UsersHistory.accepted
		).join(self.AllUsers)
		# Возвращаем список кортежей
		return query.all()


if __name__ == '__main__':
	test_db = ServerDB('../server_dataBase.db3')
	test_db.user_login('1111', '192.168.1.113', 8080, 123456)
	test_db.user_login('McG', '192.168.1.115', 8082, 654321)
	test_db.user_login('McG2', '192.168.1.114', 8081, 132435)
	# print(test_db.users_list())
	# print(test_db.active_users_list())
	# test_db.user_logout('McG')
	# print(test_db.login_history('re'))
	test_db.add_contact('test2', 'test1')
	test_db.add_contact('test1', 'test3')
	test_db.add_contact('test1', 'test6')
	test_db.remove_contact('test1', 'test3')
	test_db.process_message('McG2', '1111')
	print(test_db.message_history())
