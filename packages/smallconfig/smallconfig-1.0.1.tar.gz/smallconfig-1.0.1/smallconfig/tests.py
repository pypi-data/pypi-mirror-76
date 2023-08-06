from smallconfig import SmallConfig
import unittest
from os import remove
from os.path import join as pjoin


class TestConfig(SmallConfig):
    # on initialization, clear the directory
    def __init__(self, active_config: str = 'default.json'):
        super().__init__(active_config)
        for config_path in self.get_configs():
            remove(pjoin(self.configs_path, config_path))
        self.create_config(self.active_config)

    @property
    def default_config(self) -> dict:
        return {
            'is_unit_test': True,
            'key': 'value',
            'other_key': {
                'first_key': 1,
                'second_key': 2
            }
        }

    @property
    def manager_name(self) -> str:
        return 'SmallConfigUnitTest'


class TestSmallConfig(unittest.TestCase):
    def test_instantiation(self):
        try:
            TestConfig()
        except Exception as e:
            self.fail(f'Instantiating SmallConfig gave the following error: {str(e)}')

    def test_file_handling(self):
        config = TestConfig()

        self.assertIsNotNone(config.get_configs())

        config.create_config('new_configuration.json')
        self.assertRaises(FileExistsError, config.create_config, 'new_configuration.json')

        self.assertIn('new_configuration.json', config.get_configs())

        config.create_config('other_configuration')
        self.assertIn('other_configuration.json', config.get_configs())

    def test_values(self):
        config = TestConfig()

        self.assertEqual(config['key'], 'value')
        config.set('key', 'othervalue')
        self.assertEqual(config['key'], 'othervalue')
        config.reload()
        self.assertEqual(config['key'], 'othervalue')

        config.create_config('newconfig.json')
        self.assertEqual(config.get('key', 'newconfig.json'), 'value')

        config.set_active_config('newconfig.json')
        self.assertEqual(config['key'], 'value')


if __name__ == '__main__':
    unittest.main()
