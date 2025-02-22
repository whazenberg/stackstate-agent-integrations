# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import click

from ..console import CONTEXT_SETTINGS
from .changelog import changelog
from .requirements import requirements
from .integrations import integrations


ALL_COMMANDS = (
    changelog,
    requirements,
    integrations,
)


@click.group(
    context_settings=CONTEXT_SETTINGS,
    short_help='A collection of tasks related to the StackState Agent'
)
def agent():
    pass


for command in ALL_COMMANDS:
    agent.add_command(command)
