import argparse
import json
import providers.globals as gvars


def get_config():
	if not gvars.APP_CONFIG:
		gvars.APP_CONFIG = Config().params
	return gvars.APP_CONFIG


class Config:
	params = None
	_config_path = ""

	def __init__(self):
		self._parse_args()
		self.params = self._parse_config()

	def _parse_args(self):
		parser = argparse.ArgumentParser()
		parser.add_argument(
			"-c", "--config_path", dest="config_path", type=str, required=True,
			help="Path to configuration file."
		)

		parser.add_argument(
			"-l", "--launch", dest="launch", type=str, required=False,
			help="Launch task on startup", choices=["api"]
		)

		parser.add_argument(
			"-o", "--other", dest="other", type=str, required=False,
			help="Other arguments"
		)

		args = parser.parse_args()
		if args.launch:
			gvars.APP_START_SERVICE = args.launch

		self._config_path = args.config_path

	def _parse_config(self):
		config_params = Params()
		config_params.load_config(self._config_path)
		return config_params


class Params(object):
	def __init__(self):
		self.__config_data = {}

	@property
	def launch_service(self):
		return gvars.APP_START_SERVICE

	@property
	def config_data(self):
		return self.__config_data

	@property
	def prod(self):
		return self.__config_data["prod"]

	"""Постгрес конфиг"""

	@property
	def _postgres_settings(self):
		return self.__config_data.setdefault("postgres", {})

	def get_postgres_username(self):
		return self._postgres_settings["username"]

	def get_postgres_password(self):
		return self._postgres_settings["password"]

	def get_postgres_hostname(self):
		return self._postgres_settings["hostname"]

	def get_postgres_port(self):
		return self._postgres_settings["port"]

	def get_postgres_database(self):
		return self._postgres_settings["database"]

	"""Редис конфиг"""

	@property
	def _redis_settings(self):
		return self.__config_data.setdefault("redis", {})

	def get_redis_db(self):
		return self._redis_settings["db"]

	def get_redis_hostname(self):
		return self._redis_settings["hostname"]

	def get_redis_port(self):
		return self._redis_settings["port"]

	"""Загрузка конфигурации из файла"""

	def load_config(self, config_path):
		with open(config_path) as config_file:
			self.__config_data = json.load(config_file)
