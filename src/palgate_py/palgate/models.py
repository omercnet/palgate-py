# SPDX-FileCopyrightText: 2024-present omercnet <639682+omercnet@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

"""Module containing data models for the PalGate application."""

from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, NamedTuple

if TYPE_CHECKING:
    from datetime import datetime


@dataclass
class Device:
    """Data model for a PalGate device."""

    id: str | None = None
    sub_type: str | None = None
    model: str | None = None
    outputs: int | None = None
    type: str | None = None
    version_num: float | None = None
    pal_sim: bool | None = None
    address: str | None = None
    image1: bool | None = None
    name: str | None = None
    name1: str | None = None
    output1_disabled: bool | None = None
    output1_latch_status: bool | None = None
    relay1: str | None = None
    valid_until: datetime | None = None
    sim_status: str | None = None
    address_coord: list[float] | None = None
    device_id: str | None = None
    admin: bool | None = None
    output1: bool | None = None
    admin_rules_disable: list[Any] | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    dial_to_open: bool | None = None
    local_only: bool | None = None
    firstname: str | None = None
    lastname: str | None = None
    output1_latch: bool | None = None
    output2_latch: bool | None = None
    output1_latch_max_time: int | None = None
    output2_latch_max_time: int | None = None
    secondary_device: bool | None = None
    notifications: bool | None = None
    guest_invitation: bool | None = None
    key: str | None = None
    group_id: int | None = None
    google_assistant_active: bool | None = None

    @classmethod
    def from_dict(cls, env: dict[str, Any]) -> Device:
        """Create a Device instance from a dictionary."""
        return cls(
            **{k: v for k, v in env.items() if k in inspect.signature(cls).parameters},
        )


class User(NamedTuple):
    id: str
    token: str
    firstname: str
    lastname: str
    image: bool


class Palgate(NamedTuple):
    session: str


class Token(NamedTuple):
    token: str
