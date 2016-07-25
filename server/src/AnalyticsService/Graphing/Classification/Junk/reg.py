import re
emoticon_string = r"""(?:
[<>]?
[:;=8]                     # eyes
[\-o\*\']?                 # optional nose
[\)\]\(\[dDpP/\:\}\{@\|\\] # mouth
|
[\)\]\(\[dDpP/\:\}\{@\|\\] # mouth
[\-o\*\']?                 # optional nose
[:;=8]                     # eyes
[<>]?
)"""
#-->

def emoticon_aware_tokenizer(s):
    """Takes a string as input and returns a list of words and emoticons in the string."""
    #<--
    # The components of the tokenizer:
    regex_strings = (

    # Emoticons:
    emoticon_string
    ,
    # HTML tags:
    r"""<[^>]+>"""
    ,
    # Twitter username:
    r"""(?:@[\w_]+)"""
    ,
    # Twitter hashtags:
    r"""(?:\#+[\w_]+[\w\'_\-]*[\w_]+)"""
    ,
    # Remaining word types:
    r"""
    (?:[a-z][a-z'\-_]+[a-z])       # Words with apostrophes or dashes.

    |
    (?:[\w_]+)                     # Words without apostrophes or dashes.
    |
    (?:\.(?:\s*\.){1,})            # Ellipsis dots.
    """
    )
    word_re = re.compile(r"""(%s)""" % "|".join(regex_strings), re.VERBOSE | re.I | re.UNICODE)
    return word_re.findall(s)
    #-->

print emoticon_aware_tokenizer(":) 3423544")