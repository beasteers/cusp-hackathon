import re

from nltk.corpus import stopwords
import string


from nltk import bigrams 
from collections import Counter
from collections import defaultdict

# Get all nonprintable characters
printable = set(string.printable)
nonprintable = set([chr(i) for i in range(128)]).difference(printable)
nonprintable_tbl = {ord(c): None for c in nonprintable}
 
punctuation = list(string.punctuation)
twitter_stop = ['rt', 'via', u'\u2026'] # twitter stopwords
stop = stopwords.words('english') + twitter_stop



class patterns:
    emoticons_str = r"""
        (?:
            [:=;] # Eyes
            [oO\->]? # Nose
            [D\)\]\(\]/\\OpPdb] # Mouth
        )"""
    html_str = r'<[^>]+>' # HTML tags
    mentions_str = r'(?:@[\w_]+)' # @-mentions
    hashtags_str = r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)" # hash-tags
    url_str = r'https?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+' # URLs
    punctuation_str = r'[^A-z0-9]+'
    numbers_str = r'(?:(?:\d+,?)+(?:\.?\d+)?(?:st|nd|rd|th)?)' # numbers
    words_punc_str = r"(?:[a-z][a-z'\-_]+[a-z])" # words with - and '
    words_str = r'(?:[\w_.]+)' # other words
    
    tokens_str = [
        emoticons_str,
        html_str,
        hashtags_str,
        url_str,
        mentions_str,
        numbers_str,
        words_punc_str,
        words_str,
        r'(?:\S)' # anything else
    ]

    tokens = re.compile(r'('+'|'.join(tokens_str)+')', re.VERBOSE | re.IGNORECASE)
    emoticon = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
    mention = re.compile(r'^'+mentions_str+'$', re.VERBOSE | re.IGNORECASE)
    hashtag = re.compile(r'^'+hashtags_str+'$', re.VERBOSE | re.IGNORECASE)
    url = re.compile(r'^'+url_str+'$', re.VERBOSE | re.IGNORECASE)
    no_space_before_urls = re.compile(r'([\S]+)('+url_str+')', re.VERBOSE | re.IGNORECASE)
    punctuation = re.compile(r'^'+punctuation_str+'$', re.VERBOSE | re.IGNORECASE)
    words = re.compile(r'^'+words_str+'|'+words_punc_str+'$', re.VERBOSE | re.IGNORECASE)

 
def tokenize(s):
    return patterns.tokens.findall(s)

def fix_no_space_url(s):
    '''For some reason, there are sometimes spaces in urls. at least from what I remember. I haven't worked on this in like a year.'''
    return patterns.fix_urls.sub('\g<1> \g<2>', s)

def filter_tokens(tokens, 
    lowercase=True, 
    remove_stopwords=True, 
    remove_urls=True, 
    remove_emojis=True, 
    remove_mentions=True, 
    remove_nonascii=True,
    remove_punctuation=True, 
    remove_nonprintable=True):
    
    tokens = filter(len, tokens)
    if remove_emojis:
        tokens = [token for token in tokens if not patterns.emoticon.search(token)]
    if remove_nonascii:
        tokens = [token for token in tokens if not len(tokens) == 1 or ord(tokens[0]) < 128]
    if lowercase:
        tokens = [token if remove_emojis or patterns.emoticon.search(token) else token.lower() for token in tokens]
    if remove_stopwords:
        tokens = [token for token in tokens if token not in stop]
    if remove_punctuation:
        tokens = [token for token in tokens if token not in punctuation]
    if remove_nonprintable:
        tokens = [token for token in tokens if token not in nonprintable]
    if remove_urls:
        tokens = [token for token in tokens if not patterns.url.match(token)]
    if remove_mentions:
        tokens = [token for token in tokens if not patterns.mention.match(token)]
    
    return tokens
 
def tweet_tokenize(s, **kw):
    return filter_tokens(tokenize(s), **kw)



# def extract(tweet, search_word=None):
#     terms_stop = preprocess(tweet['text'])
#     terms_bigram = bigrams(terms_stop)

#     # Count terms only once, equivalent to Document Frequency
#     terms_single = set(terms_all)
#     # Count hashtags only
#     terms_hash = [term for term in terms_stop 
#                   if term.startswith('#')]
#     # Count terms only (no hashtags, no mentions)
#     terms_only = [term for term in terms_stop 
#                   if term not in stop and
#                   not term.startswith(('#', '@'))] 
#                   # mind the ((double brackets))
#                   # startswith() takes a tuple (not a list) if 
#                   # we pass a list of inputs


#     count_terms = Counter()
#     count_all.update(terms_all)


#     # Build co-occurrence matrix
#     com = defaultdict(lambda : defaultdict(int))
#     for i in range(len(terms_only)-1):            
#         for j in range(i+1, len(terms_only)):
#             w1, w2 = sorted([terms_only[i], terms_only[j]])                
#             if w1 != w2:
#                 com[w1][w2] += 1


#     com_max = []
#     # For each term, look for the most common co-occurrent terms
#     for t1 in com:
#         t1_max_terms = sorted(com[t1].items(), key=lambda a: a[1], reverse=True)[:5]
#         for t2, t2_count in t1_max_terms:
#             com_max.append(((t1, t2), t2_count))
#     # Get the most frequent co-occurrences
#     terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
#     print(terms_max[:5])


#     if search_word:
#         count_search = Counter()
#         for line in f:
#             tweet = json.loads(line)
#             terms_only = [term for term in preprocess(tweet['text']) 
#                           if term not in stop 
#                           and not term.startswith(('#', '@'))]
#             if search_word in terms_only:
#                 count_search.update(terms_only)
#         print("Co-occurrence for %s:" % search_word)
#         print(count_search.most_common(20))
