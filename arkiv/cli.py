import logging, logging.config
import pkg_resources

import click

from . import config as CFG
from . import core

log = logging.getLogger(__name__)


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    version = pkg_resources.require("arkiv")[0].version
    print(f"arkiv v{version}")
    ctx.exit()


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("url", type=str)
@click.option("--json", is_flag=True)
@click.option("-d", "--dry-run", is_flag=True)
@click.option("-q", "--quiet", is_flag=True)
@click.option("-v", "--verbose", count=True, type=click.IntRange(0, 2))
@click.option("-V", "--version", is_flag=True, callback=print_version, expose_value=False, is_eager=True,)
def main(url, json, dry_run, quiet, verbose):
    if json or quiet:
        verbose = -1

    verbosity = {
        -1: {"root": {"handlers": ["default"], "level": "ERROR"}},
        0: {"root": {"handlers": ["default"], "level": "INFO"}},
        1: {"root": {"handlers": ["extended"], "level": "INFO"}},
        2: {"root": {"handlers": ["extended"], "level": "DEBUG"}},
    }
    CFG.LOG_CONFIG.update(verbosity.get(verbose))
    logging.config.dictConfig(CFG.LOG_CONFIG)

    CFG.CONFIG.update(CFG.load())
    CFG.CONFIG.update({"verbosity": verbose})

    CFG.CONFIG.update({"json": json})
    CFG.CONFIG.update({"dry-run": dry_run})

    log.debug(CFG.CONFIG)

    core.archive(url)


if __name__ == "__main__":
    main()
