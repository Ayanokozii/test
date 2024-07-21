import os
import time

class Config:
    """
    Configuration class for the bot.
    This class loads all necessary configuration from environment variables.
    """

    # Pyro client config
    API_ID = os.getenv("API_ID", "21189715")  # ⚠️ Required
    API_HASH = os.getenv("API_HASH", "988a9111105fd2f0c5e21c2c2449edfd")  # ⚠️ Required
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7151676790:AAFIjgmsLZJsdDJYRWmQFaZGGGAxX3Tt3Cg")  # ⚠️ Required

    # Database config
    DB_URL = os.getenv("DB_URL", "mongodb+srv://ayanosuvii0925:subhichiku123@cluster0.uw8yxkl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # ⚠️ Required
    DB_NAME = os.getenv("DB_NAME", "AutoAcceptBot")

    # Other configs
    BOT_UPTIME = time.time()
    START_PIC = os.getenv("START_PIC", "https://telegra.ph/file/0ceb5f176f3cf877a08b5.jpg")
    ADMIN = int(os.getenv('ADMIN', '7181106700'))  # ⚠️ Required
    DEFAULT_WELCOME_MSG = os.getenv("WELCOME_MSG", "Hey {user},\nYour Request Approved ✅,\n\nWelcome to **{title}**")
    DEFAULT_LEAVE_MSG = os.getenv("LEAVE_MSG", "By {user},\nSee You Again 👋\n\nFrom **{title}**")

    # User client config
    SESSION = os.getenv("SESSION", "BQFPq6kAp2lpFF7n8_jZ4b4ZMM8x7_8_HLIqjFHy4tDZxln9d90h1m7a4u60_K2032J-Fh1Gi-T5u3jd4mmHiJ1EO05SpgmDr5kwTgFMq2E3QQ0Jg_AmYwhed8UBBjNWwas7riu2U4YiOTu_K5_3RynzLhuu98D-cqzuEhLDgRaid7JUHi3IitCRLig-4WS36w29Z_Ak1KoKlQpujqOHNfE0RsZxnHzt0u1Th-pn_1u3Mon-pMWu-nr-8JdfDdy72B5kB8pgYkrDtdvbO2pcUSEn6wmNCeurSRmwQVclwcL3KA9LJUDWy6pgMafye72t0Up9nDkkVbajVdlkwPPqTjZPmoaImwAAAAGd_UK4AA")  # ⚠️ Required

    # Webhook configuration
    WEBHOOK = bool(os.getenv("WEBHOOK", True))
    PORT = int(os.getenv("PORT", "4040"))

    # Log channel configuration
    LOG_CHANNEL = os.getenv("LOG_CHANNEL", "-1002216123516")  # Replace with your default or placeholder value

    @staticmethod
    def validate():
        """Validate required configurations."""
        required_vars = ['API_ID', 'API_HASH', 'BOT_TOKEN', 'DB_URL', 'ADMIN', 'SESSION', 'LOG_CHANNEL']
        for var in required_vars:
            if not getattr(Config, var):
                raise ValueError(f"Environment variable {var} is missing!")

class TxT:
    """
    Text messages used by the bot for various commands and responses.
    """

    HELP_MSG = """
    <b> ADMIN Available commands:- </b>

    ➜ /set_welcome - To set custom welcome message (support photo & video & animation or gif)
    ➜ /set_leave - To set custom leave message (support photo & video & animation or gif)
    ➜ /option - To toggle your welcome & leave message also auto accept (whether it'll show to user or not and will auto accept or not)
    ➜ /auto_approves - To toggle your auto approve channel or group
    ➜ /status - To see status about bot
    ➜ /restart - To restart the bot
    ➜ /broadcast - To broadcast the users (only those users who have started your bot)
    ➜ /acceptall - To accept all the pending join requests
    ➜ /declineall - To decline all the pending join requests

    <b>⦿ Developer:</b> <a href=https://t.me/Requestacceptingxbot>~ CLICK ME</a>
    """

if __name__ == "__main__":
    try:
        Config.validate()
        print("Configuration is valid.")
    except ValueError as e:
        print(f"Configuration error: {e}")
