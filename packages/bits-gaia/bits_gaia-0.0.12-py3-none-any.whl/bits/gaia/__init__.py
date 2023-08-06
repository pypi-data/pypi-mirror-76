# -*- coding: utf-8 -*-
"""Gaia class file."""
import datetime
import json
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

    def get_people_dict(self):
        """Return a dict of People from the People MySQL DB."""
        pdb = self.auth.people_mysql()
        person_types = pdb.get_table_dict("person_types")
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        people = {}
        for person in pdb.get_table("people"):
            key = person["id"]
            first_name = person["first_name"]
            last_name = person["last_name"]
            person["full_name"] = f"{first_name} {last_name}"
            person_type_id = person["person_type_id"]
            person["person_type"] = person_types.get(person_type_id)
            start_date = person["start_date"]
            person["future_hire"] = 1 if start_date > today else 0
            people[key] = json.loads(json.dumps(person, default=str))
        return people

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
