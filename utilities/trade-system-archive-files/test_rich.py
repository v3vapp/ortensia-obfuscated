import rich
from rich import pretty, print
from rich.console import Console
import time
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

log = logging.getLogger("rich")
log.info("Hello, World!")


def div(divisor: int, divident: int) -> float:
    return divisor / divident


def main():
    try:
        a = div(2, 1)
        log.info(f"2 / 1 = {a}")

        b = div(1, 0)
        log.info(f"1 / 0 = {b}")
    except Exception as e:
        log.exception("Rich error!")


if __name__ == "__main__":
    main()