# TwitterBot

![GitHub repo size](https://img.shields.io/github/repo-size/amiralitaheri/TwitterBot)
![GitHub issues](https://img.shields.io/github/issues/amiralitaheri/TwitterBot)
![GitHub](https://img.shields.io/github/license/amiralitaheri/TwitterBot)
![Twitter Follow](https://img.shields.io/twitter/follow/ProgrammerBotF?style=social)

## Archived!!
Dear users of TwitterBot,

It is with a heavy heart that we bid farewell to our beloved bot today. Due to the recent changes made to the Twitter API by Elon Musk's team, we are no longer able to continue providing our services to you.

Our bot was built with the intention of making your Twitter experience more enjoyable and we hope that we were able to achieve that goal.

Unfortunately, the prices for the new Twitter API plans are unreasonably high, and we find it ridiculous that the hobby plan costs $100. As an open source project, we were unable to afford these costs, and we know that many of our users may also be unable to do so.

While we are sad to say goodbye, we are proud of what we accomplished together and we will always be grateful for the time we spent with you.

Thank you again for your support, and we wish you all the best in your future endeavors.

### Follow me on Twitter
You can follow the bot on twitter to see actual result of the bot.  
[**Follow ProgrammerBotF On Twitter**](https://twitter.com/ProgrammerBotF) 

### Follow me on Telegram
I will post selected tweets on my Telegram channel.  
[**Join The Telegram Channel**](https://t.me/ProgrammerBotFarsi)

### How to create your own bot
For using this bot you need a Twitter developer account, you can apply for one at this link https://developer.twitter.com/en/apply-for-access

Assuming that you already have your Twitter developer account you should follow this steps:

1. Clone the repository into your machine using commend below  
    ```git clone https://github.com/amiralitaheri/TwitterBot.git``` 
2. Go to the cloned directory  
    ```cd twitter bot```  
3. install the requirements by running   
    ```pip install -r requirements.txt```
4. Create the ```config.json``` file by using the ```config.json.sample``` and add your tokens and custom configurations
5. Run the app  
```python -m twitterbot```

### How to contribute
Any improvement to performance, functionality and etc are welcomed.  

You could start by creating your own custom tweet selector, just create a python file in ```twitterbot/tweetselectors```,
 create a python class that inherit from ```twitterbot.abstracts.tweet_selector_interface.TweetSelectorInterface``` and
 impalement the ```rate_tweet``` function, then changed the ```main``` function in ```__main__.py``` to use your tweet selector.

Please note that greedy_selector is created for Persian language. 

As mention in *How to it for your own bot* section you need a Twitter developer account to run this code.
If you have problem in getting one, contact me and I might be able to help you. 

See [CONTRIBUTING.md](https://github.com/amiralitaheri/TwitterBot/blob/master/CONTRIBUTING.md) for more detail.

## Warning: 
New Twitter Developer Apps created on or after April 29, 2022 will not be able to gain access to v1.1 statuses/sample and v1.1 statuses/filter.
https://twittercommunity.com/t/deprecation-announcement-removing-compliance-messages-from-statuses-filter-and-retiring-statuses-sample-from-the-twitter-api-v1-1/170500

 
