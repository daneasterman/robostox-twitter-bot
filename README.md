## RoboStox Twitter Bot

This Twitter bot monitors the publicly available RSS / XML data stream provided by the US Securities and Exchange Commission (SEC) for new Tesla filings.

Whenever an SEC filing is made (such as when a company insider like Elon Musk buys or sells Tesla stock) the Twitter bot will fire off a tweet with information about the disclosure.

The RoboStox Twitter Bot is live and has already picked up some insider selling activity by one key Tesla executive (see screenshot below). The Twitter account for the bot can be found here: [https://twitter.com/hello_robostox](https://twitter.com/hello_robostox)

<img width="671" alt="Screenshot 2023-02-02 at 16 48 35" src="https://user-images.githubusercontent.com/4712052/216388503-1586ae7f-04b2-4336-ab46-5b3c2520b33c.png">

**Technologies used:**
- Python's Beautiful Soup library for XML extraction. 
- Celery and RabbitMQ for periodic task execution. 
- Github API for simple JSON data storage / persistence.
- Twitter API for automatically creating tweets.
- Heroku for cloud hosting.
- Sentry for error reporting.
