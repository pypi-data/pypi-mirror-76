import logging.config
import yaml
import os

path = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "logging.yaml"

env_key = "LOG_CFG"

value = os.getenv(env_key, None)
if value:
    path = value
if os.path.exists(path):
    with open(path, "rt") as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
else:
    print("logging.yaml does not exist")
    logging.basicConfig(level=logging.DEBUG)

from .cross_validate import perform_cv, parse_args
