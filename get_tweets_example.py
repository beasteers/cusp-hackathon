import got


# Get tweets
tweetCriteria = got.manager.TweetCriteria().set(
	q='Harvey Weinstein', username=None, since='2017-11-28', until='2017-11-29',
	near='New York City, NY',	within='15mi', max_tweets=100, top_tweets=True
)
pulled_tweets = got.manager.TweetManager.getTweets(tweetCriteria)
print len(pulled_tweets)