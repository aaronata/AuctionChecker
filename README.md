# AuctionChecker
This code in its entirety will check various auction/sale sites for keywords in the `keywords.txt` folder and post results to discord using a webhook. 

This currently supports the sites:
* **govdeals.com**
* **publicsurplus.com**
* **craigslist.comm**

## Using my crappy discord hook
I designed it to update two discord webhooks as I also run this for a friend.
You will probably need to remove one of them in `discordpost.py`.
I also have it set up so the webhook urls are in an .ini file. Just manually input the url in place if the configparser line.

You also will need to change the general config settings in the `auctionchecker.py` file and select which sites you want to monitor. Don’t touch the distance unless you know what your doing, publicsurplus is picky as to what value is there and wont return results if its not a supported number. If you actually need to change it, check what distances you can select on public surplus and use one of those.

Finally, add a newline seperated list in `keywords.txt` containing all keywords youw ant the checker to look out for and change the category for each individual search in `auctionchecker.py`. You can find the numbers/letters defining each category by looking at the url for the websites search return. 

Provided is a bat file that runs python. I personally use this with the Microsoft Task Scheduler for scheduled run times.

As it posts to discord, it creates a list called `ignore.txt` so it can keep track of which listsings its already seen.

## Using just the scraper
You can also do your own thing with this. The website scraper is entirely located within `AuctionScraper.py`.
I put lots of comments in it while learning BeautifulSoup. It should be very easy to learn what its doing.

## What is done and what i plan to do
* **govdeals.com**        - This is done and works well enough.
* **publicsurplus.com**   - This is done and works well enough.
* **craigslist.com**     - This is done and works well enough.
* **go-dove.com**         - Maybe. We had crappy experience with them and are not keen on working with go-dove again so this isnt a high priority.
* **ebay.com**            - Never. Just use https://www.labgopher.com/
