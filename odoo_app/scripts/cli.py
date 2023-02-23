from dotenv import load_dotenv, find_dotenv
from os import getenv
from odoo_app.bot import start_bot


def main() -> None:
    load_dotenv(find_dotenv())
    TOKEN = getenv("TOKEN")
    start_bot(TOKEN)


if __name__ == "__main__":
    main()
