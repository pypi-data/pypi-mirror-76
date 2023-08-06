import os
from builtins import FileNotFoundError
from logging import debug
from pathlib import Path

import toml
import yaml
import yaml.parser
import yaml.scanner
from settingscascade import ElementSchema, SettingsManager

from rye.default_config import default


class Task(ElementSchema):
    isolate: bool
    target_environments: list
    commands: list


class Environment(ElementSchema):
    python: str
    location: list
    depends_files: list
    setup_commands: list
    create_command: list
    install_command: list
    clean_existing: bool
    required: bool


def config_dict_from_file():
    locations = iter(
        (os.environ.get("RYE_FILE"), "pyproject.toml", "rye.yaml", "rye.yml")
    )
    data = None
    while data is None:
        try:
            path = next(locations)
        except StopIteration:
            raise FileNotFoundError("Could not locate a valid rye file")
        data = toml_file(path) or yaml_file(path)
    return data


def toml_file(file_location):  # pragma: no cover
    try:
        return toml.loads(Path(file_location).read_text())["tool"]["rye"]
    except (FileNotFoundError, toml.TomlDecodeError, KeyError, TypeError) as e:
        debug(f"Warning couldn't parse {file_location} as TOML: {e}")
        return None


def yaml_file(file_location):
    try:
        return yaml.safe_load(Path(file_location).read_text())
    except (
        FileNotFoundError,
        yaml.parser.ParserError,
        yaml.scanner.ScannerError,
        TypeError,
    ) as e:
        debug(f"Warning couldn't parse {file_location} as YAML: {e}")
        return None


def cwd():
    return os.getcwd()


def list_to_path(parts):
    return Path(*parts)


def join(args):
    sep, *terms = args
    return sep.join([term for term in terms if term])


def current_venv(_):
    try:
        return os.environ["VIRTUAL_ENV"]
    except KeyError:  # pragma: no cover
        raise RuntimeError(
            "You used the current_venv function "
            "without an activated virtual environment"
        )


def home_dir(_):
    return Path.home()


def get_config(data=None):
    config = SettingsManager(
        data or [default, config_dict_from_file()], [Task, Environment]
    )
    config.add_filter("list_to_path", list_to_path)
    config.add_filter("join", join)
    config.add_filter("current_venv", current_venv)
    config.add_filter("home_dir", home_dir)
    return config
