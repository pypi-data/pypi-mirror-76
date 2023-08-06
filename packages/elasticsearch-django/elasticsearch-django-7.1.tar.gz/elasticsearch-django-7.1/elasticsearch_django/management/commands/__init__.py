"""Base command for search-related management commands."""
from __future__ import annotations

import argparse
import builtins
import logging
from typing import Any, Optional, Union

from django.core.management.base import BaseCommand
from elasticsearch.exceptions import TransportError

CommandReturnType = Optional[Union[list, dict]]
logger = logging.getLogger(__name__)


class BaseSearchCommand(BaseCommand):
    """Base class for commands that interact with the search index."""

    description = "Base search command."

    def _confirm_action(self) -> bool:
        """Return True if the user confirms the action."""
        msg = "Are you sure you wish to continue? [y/N] "
        return builtins.input(msg).lower().startswith("y")

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Add default base options of --noinput and indexes."""
        parser.add_argument(
            "-f",
            "--noinput",
            action="store_false",
            dest="interactive",
            default=True,
            help="Do no display user prompts - may affect data.",
        )
        parser.add_argument(
            "indexes", nargs="*", help="Names of indexes on which to run the command."
        )

    def do_index_command(self, index: str, **options: Any) -> CommandReturnType:
        """Run a command against a named index."""
        raise NotImplementedError()

    def handle(self, *args: Any, **options: Any) -> None:
        """Run do_index_command on each specified index and log the output."""
        for index in options.pop("indexes"):
            try:
                data = self.do_index_command(index, **options)
            except TransportError as ex:
                logger.warning("ElasticSearch threw an error: %s", ex)
                data = {"index": index, "status": ex.status_code, "reason": ex.error}
            except FileNotFoundError as ex:
                logger.warning("Mapping file not found: %s", ex)
                data = {
                    "index": index,
                    "status": "N/A",
                    "reason": "Mapping file not found",
                }
            except Exception as ex:
                logger.warning("Error running command: %s", ex)
                data = {
                    "index": index,
                    "status": "N/A",
                    "reason": str(ex),
                }
            finally:
                logger.info(data)
