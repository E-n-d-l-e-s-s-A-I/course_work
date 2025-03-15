import asyncclick as click
from misc.fill_db import fill_test_data


@click.group()
def cli() -> None: ...


@click.command()
async def filldb() -> None:
    """Заполняем БД тестовыми данными."""
    await fill_test_data()


cli.add_command(filldb)

if __name__ == "__main__":
    cli(_anyio_backend="asyncio")
