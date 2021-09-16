from ..CommonFunctions.functions import run_report
from ..RSoXSBase.slack import RSoXSBot
import os


run_report(__file__)
slack_token = os.environ.get("SLACK_API_TOKEN", None)
rsoxs_bot = RSoXSBot(token=slack_token, proxy=None, channel="#sst-1-rsoxs-station")
