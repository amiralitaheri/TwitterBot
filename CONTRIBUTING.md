### How to contribute
Any improvement to performance, functionality and etc are welcomed.  

You could start by creating your own custom tweet selector, just create a python file in ```twitterbot/tweetselectors```,
 create a python class that inherit from ```twitterbot.abstracts.tweet_selector_interface.TweetSelectorInterface``` and
 impalement the ```rate_tweet``` function, then changed the ```main``` function in ```__main__.py``` to use your tweet selector.

Please note that greedy_selector is created for Persian language. 

As mention in *How to it for your own bot* section you need a Twitter developer account to run this code.
If you have problem in getting one, contact me and I might be able to help you. 

### Things to keep in mind
1. If you are working on an issue/feature, try announcing it to others to avoid to people working on same issue/feature
2. Try to test your code and make it as clean as possible before submitting a pull request
3. Push your code in a branch named *yourName_featureName* avoid pushing to *master* branch 

