# SPDX-FileCopyrightText: 2024-present omercnet <639682+omercnet@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

"""Palgate module provides the PalGate class to interact with the PalGate system."""

from __future__ import annotations

import json
import os
import platform
from pathlib import Path
from typing import Any
from urllib import request
from urllib.error import HTTPError
from urllib.parse import urljoin

import jpype  # type: ignore
import jpype.imports  # type: ignore
from jpype.types import JClass  # type: ignore

from palgate_py.palgate.config import Config, User
from palgate_py.palgate.models import Device


class PalGate:
    """PalGate class provides an interface to interact with the PalGate system."""

    FaceDetectionNative: JClass
    Long: JClass
    System: JClass

    config: Config
    debug: bool

    API_BASE_URL = "https://api1.pal-es.com/v1/bt/"

    def __init__(self) -> None:
        """Initialize the PalGate instance."""
        cwd = Path(__file__).parent
        lib_path = cwd / "lib" / platform.processor()

        jpype.addClassPath(str(cwd / "lib" / "palgate.jar"))
        jpype.startJVM(f"-Djava.library.path={lib_path}")

        self.debug = os.environ.get("DEBUG", "") != ""
        self.Long = JClass("java.lang.Long")
        self.System = JClass("java.lang.System")

        self.System.load(str(lib_path / "liblog.so"))
        self.System.load(str(lib_path / "libdl.so"))
        self.System.load(str(lib_path / "libm.so"))
        self.System.load(str(lib_path / "libc.so"))
        self.FaceDetectNative = JClass("com.bluegate.shared.FaceDetectNative")

        self.config = Config()

    def _get_token(self) -> str:
        if self.config.user is None:
            msg = "User configuration is not set."
            raise ValueError(msg)

        return str(
            self.FaceDetectNative.getToken(self.config.user.token, self.config.user.id)
        )

    def qr_url(self) -> str:
        """Generate the QR code URL for the session."""

        if self.config.palgate is None:
            msg = "Palgate configuration is not set."
            raise ValueError(msg)
        session = self.config.palgate.get("session")
        return urljoin(self.API_BASE_URL, f"un/secondary/qr/{session}")

    def _api(self, path: str, *, auth: bool = True) -> dict:
        url = urljoin(self.API_BASE_URL, path)
        headers = {"User-Agent": "okhttp/4.9.3"}
        if auth:
            headers["X-Bt-Token"] = self._get_token()
        if self.debug:
            pass

        if not url.startswith("https:"):
            msg = "Invalid URL: {req.full_url}"
            raise ValueError(msg)

        req = request.Request(  # noqa: S310
            url,
            headers=headers,
        )
        try:
            with request.urlopen(req) as res:  # noqa: S310
                data = res.read()
        except HTTPError as e:
            data = json.dumps({"status": "error", "msg": str(e)}).encode()
        return json.loads(data)

    def login(self) -> tuple[bool, Any]:
        """Log in to the PalGate system."""

        if self.config.palgate is None:
            msg = "Palgate configuration is not set."
            raise ValueError(msg)
        session = self.config.palgate.get("session")
        try:
            data = self._api(f"un/secondary/init/{session}", auth=False)
            user = User(**data["user"])
            self.config.user = user
        except (TypeError, HTTPError) as e:
            return True, e
        return False, None

    def is_token_valid(self) -> tuple[bool, str]:
        """Check if the token is valid."""

        res = self._api("user/check-token")
        return res.setdefault("status", "error") != "ok", res.get("msg", "")

    def list_devices(self) -> list[Device]:
        """List all devices."""

        res = self._api("devices")
        return [Device.from_dict(device) for device in res["devices"]]

    def open_gate(self, device_id: str) -> tuple[bool, str]:
        """Open a gate."""

        res = self._api(f"device/{device_id}/open-gate?openBy=100&outputNum=1")
        return res.setdefault("status", "error") != "ok", res.get("msg", "")

    def logout(self):
        """Log out from the PalGate system."""

        del self.config.user
        del self.config.palgate
