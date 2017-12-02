class TweetCriteria:
	
	def __init__(self):
		self.maxTweets = 0
		self.within = '15mi'

	def set(self, q=None, username=None, 
			since=None,	until=None,
			near=None,	within=None,
			max_tweets=None, top_tweets=None):
		if username: 
			self.setUsername(username)
		if since:
			self.setSince(since)
		if until:
			self.setUntil(until)
		if near:
			self.setNear(near)
		if within:
			self.setWithin(within)
		if max_tweets:
			self.setMaxTweets(max_tweets)
		if top_tweets:
			self.setTopTweets(top_tweets)
		return self
		
	def setUsername(self, username):
		self.username = username
		return self
		
	def setSince(self, since):
		self.since = since
		return self
	
	def setUntil(self, until):
		self.until = until
		return self

	def setNear(self, near):
		self.near = near
		return self

	def setWithin(self, within):
		self.within = within
		return self
		
	def setQuerySearch(self, querySearch):
		self.querySearch = querySearch
		return self
		
	def setMaxTweets(self, maxTweets):
		self.maxTweets = maxTweets
		return self

	def setTopTweets(self, topTweets):
		self.topTweets = topTweets
		return self