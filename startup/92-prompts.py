run_report(__file__)

from IPython.terminal.prompts import Prompts, Token


class RSoXSPrompt(Prompts):
    def in_prompt_tokens(self, cli=None):
        if len(RE.md['user']) > 0 and len(RE.md['project']) > 0:
            RSoXStoken = (Token.Prompt, 'RSoXS {}/{} '.format(RE.md['user'],RE.md['project']))
        else:
            RSoXStoken = (Token.OutPrompt, 'RSoXS no user or project')
        return [RSoXStoken,
                (Token.Prompt, ' ['),
                (Token.PromptNum, str(self.shell.execution_count)),
                (Token.Prompt, ']: ')]

ip = get_ipython()
ip.prompts = RSoXSPrompt(ip)

sample()