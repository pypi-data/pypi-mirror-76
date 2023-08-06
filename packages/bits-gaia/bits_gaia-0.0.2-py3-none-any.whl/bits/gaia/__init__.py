"""Gaia class file."""
import os

import yaml
from google.cloud import storage


class Gaia:
    """Gaia class."""

    def __init__(self):
        """Initialize a new Gaia class."""

    def get_config(self):
        """Return a dictionary of config settings."""
        bucket = os.environ.get('CONFIG_BUCKET')
        blob = storage.Client().bucket(bucket).blob('config.yaml')
        yaml_string = blob.download_as_string()
        docs = yaml.load_all(yaml_string, Loader=yaml.Loader)
        config = {}
        for doc in docs:
            for key, value in doc.items():
                config[key] = value
        return config
