# SPDX-FileCopyrightText: 2024-present omercnet <639682+omercnet@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT

"""Module serves as the entry point for the palgate_py CLI application."""

import sys

if __name__ == "__main__":
    from .cli import cli

    sys.exit(cli())
