from .pingpong import PPManager, PromptFmt
from .utils import build_prompts

class AlpacaPromptFmt(PromptFmt):
  @classmethod
  def ctx(cls, context):
    if context is None or context == "":
      return ""
    else:
      return f"""{context}

"""

  @classmethod
  def prompt(cls, pingpong, truncate_size):
    ping = pingpong.ping[:truncate_size]
    pong = "" if pingpong.pong is None else pingpong.pong[:truncate_size]
    return f"""### Instruction:
{ping}

### Response:
{pong}
"""

class AlpacaChatPPManager(PPManager):
  def build_prompts(self, from_idx: int=0, to_idx: int=-1, fmt: PromptFmt=AlpacaPromptFmt, truncate_size: int=None):
    return build_prompts(self, from_idx, to_idx, fmt, truncate_size)

