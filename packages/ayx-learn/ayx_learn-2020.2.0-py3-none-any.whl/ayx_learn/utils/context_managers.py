"""Context manager utilities."""
import os
import sys
from pathlib import Path


class SysPrefixContext:
    """Change the sys.prefix in a certain context."""

    def __init__(self, new_sys_prefix):  # type: ignore
        """Construct the context manager."""
        self.sys_prefix = new_sys_prefix
        self._original_prefix = ""

    def __enter__(self):  # type: ignore  # type: ignore
        """Enter the context and change the sys.prefix."""
        self._original_prefix = sys.prefix
        sys.prefix = self.sys_prefix

    def __exit__(self, *args):  # type: ignore
        """Exit the context and change the prefix back to normal."""
        sys.prefix = self._original_prefix


CondaPrefixContext = SysPrefixContext(  # type: ignore
    Path(os.path.abspath(os.path.dirname(__file__))) / "../../../.."
)
