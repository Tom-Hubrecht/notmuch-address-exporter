from os import environ as env

from export import export

__VERSION__ = "0.1.0"

__all__ = [
    "__VERSION__",
    "export",
]

if __name__ == "__main__":
    export(env["NOTMUCH_ADDRESS_EXPORT_FILE"])
