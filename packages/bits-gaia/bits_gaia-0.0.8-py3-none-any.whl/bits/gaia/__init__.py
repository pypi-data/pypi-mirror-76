# -*- coding: utf-8 -*-
"""Gaia class file."""
import os

import requests
import yaml
from google.cloud import storage
from google.cloud.secretmanager_v1 import SecretManagerServiceClient

from .auth import Auth


class Gaia:
    """Gaia class."""

    def __init__(self, verbose=False):
        """Initialize a new Gaia class."""
        self.config = None
        self.project = None

        self.auth = Auth(self)
        self.verbose = verbose

    def get_config(self):
        """Return a dictionary of config settings."""
        if self.config:
            return self.config
        bucket = os.environ.get("CONFIG_BUCKET")
        blob = storage.Client().bucket(bucket).blob("config.yaml")
        yaml_string = blob.download_as_string()
        docs = yaml.load_all(yaml_string, Loader=yaml.Loader)
        self.config = {}
        for doc in docs:
            for key, value in doc.items():
                self.config[key] = value
        return self.config

    def get_project(self):
        """Return the project ID of the current environment."""
        if "GCP_PROJECT" in os.environ:
            return os.environ["GCP_PROJECT"]
        return requests.get(
            "http://metadata.google.internal/computeMetadata/v1/project/project-id",
            headers={"Metadata-Flavor": "Google"},
        ).text

    def get_secret(self, name):
        """Return the auth data from the request_json."""
        if not self.project:
            self.project = self.get_project()
        client = SecretManagerServiceClient()
        secret_path = client.secret_version_path(self.project, name, "latest")
        return client.access_secret_version(secret_path).payload.data.decode("utf-8")

    def get_settings(self, name):
        """Return the configuration settings for a specific service name."""
        return self.get_config().get(name)
