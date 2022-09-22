import multiprocessing
import os

import gunicorn
from dotenv import find_dotenv, load_dotenv

pythonpath = os.path.dirname(__file__)

load_dotenv(find_dotenv(os.getenv("ENV_FILE", "env")))

gunicorn.SERVER_SOFTWARE = "CALC Analysis"

port = os.getenv("PORT", 5050)
bind = f"0.0.0.0:{port}"

workers = (
    1
    if os.getenv("IS_WORKER", "false") == "true"
    else multiprocessing.cpu_count() * 2 + 1
)


forwarded_allow_ips = "*"
timeout = int(os.getenv("GUNICORN_TIMEOUT", 120))
