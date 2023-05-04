import click
import core

DIR_TYPE = click.Path(exists=True, file_okay=False, resolve_path=True)
CLI_HELP_MSG = "A game modding CLI tool to handle Steamworld games assets."
CLI_EPILOG = """
Usage examples:
to decompress without print log:
$ steamy --quiet ~/GOG Games/SteamWorld Heist/

to compress or decompress:
$ steamy --compress ~/GOG Games/SteamWorld Heist/
$ steamy --decompress ~/GOG Games/SteamWorld Heist/

Supported features:
- compression

Compression:
- Supported files: ".z", ".impak".
- Side effects: generates .lock files, for recompression.
"""


@click.command(help=CLI_HELP_MSG, epilog=CLI_EPILOG)
@click.argument("game_directory", type=DIR_TYPE)
@click.version_option(version="0.1.0", prog_name="Steamy")
@click.option(
    "--compress",
    "action",
    flag_value="compress",
    help="Optional action, instead file decompression",
)
@click.option(
    "--decompress",
    "action",
    flag_value="decompress",
    default=True,
    help="Default action, instead file compression",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="[0-warning, 1-info, 2-debug] - usage example: -vv",
)
@click.option("--quiet", is_flag=True, help="Do not show log")
def cli(game_directory, action, verbose, quiet):
    if action == "compress":
        core.compress(game_directory)
    else:
        core.decompress(game_directory)

    click.echo(f"game_directory: {game_directory}")
    click.echo(f"action: {action}")
    click.echo(f"verbose: {verbose}")
    click.echo(f"quiet: {quiet}")


if __name__ == "__main__":
    cli()
