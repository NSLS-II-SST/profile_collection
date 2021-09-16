from ..CommonFunctions.functions import run_report

run_report(__file__)
from ..RSoXSBase.slack import RSoXSBot
import os

slack_token = os.environ.get("SLACK_API_TOKEN", None)
rsoxs_bot = RSoXSBot(token=slack_token, proxy=None, channel="#sst-1-rsoxs-station")
