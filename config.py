import re
import os
import time
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Compile regex pattern for ID validation
id_pattern = re.compile(r'^\d+$')

class Config:
    """
    Configuration class for the bot.
    This class loads all necessary configuration from environment variables.
    """

    # Pyro client config
    API_ID = os.getenv("API_ID", "21189715")  # ⚠️ Required
    API_HASH = os.getenv("API_HASH", "988a9111105fd2f0c5e21c2c2449edfd")  # ⚠️ Required
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7044609105:AAEbL7gi84MMfESHFnsoSBsHVVyHNB1IQCo")  # ⚠️ Required

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
    SESSION = os.getenv("SESSION", "BQGpTXQAWQj7skbUYWJG68v_k91mlNI87pQCLM-fbIwpJy7SHfkOvUjTUumhYW-kJpgmf9JLY68qg_IAp_i5XQXI4cB5FNy_vYyc5VcAnzt7sze0TC5yh-4dPHtwXAMDdAlt2ZemBCGow9J4DXsQ5d0JcxdOARLqtsW8u_d__0GSVPpLSFftf179T6KzWCHRTYOfx7NmsSyysg3MuCP0j2jT0iFXSmoS_4mHJ49JLaFxB-Ln2-rHh-Sovd_baZ3-6F_c-YG7GhfdLyn7iHKrn5SeTskmczV4geih58cD9RBcxykpKkbpvcXBV8XYfSuCKZF3zKpe-2qY59QHmhTO6ikkTW_jEgAAAAGruX5VAA")  # ⚠️ Required

    # Webhook configuration
    WEBHOOK = bool(os.getenv("WEBHOOK", True))
    PORT = int(os.getenv("PORT", "8080"))

    @staticmethod
    def validate():
        """Validate required configurations."""
        required_vars = ['API_ID', 'API_HASH', 'BOT_TOKEN', 'DB_URL', 'ADMIN', 'SESSION']
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
