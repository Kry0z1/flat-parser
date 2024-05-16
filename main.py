import asyncio

from src.console_stuff.main import main as main_cli
from src.bot_stuff.main import main as main_bot


async def main():
    choice = input("Do you want to start server?(y/n)\n")
    while choice.lower() not in "ny":
        choice = input("Do you want to start server?(y/n)\n")
    if choice == "y":
        await main_bot()
    else:
        main_cli()

if __name__ == "__main__":
    asyncio.run(main())