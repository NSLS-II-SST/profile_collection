from slack import WebClient

class RSoXSBot:
    # The constructor for the class. It takes the channel name as the a
    # parameter and then sets it as an instance variable
    def __init__(self,token,proxy,channel):
        self.channel = channel
        self.webclient = WebClient(token=token, proxy=proxy)

    # Craft and return the entire message payload as a dictionary.
    def send_message(self, message):
        composed_message =  {
            "channel": self.channel,
            "blocks": [
                {"type": "section", "text": {"type": "mrkdwn", "text": message}},
            ],
        }
        try:
            self.webclient.chat_postMessage(**composed_message)
        except Exception:
            pass

slack_token = os.environ.get("SLACK_API_TOKEN", None)
rsoxs_bot = RSoXSBot(token=slack_token,
                     proxy=None,
                     channel="#sst-1-rsoxs-station")


from IPython.terminal.prompts import Prompts, Token
import datetime


class RSoXSPrompt(Prompts):
    def in_prompt_tokens(self, cli=None):
        dt = datetime.datetime.now()
        formatted_date = dt.strftime('%Y-%m-%d')

        if len(RE.md['proposal_id']) > 0 and len(RE.md['project_name']) > 0 and len(RE.md['cycle']) > 0:
            RSoXStoken = (Token.Prompt, 'RSoXS ' + '{}/{}/{}/auto/{}/ '.format(RE.md['cycle'],
                                                                               RE.md['proposal_id'],
                                                                               RE.md['project_name'],
                                                                               formatted_date)
                          )
        else:
            RSoXStoken = (Token.OutPrompt, 'RSoXS (define metadata before scanning)')
        return [RSoXStoken,
                (Token.Prompt, ' ['),
                (Token.PromptNum, str(self.shell.execution_count)),
                (Token.Prompt, ']: ')]


ip = get_ipython()
ip.prompts = RSoXSPrompt(ip)


def beamline_status():
    # user()
    sample()
    boxed_text('Detector status',
               exposure() +
               '\n   ' + saxs_det.binning() +
               '\n   ' + waxs_det.binning() +
               '\n   ' + saxs_det.cooling_state()+
               '\n   ' + waxs_det.cooling_state()+
               '\n   WAXS ' + waxs_det.shutter()+
               '\n   SAXS ' + saxs_det.shutter(),
               'lightblue', 80, shrink=False)