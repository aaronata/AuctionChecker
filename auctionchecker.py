import AuctionScraper
import discordpost
import time
import configparser


post_to_aaron_discord = True
post_to_sean_discord = False

check_govdeals = False
check_publicsupluss = True

config = configparser.ConfigParser()
config.read('discordtokens.ini')
webhook_url2 = config['Discord']['webhookurl2']
webhook_url =  config['Discord']['webhookurl']

print("Hello! Checking for new auctions now.")

search = AuctionScraper.searchPublicSurpluss(500, 32114, "", 1, 0, 9999)
#print("Found " + str(search['num_of_results']) + " things.")


#if check_publicsupluss:


if check_govdeals:
    # Do a search for Communication/Electronic Equipment
    print("\n\nDoing search for Communication/Electronic Equipment\n")
    search = AuctionScraper.searchGovdeals(100, 32114, "", 28, 0, 9999)
    print("Found " + str(search['num_of_results']) + " things.")

    # Filter out results we dont want
    f = open('keywords.txt', 'r')
    keywords = f.readlines()
    f.close()
    keywords = [sub.replace('\n', ' ') for sub in keywords]  # strip out the newlines

    # Filter out auctions weve already seen
    f = open('ignore.txt', 'r')
    ignore = f.readlines()
    f.close()
    ignore = [sub.replace('\n', '') for sub in ignore]  # strip out the newlines

    discordpost.discordPost(search, webhook_url, ignore, keywords)
    discordpost.discordPost(search, webhook_url2, ignore, keywords)



    # Do a search for Computers, Parts and Supplies
    print("\n\nDoing search for Computers, Parts and Supplies\n")
    search = AuctionScraper.searchGovdeals(100, 32114, "", 29, 0, 9999)
    print("Found " + str(search['num_of_results']) + " things.")

    f = open('keywords.txt', 'r')
    keywords = f.readlines()
    f.close()
    keywords = [sub.replace('\n', ' ') for sub in keywords]  # strip out the newlines

    # Get already seen products from  file
    f = open('ignore.txt', 'r')
    ignore = f.readlines()
    f.close()
    ignore = [sub.replace('\n', '') for sub in ignore]  # strip out the newlines

    discordpost.discordPost(search, webhook_url, ignore, keywords)
    discordpost.discordPost(search, webhook_url2, ignore, keywords)




    # Do a search for Engineering Equipment and Supplies
    print("\n\nDoing search for Engineering Equipment and Supplies\n")
    search = AuctionScraper.searchGovdeals(100, 32114, "", 38, 0, 9999)
    print("Found " + str(search['num_of_results']) + " things.")

    f = open('keywords.txt', 'r')
    keywords = f.readlines()
    f.close()
    keywords = [sub.replace('\n', ' ') for sub in keywords]  # strip out the newlines

    # Get already seen products from  file
    f = open('ignore.txt', 'r')
    ignore = f.readlines()
    f.close()
    ignore = [sub.replace('\n', '') for sub in ignore]  # strip out the newlines

    discordpost.discordPost(search, webhook_url, ignore, keywords)
    discordpost.discordPost(search, webhook_url2, ignore, keywords)
    discordpost.discordPost(search, webhook_url)
    discordpost.discordPost(search, webhook_url2)

