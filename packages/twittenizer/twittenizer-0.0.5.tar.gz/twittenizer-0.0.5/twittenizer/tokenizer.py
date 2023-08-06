import html
import re
from typing import List

from .nltk_tweet_tokenizer import TweetTokenizer

__all__ = ['Tokenizer']

URLS = re.compile(
    r"""(?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:[a-z]{2,13}))(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)| \([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:[a-z]{2,13})\b/?(?!@))"""
)

MENTION = re.compile("""(@) ([\w_]+)""")

CONTRACTIONS = re.compile(
    r"""(?i)(\w+)(n['’′]t|['’′]ve|['’′]ll|['’′]d|['’′]re|['’′]s|['’′]m)"""
)

ARROWS = re.compile(r"(?:<*[-―—=]*>+|<+[-―—=]*>*)")

PUNCTCHARS = re.compile(r"""['\"“”‘’.?!…,:;(){}&#/_-]""")

DOLLARS = re.compile(r"""($)([\w_]+)""")


class Tokenizer(TweetTokenizer):
    """Main class used to create the tokenizer."""

    def __init__(self):
        super().__init__()

    def tokenize(self, text: str) -> List[str]:
        res = html.unescape(text)
        res = URLS.sub("", text)
        res = MENTION.sub(r"\2", res)
        res = CONTRACTIONS.sub(r"\1 \2", res)
        res = ARROWS.sub("", res)
        res = re.sub(r"RT|rt", "", res)
        res = re.sub(r"&", "and", res)
        res = re.sub(r"<3", "heart", res)
        res = PUNCTCHARS.sub(r"", res)
        res = DOLLARS.sub(r"\2", res)
        tokens = super().tokenize(res)
        return tokens
