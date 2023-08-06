# smallconfig
For Python 3.8+.

A small utility for managing script-specific settings and multiple
configurations. Configuration files are stored in `Appdata/Roaming` as
.json files. Uses only the standard library.

# Quickstart

This utility contains a template class `SmallConfig` which handles
multiple configuration files for the same script.

Create a child class of `SmallConfig` that implements the
`manager_name` and `default_config` properties.

```python
from smallconfig import SmallConfig as SmallConfigTemplate

class SmallConfig(SmallConfigTemplate):
    @property
    def manager_name(self):
        return 'ExampleManagerName'
    @property
    def default_config(self):
        return {
            'key': 'value',
            'is_example': True,
        }
```

Then create an instance of the class. Set a default configuration to
clean up function calls.

```python
config = SmallConfig('configuration.json')
config.get('key') # returns 'value'
config.set('key', 'othervalue')
config.get('key') # returns 'othervalue'
config.set_active_config('otherconfiguration.json')
config.get('key') # returns 'value'
config.get('key', 'configuration.json') # returns 'othervalue'
```

Other useful functions, mostly for juggling multiple configurations:

```python
# returns a list of full file paths to configs with given manager name
config.get_configs()

# gets the config dictionary of a given config name
config.get_config('config.json')

# reloads the cache of a config directly from a file
config.reload()

# creates a new configuration file (with default settings)
config.create_config('newconfig.json')

# sets the default configuration
config.set_active_config('otherconfig.json')
```
