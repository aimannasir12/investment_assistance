import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import nltk
nltk.data.path.append(r'C:\Users\aiman\PycharmProjects\investment_assistance\nltk_data')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
import streamlit as st
from streamlit_lottie import st_lottie
import requests
import time
st.set_page_config(page_title="Welcome to our Small Investor Advisor",page_icon="🧠")
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

st.title('CURRENT MARKET PSYCHOLOGY :brain:')
lottie_stocks = load_lottieurl("https://assets7.lottiefiles.com/private_files/lf30_bbx4oauz.json")
st_lottie(lottie_stocks, height=270, width=700)
hide_st_style="""
<style>
footer{visibility: hidden;}
</style>"""
st.markdown(hide_st_style,unsafe_allow_html=True)
st.write('Here we are going to scrape twitter data from the web to inform you of the latest that is being said about the stock market...since afterall the price of the market depends on the confidence the investors have in it.')
st.write("It informs you of the politics, global economic conditions, unexpected events concerning the stock market")
with st.spinner('This may take a little while...'):
    time.sleep(5)
st.success('Done Scraping And Analyzing!')
st.info(':information_source: Scroll down to obtain the data..:clock4:')
# To identify the sentiment of text
from textblob import TextBlob
from textblob.np_extractors import ConllExtractor
import tweepy as tw
# your Twitter API key and API secret
my_api_key = "vLfWKhd1eD8ymesrctcJ96d6s"
my_api_secret = "NmzltCeciD0a2twAJa3FvFqIclIm5xwarY8GQ815xGCNnZaxEl"
# authenticate
auth = tw.OAuthHandler(my_api_key, my_api_secret)
api = tw.API(auth, wait_on_rate_limit=True)
search_terms1 =['stock market']
tweets_df_all = pd.DataFrame()
for term in search_terms1:
    print(term)
    # get tweets from the API
    tweets = tw.Cursor(api.search_tweets,
                       q=term,
                       lang="en",
                       since_id="2022-10-06").items(50)
    # store the API responses in a list
    tweets_copy = []
    for tweet in tweets:
        tweets_copy.append(tweet)
    # intialize the dataframe
    tweets_df = pd.DataFrame()
    # populate the dataframe
    for tweet in tweets_copy:
        hashtags = []
        try:
            for hashtag in tweet.entities["hashtags"]:
                hashtags.append(hashtag["text"])
            text = api.get_status(id=tweet.id, tweet_mode='extended').full_text
        except:
            pass
        tweets_df = tweets_df.append(pd.DataFrame({'user_name': tweet.user.name,
                                                   'user_location': tweet.user.location,
                                                   'user_description': tweet.user.description,
                                                   # 'user_verified': tweet.user.verified,
                                                   'date': tweet.created_at,
                                                   'text': text,
                                                   'hashtags': [hashtags if hashtags else None],
                                                   'source': tweet.source}))
        tweets_df = tweets_df.reset_index(drop=True)
        tweets_df['search_term'] = term
        tweets_df_all = tweets_df_all.append(tweets_df)
def fetch_sentiment_using_textblob(text):
    analysis = TextBlob(text)
    return 'pos' if analysis.sentiment.polarity >= 0 else 'neg'
sentiments_using_textblob = tweets_df.text.apply(lambda tweet: fetch_sentiment_using_textblob(tweet))
pd.DataFrame(sentiments_using_textblob.value_counts())
tweets_df['sentiment'] = sentiments_using_textblob


def remove_pattern(text, pattern_regex):
    r = re.findall(pattern_regex, text)
    for i in r:
        text = re.sub(i, '', text)

    return text
# We are keeping cleaned tweets in a new column called 'tidy_tweets'
tweets_df['tidy_tweets'] = np.vectorize(remove_pattern)(tweets_df['text'], "@[\w]*: | *RT*")
cleaned_tweets = []

for index, row in tweets_df.iterrows():
    # Here we are filtering out all the words that contains link
    words_without_links = [word for word in row.tidy_tweets.split() if 'http' not in word]
    cleaned_tweets.append(' '.join(words_without_links))

tweets_df['tidy_tweets'] = cleaned_tweets
#remove tweets with empty text
tweets_df = tweets_df[tweets_df['tidy_tweets']!='']
#drop duplicate rows
tweets_df.drop_duplicates(subset=['tidy_tweets'], keep=False)
#reset rows since some rows have been removed are missing
tweets_df = tweets_df.reset_index(drop=True)
#we are using a different column for this since we still need the punctuation, special characters and numbers for semantic meaning
tweets_df['absolute_tidy_tweets'] = tweets_df['tidy_tweets'].str.replace("[^a-zA-Z# ]", "")
stopwords = set(stopwords.words("english"))
stopwords_set = set(stopwords)
cleaned_tweets = []
for index, row in tweets_df.iterrows():
    # filerting out all the stopwords
    words_without_stopwords = [word for word in row.absolute_tidy_tweets.split() if
                               not word in stopwords_set and '#' not in word.lower()]
    # finally creating tweets list of tuples containing stopwords(list) and sentimentType
    cleaned_tweets.append(' '.join(words_without_stopwords))
