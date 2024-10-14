import json
from collections import Counter, defaultdict
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from email.utils import parseaddr
from itertools import chain

from notmuch2 import Database, Message, NullPointerError


@dataclass
class AddressRecord:
    count: int
    name: str | None
    email: str


def get_addresses(email: Message) -> Iterable[tuple[str, str]]:
    def iter_header(name: str) -> Iterable[str]:
        """
        Wrap notmuch's header method
        """
        try:
            return (x.strip() for x in email.header(name).split(","))
        except (LookupError, NullPointerError):
            return iter(())

    return (
        parseaddr(e)
        for e in chain(iter_header("From"), iter_header("To"), iter_header("Cc"))
    )


def compile_addresses():
    db = Database(mode=Database.MODE.READ_ONLY)

    address_map: dict[str, list[str]] = defaultdict(list)
    res = []

    for name, email in chain.from_iterable(
        get_addresses(msg) for msg in db.messages("*")
    ):
        address_map[email].append(name)

    for email, names in address_map.items():
        # Get the most common name
        cnames = Counter(names)

        most_used = None
        for n, _ in cnames.most_common():
            if n and "@" not in n:
                most_used = n
                break

        res.append(asdict(AddressRecord(cnames.total(), most_used, email)))

    return res


def export(out: str):
    with open(out, "w") as fp:
        json.dump(compile_addresses(), fp)
