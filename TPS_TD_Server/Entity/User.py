import sqlite3


class User(object):
	def __init__(self, username, client_hid, skill_level=0, trap_level=0):
		super(User, self).__init__()
		self.username = username
		self.skill_level = skill_level
		self.trap_level = trap_level
		self.rid = None
		self.client_hid = client_hid

	def set_info_from_player(self, skill_level, trap_level):
		self.skill_level = skill_level
		self.trap_level = trap_level

	def save_info_to_database(self):
		from common import conf
		conn = sqlite3.connect(conf.DB_NAME)  # connect to the user information database
		c = conn.cursor()
		c.execute("UPDATE UserProperty SET skillLevel=?, trapLevel=? WHERE username=?",
				(self.skill_level, self.trap_level, self.username))
		conn.commit()
