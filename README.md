# TwitterBot

### follow me on Twitter
You can follow the bot on twitter to see actual result of the bot.  
[**Follow ProgrammerBotF On Twitter**](https://twitter.com/ProgrammerBotF) 

### How to it for your own bot
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
 impalement the rate_tweet tweet function, then changed the ```main``` function in ```__main__.py``` to use your tweet selector.

Please note that greedy_selector is created for Persian language. 

As mention in *How to it for your own bot* section you need a Twitter developer account to run this code.
If you have problem in getting one, contact me and I might be able to help you. 
 
