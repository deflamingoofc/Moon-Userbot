import os
import environs

try:
    env = environs.Env()
    env.read_env("./.env")
except FileNotFoundError:
    print("No .env file found, using os.environ.")

api_id = int(os.getenv("API_ID", env.int("API_ID")))
api_hash = os.getenv("API_HASH", env.str("API_HASH"))

STRINGSESSION = os.getenv("STRINGSESSION", env.str("STRINGSESSION"))

bot_token = os.getenv("BOT_TOKEN", env.str("BOT_TOKEN"))

second_session = os.getenv("SECOND_SESSION", env.str("SECOND_SESSION", ""))

db_type = os.getenv("DATABASE_TYPE", env.str("DATABASE_TYPE"))
db_url = os.getenv("DATABASE_URL", env.str("DATABASE_URL", ""))
db_name = os.getenv("DATABASE_NAME", env.str("DATABASE_NAME"))

test_server = bool(os.getenv("TEST_SERVER", env.bool("TEST_SERVER", False)))
modules_repo_branch = os.getenv("MODULES_REPO_BRANCH", env.str("MODULES_REPO_BRANCH", "master"))