tweets_df['absolute_tidy_tweets'] = cleaned_tweets
tokenized_tweet = tweets_df['absolute_tidy_tweets'].apply(lambda x: x.split())
#word net lemmatizer
nltk.download('wordnet')
nltk.download('omw-1.4')
word_lemmatizer = WordNetLemmatizer()
tokenized_tweet = tokenized_tweet.apply(lambda x: [word_lemmatizer.lemmatize(i) for i in x])
#join tokenized tweet to give a sentence
for i, tokens in enumerate(tokenized_tweet):
    tokenized_tweet[i] = ' '.join(tokens)
tweets_df['absolute_tidy_tweets'] = tokenized_tweet
class PhraseExtractHelper(object):
    def __init__(self):
        self.lemmatizer = nltk.WordNetLemmatizer()
        self.stemmer = nltk.stem.porter.PorterStemmer()
    def leaves(self, tree):
        """Finds NP (nounphrase) leaf nodes of a chunk tree."""
        for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
            yield subtree.leaves()
    def normalise(self, word):
        """Normalises words to lowercase and stems and lemmatizes it."""
        word = word.lower()
        # word = self.stemmer.stem_word(word) # We will loose the exact meaning of the word
        word = self.lemmatizer.lemmatize(word)
        return word
    def acceptable_word(self, word):
        """Checks conditions for acceptable word: length, stopword. We can increase the length if we want to consider large phrase"""
        accepted = bool(3 <= len(word) <= 40
                        and word.lower() not in stopwords
                        and 'https' not in word.lower()
                        and 'http' not in word.lower()
                        and '#' not in word.lower()
                        )
        return accepted
    def get_terms(self, tree):
        for leaf in self.leaves(tree):
            term = [self.normalise(w) for w, t in leaf if self.acceptable_word(w)]
            yield term
sentence_re = r'(?:(?:[A-Z])(?:.[A-Z])+.?)|(?:\w+(?:-\w+)*)|(?:\$?\d+(?:.\d+)?%?)|(?:...|)(?:[][.,;"\'?():-_`])'
grammar = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns

    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
"""
chunker = nltk.RegexpParser(grammar)
nltk.download('averaged_perceptron_tagger')
key_phrases = []
phrase_extract_helper = PhraseExtractHelper()
for index, row in tweets_df.iterrows():
    toks = nltk.regexp_tokenize(row.tidy_tweets, sentence_re)
    postoks = nltk.tag.pos_tag(toks)
    tree = chunker.parse(postoks)

    terms = phrase_extract_helper.get_terms(tree)
    tweet_phrases = []

    for term in terms:
        if len(term):
            tweet_phrases.append(' '.join(term))
    key_phrases.append(tweet_phrases)
# text blob key phrases
nltk.download('conll2000')
textblob_key_phrases = []
extractor = ConllExtractor()
for index, row in tweets_df.iterrows():
    # filerting out all the hashtags
    words_without_hash = [word for word in row.tidy_tweets.split() if '#' not in word.lower()]
    hash_removed_sentence = ' '.join(words_without_hash)
    blob = TextBlob(hash_removed_sentence, np_extractor=extractor)
    textblob_key_phrases.append(list(blob.noun_phrases))
#textblob_key_phrases[:10]
tweets_df['key_phrases'] = textblob_key_phrases
from wordcloud import WordCloud
def generate_wordcloud(all_words):
    wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=100, relative_scaling=0.5, colormap='Dark2').generate(all_words)
    #'''plt.figure(figsize=(14, 10))
    #plt.imshow(wordcloud, interpolation="bilinear")
    #plt.axis('off')
    #plt.show()'''
sentiments_using_textblob = tweets_df.text.apply(lambda tweet: fetch_sentiment_using_textblob(tweet))
fig2=pd.DataFrame(sentiments_using_textblob.value_counts())
all_words = ' '.join([text for text in tweets_df['absolute_tidy_tweets']])
img=WordCloud().generate(all_words)
plt.imshow(img)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.write('---')
st.subheader('Twitter discussions :loudspeaker:')
st.pyplot()
st.write(':information_source: The size of the term directly represents how often it is being talked about.')
st.write('---')
import plotly.express as px
st.header("Discussion Sentiment Analysis")
fig1 = px.bar(fig2, x="text", color="text")
st.plotly_chart(fig1)
st.write(':information_source: Shows the positive and negative sentiments in the tweets. Please refer to the legend on the right.')


