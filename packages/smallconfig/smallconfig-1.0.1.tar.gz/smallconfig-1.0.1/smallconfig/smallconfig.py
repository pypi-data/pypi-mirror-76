from os import getenv, makedirs, listdir
from os.path import exists, splitext, isabs, join as pjoin, basename
from json import dumps, loads, JSONDecodeError


class SmallConfig:
    def __init__(self, active_config: str = 'default.json'):
        self._configs_path = pjoin(self._root_storage_path, self.manager_path)
        if not exists(self._configs_path):
            makedirs(self._configs_path)

        # active_config keeps function calls cleaner
        self._active_config = active_config
        try:
            self.create_config(self.active_config)
        except FileExistsError:
            pass

        # cache configs to reduce the number of disk operations
        # keys should be full file paths
        self._cached_configs = {}

        # load the active (usually default) config
        self.reload(self._active_config)

    def get_configs(self) -> list:
        """
        :return: A list of the full paths to all available config files.
        """
        configs = set()

        for file in listdir(self._configs_path):
            filepath = pjoin(self._configs_path, file)
            try:
                with open(filepath, 'r', encoding=self._config_encoding) as json_file:
                    loads(json_file.read())
            except (IOError, JSONDecodeError):
                continue

            configs.add(basename(filepath))

        return sorted(list(configs))

    def get(self, key: str, config_name: str = None):
        """
        :return: The value of the given key from the name of the config.
        """
        if config_name is None:
            return self.get(key, self.active_config)
        filepath = self._config_name_to_filepath(config_name)
        if filepath in self._cached_configs:
            return self._cached_configs[filepath][key]
        else:
            self.reload(config_name)
            return self.get(config_name, key)

    def set(self, key: str, value, config_name: str = None) -> None:
        if config_name is None:
            return self.set(key, value, self.active_config)
        filepath = self._config_name_to_filepath(config_name)
        if filepath not in self._cached_configs:
            self.reload(config_name)

        self._cached_configs[filepath][key] = value
        self._write_config_to_file(filepath, self._cached_configs[filepath])

    def get_config(self, config_name: str = None) -> dict:
        if config_name is None:
            config_name = self._active_config
        filepath = self._config_name_to_filepath(config_name)
        if not exists(filepath):
            self.create_config(config_name)
        with open(filepath, 'r', encoding=self._config_encoding) as json_file:
            self._cached_configs[filepath] = loads(json_file.read())
            return self._cached_configs[filepath]

    def reload(self, config_name: str = None) -> None:
        if config_name is None:
            return self.reload(self.active_config)
        self.get_config(config_name)

    def create_config(self, config_name) -> dict:
        filepath = self._config_name_to_filepath(config_name)
        if not exists(filepath):
            self._write_config_to_file(filepath, self.default_config)
            return self.default_config
        else:
            raise FileExistsError(f'Config file already exists at {filepath}')

    def set_active_config(self, config_name: str) -> None:
        self._active_config = config_name

    def _write_config_to_file(self, filepath: str, config: dict):
        with open(filepath, 'w', encoding=self._config_encoding) as f:
            f.write(dumps(config, indent=4, sort_keys=False))

    def _config_name_to_filepath(self, config_name: str):
        if isabs(config_name):
            return config_name
        name, ext = splitext(config_name)
        if ext == '':
            config_name += '.json'
        return pjoin(self.configs_path, config_name)

    def get_config_path(self, config_name=None) -> str:
        if config_name is None:
            config_name = self._active_config
        return pjoin(self._configs_path, self._config_name_to_filepath(config_name))

    def __str__(self):
        return dumps(self.get_config(self._active_config), indent=4)

    def __repr__(self):
        return f'SmallConfig({self._active_config})'

    def __getitem__(self, key):
        return self.get(key, self._active_config)

    def __setitem__(self, key, value):
        return self.set(key, value, self._active_config)

    def __iter__(self):
        for k in self.get_config(self._active_config):
            yield k

    @property
    def _config_encoding(self) -> str:
        """
        Ensures uniform encoding throughout configurations
        :return: Valid encoding type
        """
        return 'utf-8'

    @property
    def _root_storage_path(self) -> str:
        return pjoin(getenv('APPDATA'), 'SmallConfig')

    @property
    def configs_path(self) -> str:
        return self._configs_path

    @property
    def active_config(self) -> str:
        return self._active_config

    @property
    def default_config(self) -> dict:
        """
        :return: A JSON-serializable dictionary that serves
        """
        raise NotImplementedError

    @property
    def manager_name(self) -> (str, tuple):
        """
        :return: A string or tuple that uniquely identifies the name under which these settings should be stored
        """
        raise NotImplementedError

    @property
    def manager_path(self) -> str:
        """
        :return: A string that gives the directory (relative to the root storage path) where configs are stored
        """
        if type(self.manager_name) == tuple:
            return pjoin(*self.manager_name)
        else:
            return self.manager_name
