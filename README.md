# AuctionChecker
## Using my crappy discord hook
This code in its entirety will check various auction sites for keywords in the `keywords.txt` folder and post results to discord webhook. However, the code is probably broken
because I made a bunch of untested modifications before uploading to github. I designed it to update two discord webhooks as I also run this for a friend.
You will probably need to remove one of them.

To use this, make a `discordtokens.ini` folder and populate it as follows with a discord webhook url:

```
[Discord]
webhookurl = Insert_URL_Here
```

You also will need to change the zip code on the `auctionchecker.py` file. Don’t touch the distance unless you know what your doing, the sites are picky as to what value is there.

Provided is a bat file that runs python. I personally use this with the Microsoft Task Scheduler for scheduled run times.

## Using just the scraper
You can also do your own thing with this. The website scraper is entirely located within `AuctionScraper.py`
I put lots of comments in it while learning BeautifulSoup. It should be very easy to learn what its doing.

## What is done and what i plan to do
* **govdeals.com**        - This is done and works well enough.
* **publicsurplus.com**   - This is in progress and will be done next. Sidenote: their site's html layout makes me want to kill myself.
* **go-dove.com**         - Planned
* **ebay.com**                - Never. Just use https://www.labgopher.com/
