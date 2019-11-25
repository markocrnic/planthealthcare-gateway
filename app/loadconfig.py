import yaml
import re
import os

path_matcher = re.compile(r'\$\{([^}^{]+)\}')


def path_constructor(loader, node):
    # Extract the matched value, expand env variable, and replace the match
    value = node.value
    match = path_matcher.match(value)
    env_var = match.group()[2:-1]
    return os.environ.get(env_var)


def load_config(config_file):
    with open(config_file, 'r') as stream:
        try:
            yaml.add_implicit_resolver('!path', path_matcher, None, yaml.SafeLoader)
            yaml.add_constructor('!path', path_constructor, yaml.SafeLoader)
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
