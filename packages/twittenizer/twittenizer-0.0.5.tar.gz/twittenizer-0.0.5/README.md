# Twittenizer: Convert stupid text in smart features.

## What does this lib do?

A tokenizer created specifically for messages posted on Twitter ( known as tweets).
The constraints imposed by Twitter during the writing of messages force the users not to follow typographical standards.
The purpose of this tokenizer is to reduce as much as possible the noise induced by the constraints while keeping as much of the information available in the tweet as possible.

It is build on top of NTLK Twitter tokenizer.

## Installation

```pip install twittenizer```

## Example

```
>>> from twittenizer import Tokenizer
>>> tokenizer = Tokenizer()
>>> tokenizer.tokenize("Here is my website: https://t.co/EZWeDhjl, check it out! ")
['Here',  'is', 'my', 'website', 'check', 'it', 'out']
```

## Licence

## Documentation

