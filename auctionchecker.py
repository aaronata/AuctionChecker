import AuctionScraper
import discordpost
import time

check_govdeals = False
check_publicsupluss = False
check_craigslist = True

# General config
zipcode = 32114
disance = 100  # some websites get upset when this is set to values they dont like
maximum_price = 1000

print("Hello! Checking for new auctions now.")

if check_craigslist:
    print("\n\nSearching craigslist orlando\n")
    search = AuctionScraper.searchCraigslist('server', 'sya', 'orlando', 0, maximum_price)
    print("Found " + str(search['num_of_results']) + " things.")
    discordpost.repeatedPost(search)

    print("\n\nSearching craigslist daytona\n")
    search = AuctionScraper.searchCraigslist('server', 'sya', 'daytona', 0, maximum_price)
    print("Found " + str(search['num_of_results']) + " things.")
    discordpost.repeatedPost(search)

if check_publicsupluss:
    print("\n\nSearching public surpluss\n")
    search = AuctionScraper.searchPublicSurpluss(100, 32114, '', 1, 0, maximum_price)
    print("Found " + str(search['num_of_results']) + " things.")
    discordpost.repeatedPost(search)

if check_govdeals:
    # Do a search for Communication/Electronic Equipment
    print("\n\nSearching govdeals for Communication/Electronic Equipment\n")
    search = AuctionScraper.searchGovdeals(100, 32114, "", 28, 0, maximum_price)
    print("Found " + str(search['num_of_results']) + " things.")
    discordpost.repeatedPost(search)

    # Do a search for Computers, Parts and Supplies
    print("\n\nSearching govdeals for Computers, Parts and Supplies\n")
    search = AuctionScraper.searchGovdeals(100, 32114, "", 29, 0, maximum_price)
    print("Found " + str(search['num_of_results']) + " things.")
    discordpost.repeatedPost(search)

    # Do a search for Engineering Equipment and Supplies
    print("\n\nSearching govdeals for Engineering Equipment and Supplies\n")
    search = AuctionScraper.searchGovdeals(100, 32114, "", 38, 0, maximum_price)
    print("Found " + str(search['num_of_results']) + " things.")
    discordpost.repeatedPost(search)
