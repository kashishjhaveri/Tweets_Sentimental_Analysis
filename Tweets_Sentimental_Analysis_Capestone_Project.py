%matplotlib inline

import tweepy
import string
import pandas as pd
import numpy as np
import regex as re
import nltk
from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize 
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pyodbc

analyser = SentimentIntensityAnalyzer()

# Defining keys and auth.
consumer_key = "mqY7KXU62bf3wVfVz9ffGHZoN"
consumer_secret = "2hbZlgJ7jXr7rl7jbGeo4RaJR1jlYh2s7YCwwywmFC3QUcyXXi"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAGORNAEAAAAAG3l4jww0CbHhcmq1Ru2F7IrKkQE%3DiWzFDUv4qad7W9M0RVS6wWic37pvdZfJigG8eer5gDcmi86Bci"
access_token = "1362198643474857985-jW2JLdDHHsrfNDa1zf4M3S4yJ66itP"
access_token_secret = "sVl354OmRInWH6cR0RGT6ejim5npvONM1GMVq3iqmKW3U"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

#SQL Connectivity
Server = "tweet.database.windows.net"
Database = "tweetdb"
Table = "tweetstb.dbo.tweetsdb"

#Connect Server
def connectSqlServer():
    try:
        conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server} ;Server="+Server+"; Database="+Database+";Trusted_Connection=no;UID=tweetadmin;PWD=admin@123")
        return conn
    except:
        print("Error in Connecting Server")
        return "" 

    
connectSqlServer()

def insert_row(tweets_id,date_time,tweet_text):
    
    try:
        query = "INSERT INTO [dbo].[tweetstb] ([Tweet_ID], [Date_Time], [Tweet_Text]) VALUES(\'{0}\',\'{1}\',\'{2}\')".format(tweets_id,date_time,tweet_text)
        print(query)
        conn = connectSqlServer()
        cursor = conn.cursor()
        cursor.execute(query)
        # the connection is not autocommited by default. So we must commit to save our changes.
        conn.commit()
        return "Success"
    except Exception as e: 
        print(e)
        return "Fail"
		
print(cleaned_tweets)

#Frequency plot unflitered
freq = nltk.FreqDist(word_tokens)
for key,val in freq.items():
    #print(str(key) + ':' + str(val))
freq.plot(20, cumulative=False)

#Word Cloud unfiltered
wordcloud = WordCloud(
                          background_color='white',
                          max_words=100,
                          max_font_size=50, 
                          random_state=42
                         ).generate(" ".join(word_tokens))

fig = plt.figure(1)
plt.imshow(wordcloud)
plt.axis('off')
plt.show()

#Sentiment analysis unfiltered
sentiment_results = []

for tweets in tweets_df[2]:
    sentiment_tweet = analyser.polarity_scores(" ".join(tweets))
    print(sentiment_tweet)
    sentiment_results.append(sentiment_tweet)

colours = ({'POSITIVE': 'green',
           'NEGATIVE': 'orange'})
senti_df = pd.DataFrame(sentiment_results,columns=['neg','neu','pos', 'compound'])

senti_df['Sentiment_Type']='NEUTRAL'
senti_df.loc[senti_df['compound']>0.6,'Sentiment_Type']='POSITIVE'
senti_df.loc[senti_df['compound']< 0.3,'Sentiment_Type']='NEGATIVE'

senti_df.Sentiment_Type.value_counts().plot(kind='pie',title="Sentiment Analysis",autopct='%1.1f%%',colors= ["cyan","red","orange"])

plt.show()


#Frequency plot unfiltered
freq = nltk.FreqDist(filtered_sentence)
for key,val in freq.items():
    print(str(key) + ':' + str(val))
freq.plot(20, cumulative=False)

#Word Cloud filtered
wordcloud = WordCloud(
                          background_color='white',
                          max_words=100,
                          max_font_size=50, 
                          random_state=42
                         ).generate(" ".join(filtered_sentence))

fig = plt.figure(1)
plt.imshow(wordcloud)
plt.axis('off')
plt.show()

#Sentiment analysis unfiltered
sentiment_results = []

for tweets in cleaned_tweets:
    sentiment_tweet = analyser.polarity_scores(" ".join(tweets))
    sentiment_tweet['tweet'] = tweets
    print(sentiment_tweet)
    sentiment_results.append(sentiment_tweet)
    
senti_df = pd.DataFrame(sentiment_results,columns=['neg','neu','pos', 'compound','tweet'])

senti_df['Sentiment_Type']='NEUTRAL'
senti_df.loc[senti_df['compound']> 0.6,'Sentiment_Type']='POSITIVE'
senti_df.loc[senti_df['compound']< 0.3,'Sentiment_Type']='NEGATIVE'

senti_df.Sentiment_Type.value_counts().plot(kind='pie',title="Sentiment Analysis",autopct='%1.1f%%',colors= ["red","orange","cyan"])

plt.show()

pos_words = ''
pos_words_list = []

for tweets in senti_df.loc[senti_df['Sentiment_Type'] == 'POSITIVE']['tweet']:
    pos_words += ' '.join(tweets)
    pos_words_list.extend(tweets)
    
#Frequency plot positive
freq = nltk.FreqDist(pos_words_list)
for key,val in freq.items():
    print(str(key) + ':' + str(val))
freq.plot(20, cumulative=False)

#word cloud for positive tweets
wordcloud = WordCloud(
                          background_color='white',
                          max_words=100,
                          max_font_size=50, 
                          random_state=42
                         ).generate(pos_words)

fig = plt.figure(1)
plt.imshow(wordcloud)
plt.axis('off')
plt.show()

#word cloud for negative tweets

neg_words = ''
neg_words_list = []

for tweets in senti_df.loc[senti_df['Sentiment_Type'] == 'NEGATIVE']['tweet']:
    neg_words += ' '.join(tweets)
    neg_words_list.extend(tweets)

#Frequency plot negative
freq = nltk.FreqDist(neg_words_list)
for key,val in freq.items():
    print(str(key) + ':' + str(val))
freq.plot(20, cumulative=False)
    
wordcloud = WordCloud(
                          background_color='white',
                          max_words=100,
                          max_font_size=50, 
                          random_state=42
                         ).generate(neg_words)

fig = plt.figure(1)
plt.imshow(wordcloud)
plt.axis('off')
plt.show()

#word cloud for neutral tweets

neu_words = ''
neu_words_list = []
for tweets in senti_df.loc[senti_df['Sentiment_Type'] == 'NEUTRAL']['tweet']:
    neu_words += ' '.join(tweets)
    print(tweets)
    neu_words_list.extend(tweets)
    print(neu_words_list)

#Frequency plot neutral
freq = nltk.FreqDist(neu_words_list)
for key,val in freq.items():
    print(str(key) + ':' + str(val))
freq.plot(20, cumulative=False)

wordcloud = WordCloud(
                          background_color='white',
                          max_words=100,
                          max_font_size=50, 
                          random_state=42
                         ).generate(neu_words)

fig = plt.figure(1)
plt.imshow(wordcloud)
plt.axis('off')
plt.show()