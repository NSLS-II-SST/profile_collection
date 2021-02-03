run_report(__file__)

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
               '\n   ' + saxs_det.binning().center(73) +
               '\n   ' + waxs_det.binning().center(73) +
               '\n   ' + saxs_det.cooling_state().center(73) +
               '\n   ' + waxs_det.cooling_state().center(73),
               'lightblue', 80, shrink=True)


user()
beamline_status()
