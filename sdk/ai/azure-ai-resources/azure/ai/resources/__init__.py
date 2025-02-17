# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

__path__ = __import__("pkgutil").extend_path(__path__, __name__)  # type: ignore

from ._ai_client import AIClient
from ._version import VERSION

__all__ = [
    "AIClient",
]

VERSION = VERSION
