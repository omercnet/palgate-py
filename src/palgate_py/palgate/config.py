# SPDX-FileCopyrightText: 2024-present omercnet <639682+omercnet@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

"""Config module manages the configuration settings for the palgate application."""

from __future__ import annotations

import configparser
import os
from pathlib import Path
from uuid import uuid4

from palgate_py.palgate.models import User


class Config:
    """A class to manage the configuration settings for the palgate application."""

    _filename: Path
    _config: configparser.ConfigParser

    def __init__(self) -> None:
        """Initialize the Config object."""
        # Determine the appropriate config directory based on the operating system
        if os.name == "nt":  # Windows
            appdata = os.getenv("APPDATA")
            if appdata is None:
                msg = "APPDATA environment variable is not set."
                raise ValueError(msg)
            config_dir = Path(appdata) / "palgate"
        else:  # Linux and macOS
            config_dir = Path.home() / ".config" / "palgate"

        # Create the directory if it doesn't exist
        config_dir.mkdir(parents=True, exist_ok=True)

        # Define the config file path
        self._filename = config_dir / "config.ini"

        # Initialize the ConfigParser and read the config file
        self._config = configparser.ConfigParser()
        self._config.read(self._filename)

        # Set a value
        if "palgate" not in self._config:
            self._config["palgate"] = {"session": str(uuid4())}

        if "palgate.user" not in self._config:
            self._config["palgate.user"] = {}

    @property
    def palgate(self) -> configparser.SectionProxy | None:
        """Return the 'palgate' section of the configuration."""
        try:
            return self._config["palgate"]
        except KeyError:
            return None

    @palgate.setter
    def palgate(self, value: dict[str, str]) -> None:
        for k, v in value.items():
            self._config["palgate"][k] = str(v)
        self.save()

    @palgate.deleter
    def palgate(self) -> None:
        del self._config["palgate"]
        self.save()

    @property
    def user(self) -> User | None:
        """Return the 'user' section of the configuration as a User object."""
        try:
            return User(**self._config["palgate.user"])
        except (KeyError, TypeError):
            return None

    @user.setter
    def user(self, user: User) -> None:
        for k, v in user._asdict().items():
            self._config["palgate.user"][k] = str(v)
        self.save()

    @user.deleter
    def user(self) -> None:
        del self._config["palgate.user"]
        self.save()

    def save(self) -> None:
        """Save the updated settings to the config file."""
        with self._filename.open("w") as file:
            self._config.write(file)
