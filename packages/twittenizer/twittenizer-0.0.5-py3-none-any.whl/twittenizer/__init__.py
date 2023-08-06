# coding: utf-8

"""
A tokenizer created specifically for messages posted on Twitter ( known as tweets).
The constraints imposed by Twitter during the writing of messages force the users not to
follow typographical standards. 
The purpose of this tokenizer is to reduce as much as possible the noise induced by the
constraints while keeping as much of the information available in the tweet as possible.
"""

from .tokenizer import Tokenizer
