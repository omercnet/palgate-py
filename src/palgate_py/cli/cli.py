# SPDX-FileCopyrightText: 2024-present omercnet <639682+omercnet@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

"""Cli module provides a command-line interface for interacting with PalGate devices."""

import click

from palgate_py.__about__ import __version__
from palgate_py.palgate import PalGate

client = PalGate()


def login_error() -> None:
    """Show an error message indicating that the user needs to login."""
    click.secho("You need to login first!", fg="red")


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(version=__version__, prog_name="Palgate-PY")
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    help="Show more information",
    default=False,
)
@click.pass_context
def cli(ctx, debug) -> None:
    """Provide the main command group for the PalGate CLI."""
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug
    if click.get_current_context().invoked_subcommand == "logout":
        return
    if client.config.user:
        err, msg = client.is_token_valid()
        if err:
            click.secho(f"Error: {msg}", fg="red")
            raise click.exceptions.Exit
        if debug:
            click.secho(msg, fg="green")
    else:
        click.secho(
            "Link a new device with your palgate app (https://www.youtube.com/watch?v=LRuezZ1jw9Q)"
        )
        click.secho(client.qr_url(), fg="blue")
        err, msg = client.login()
        if err:
            click.secho(f"There was a problem logging in!\n{msg}", err=True)
        else:
            click.secho("Logged in succesfully!", fg="green")


@cli.command()
@click.pass_context
def list_devices(ctx) -> None:
    """List all devices. If debug is True, show more information."""
    devices = client.list_devices()
    for device in devices:
        if ctx.obj["DEBUG"]:
            click.secho(repr(device))
        else:
            click.secho(f"{device.name} ({device.name1})")


@cli.command()
@click.argument("device_id")
@click.pass_context
def open_gate(device_id: str) -> None:
    """Open the gate for the specified device ID."""
    err, msg = client.open_gate(device_id)
    if err:
        click.secho(f"Error: {msg}", fg="red")
    else:
        click.secho(msg, fg="green")


@cli.command()
@click.pass_context
def logout() -> None:
    """Log out from the PalGate system."""
    client.logout()
    click.secho("Logged out successfully!", fg="green")
