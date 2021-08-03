# !pip install korean_romanizer
# !pip install g2pk
# !pip install pororo

from korean_romanizer.romanizer import Romanizer
from pororo import Pororo

class KoreanRomanizer:
  def __init__(self):
    self.sent = ""
    print("Romanizer Initialized")
  def romanize(self, sent):
    """
    Returns converted Korean sentences into Romaji as pronounced.
    parameter: sent(str) - sentence you want to convert
    """
    self.sent = sent
    g2p = Pororo(task="g2p", lang="ko")
    r = Romanizer(g2p(self.sent))
    return r.romanize()