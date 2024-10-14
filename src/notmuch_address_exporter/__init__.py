from os import environ as env

from .cli import export_addresses
from .export import export

__VERSION__ = "0.1.0"

__all__ = [
    "__VERSION__",
    "export",
]

if __name__ == "__main__":
    export_addresses()
