from os import environ as env

from export import export


def export_addresses():
    out = env.get("NOTMUCH_ADDRESS_EXPORT_FILE")

    if out is None:
        raise FileNotFoundError("No file selected for the export of notmuch addresses.")

    export(out)
