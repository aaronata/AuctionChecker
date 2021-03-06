import requests
from bs4 import BeautifulSoup
import re
import time


# This searches govdeals.com. This is fully working.
# I added lots of comments while learning BeautifulSoup so it should be easy to follow
def searchGovdeals(distance, zipcode, search_term, category, from_price, to_price):
    # Category numbers. You can find the rest by looking at the URL on the actual website
    # 28:Communication/Electronic Equipment
    # 29:Computers, Parts and Supplies
    # 38:Engineering Equipment and Supplies

    rowcount = 9999

    # Get the number of results because govdeals sucks. If you ask for more results then there are, they only give you 10.
    URL = 'https://www.govdeals.com/index.cfm?fa=Main.AdvSearchResultsNew&additionalParams=true&searchPg=Advanced&timing=bySimple&timeType=&locationType=miles&miles=' + str(distance) + '&zipCode=' + str(zipcode) + '&milesKilo=miles&kWord=' + search_term + '&kWordSelect=1&category=' + str(category) + '&sPrice=' + str(from_price) + '&ePrice=' + str(to_price) + '&whichForm=&rowCount=' + str(rowcount) + '&sortOption=aa'
    page = requests.get(URL)  # Get the page with http GET
    soup = BeautifulSoup(page.content, 'html.parser')  # Setup parser
    rowcount = soup.find('div', id='pagination_2')
    if rowcount == None:  # Check if there are results at all
        rowcount = 0
    else:
        rowcount = int(rowcount.text.split("of ")[1])

    # initialize lists
    picture = []
    link = []
    title = []
    ID = []
    location = []
    auctionclose = []
    price = []
    price_styleized = []
    bids = []
    itemid = []
    sellerid = []
    combinedid = []
    num_of_results = rowcount

    if rowcount > 0:  # if there are results, do a search and get all the results on one page
        URL = 'https://www.govdeals.com/index.cfm?fa=Main.AdvSearchResultsNew&additionalParams=true&searchPg=Advanced&timing=bySimple&timeType=&locationType=miles&miles=' + str(distance) + '&zipCode=' + str(zipcode) + '&milesKilo=miles&kWord=' + search_term + '&kWordSelect=1&category=' + str(category) + '&sPrice=' + str(from_price) + '&ePrice=' + str(to_price) + '&whichForm=&rowCount=' + str(rowcount) + '&sortOption=aa'

        page = requests.get(URL)  # Get the page
        soup = BeautifulSoup(page.content, 'html.parser')  # Setup parser

        results = soup.find(id='container_srch_results')  # Get the container that is the results

        indiv_results = results.find_all('div', id='boxx_row')  # Create an array of all listings

        for indiv_results in indiv_results:  # for as many times as there are results
            picture_elem = indiv_results.find('div', id='result_col_1')  # Get the picture div
            picture_elem = picture_elem.find('a')['href']  # get the url from the <a> tag

            title_elem = indiv_results.find('div', id='result_col_2')  # Get the title of the listing with a bunch of stuff in it
            link_elem = title_elem.find('a')['href']  # Get a link to it from the <a> tag
            ID_elem = title_elem.find('div', class_='small')  # Get whatever this is
            title_elem = title_elem.find('a')  # Strip the rest of the stuff and leave the title

            location_elem = indiv_results.find('div', id='result_col_3')  # Get the location of the listing
            auctionclose_elem = indiv_results.find('div', id='result_col_4')  # Get the closing time
            price_elem = indiv_results.find('div', id='result_col_5')  # Get the price and bids

            picture.append("https://www.govdeals.com/" + picture_elem)  # Make them not relative links
            link.append("https://www.govdeals.com/" + link_elem)

            itemid.append(link_elem.split("?")[1].split("&")[1].split("=")[1])  # find the items id from the found URL
            sellerid.append(link_elem.split("?")[1].split("&")[2].split("=")[1])  # find the sellers id from the found url
            combinedid.append(str(link_elem.split("?")[1].split("&")[1].split("=")[1]) + str(link_elem.split("?")[1].split("&")[2].split("=")[1]))

            title.append(re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', title_elem.text.strip(), flags=re.M))
            # These get things, strip off spaces, tabs, newlines, \ns, \rs, \whateverthefucks,and it also slices and dices them into what i want.
            ID.append(re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', ID_elem.text.strip(), flags=re.M))
            location.append(re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', location_elem.text.strip(), flags=re.M).split(":\r\n")[1])
            auctionclose.append(re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', auctionclose_elem.text.strip('\n'), flags=re.M).replace('\n', '').replace('\xa0', '').replace('\r', '').split(':', 1)[1])
            price_split = re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', price_elem.text.strip(), flags=re.M).replace('\r', '').replace('\xa0', '').split(':\n\n', 1)[1].split('\n')

            price_styleized.append(price_split[0])  # Separates the price and the number of bids
            price.append(float(price_split[0].replace("$", "").replace(",", "")))

            if len(price_split) == 2:  # Sets bids to zero if it doesnt say how many there are.
                bids.append(price_split[1].split(':')[1].replace(' ', ''))
            else:
                bids.append(0)

    # so this is what we got:
    # picture
    # link
    # title
    # ID
    # location
    # auctionclose
    # price
    # price_styleized
    # bids
    # num_of_results
    # itemid
    # sellerid

    result_list = {}
    result_list['listingtype'] = 'auction'
    result_list["num_of_results"] = num_of_results
    result_list["picture"] = picture
    result_list["link"] = link
    result_list["title"] = title
    result_list["ID"] = ID
    result_list["location"] = location
    result_list["auctionclose"] = auctionclose
    result_list["price"] = price
    result_list["price_styleized"] = price_styleized
    result_list["bids"] = bids
    result_list["itemid"] = itemid
    result_list["sellerid"] = sellerid
    result_list["combinedid"] = combinedid

    return result_list


def searchPublicSurpluss(distance, zipcode, search_term, category, from_price, to_price):
    # 1:Computers

    picture = []
    link = []
    title = []
    ID = []
    location = []
    auctionclose = []
    price = []
    price_styleized = []
    bids = []
    combinedid = []

    pagenumber = 0
    URL = 'https://www.publicsurplus.com/sms/browse/search?posting=y&slth=&page=' + str(pagenumber) + '&sortBy=timeLeft&keyWord=' + search_term + '&catId=' + str(category) + '&endHours=-1&startHours=-1&lowerPrice=' + str(from_price) + '&higherPrice=' + str(to_price) + '&milesLocation=' + str(distance) + '&zipCode=' + str(zipcode) + '&region=&search=Search'
    # empty results
    # URL = 'https://www.publicsurplus.com/sms/browse/search?posting=y&slth=&page=0&sortBy=timeLeft&keyWord=keywordtest&catId=1&endHours=-1&startHours=-1&lowerPrice=69&higherPrice=420&milesLocation=300&zipCode=32114&region=&search=Search'
    print(URL)
    page = requests.get(URL)  # Get the page with http GET
    soup = BeautifulSoup(page.content, 'html.parser')  # Setup parser
    mainDiv = soup.find('div', class_='baseDiv')

    tbody = mainDiv.find_all('table')[1]  # Get the table of results
    listings = tbody.find_all('tr')  # Get individual listings.
    listings.pop(0)  # Pop the first element because its just the top of the table with the column titles

    print("Found " + str(len(listings)) + " auctions.")

    num_of_results = len(listings)

    print("Working", end='')
    for listings in listings:
        print(".", end='')
        listing = listings.find_all('td')  # Split out the individual elements of the listing

        title.append(listing[1].text.strip())  # Get the title
        # print(listing[1].text.strip())
        link.append("https://www.publicsurplus.com" + listing[1].find('a')['href'])  # Get URL of the auction
        ID.append(listing[0].text.strip())  # Get ID of auction
        combinedid.append(listing[0].text.strip())
        auctionclose.append(listing[4].text.strip())  # Get the date the auction closes
        price_styleized.append(listing[5].text.strip())  # Get the raw and stylized prices
        price.append(float(listing[5].text.strip().replace("$", "").replace(",", "")))

        # https: // d37qv0n5b4mbzm.cloudfront.net / sms / docviewer / cdnaucdoc / img / 2667227 / 38799047
        # https: // d37qv0n5b4mbzm.cloudfront.net / sms / docviewer / cdnmainaucdoc / thumb - s / 2667227 / 38799047

        picture_url = listing[2].find('img')['src'].split('/')  # Do some trickary with the url to get the actual picture.
        picture_url[5] = 'cdnaucdoc'  # This is what happens when old people program.
        picture_url[6] = 'img'  # It makes you have to do this kind of stuff.
        picture_url = '/'.join(picture_url)  # Also the syntax of this command is stupid.
        picture.append(picture_url)  # Get URL of picture

        if True:
            # Time to get the other things. Need to look at the auction page because its not on the search page.
            time.sleep(0.1)  # Make sure you dont spam their website too quickly.

            auction_url = "https://www.publicsurplus.com" + listing[1].find('a')['href']
            auction_page = requests.get(auction_url)  # Get the page with http GET
            auction_soup = BeautifulSoup(auction_page.content, 'html.parser')  # Setup parser

            auction_mainDiv = auction_soup.find('div', class_='baseDiv')
            auction_table = auction_mainDiv.find_all('table')[3]  # Get the second table in the website. No clue where the first one is.
            the_actual_table = auction_table.find('table')  # Get yet another table, this with with the actual info i want. Whats with these people and tables.

            # i just want to point out theres at least 4 nested tables on this page

            the_actual_stuff_i_want = the_actual_table.find_all('tr')  # Split out the individual elements of the listing

            bids.append(the_actual_stuff_i_want[3].find('td', class_="aucinfo").text.strip())  # Get number of bids

            # Get the address. Starting from end of the lists cause this website sucks ass and sometimes certain rows dont show up so the table size changes
            address = the_actual_stuff_i_want[len(the_actual_stuff_i_want) - 4].find('td', class_="aucinfonb").find_all('div')
            location.append(address[len(address) - 1].text.strip().split(',')[0])

            # This get the description. I dont need though so im not going to finish this code.
            # Should be really easy to get going if needed/
            '''description_table = auction_mainDiv.find_all('table')[6]  # Desctiption table. Tables tables tables tables tables
            description_div = description_table.find('div')
            description = description_div.find_all('p')         # List of all paragraphs for the description.
            for d in description:
                print(d.text)   '''
            # description.append()



    result_list = {}
    result_list['listingtype'] = 'auction'
    result_list["num_of_results"] = num_of_results
    result_list["picture"] = picture
    result_list["link"] = link
    result_list["title"] = title
    result_list["location"] = location
    result_list["auctionclose"] = auctionclose
    result_list["postdate"] = None  # todo does this break things?
    result_list["price"] = price
    result_list["price_styleized"] = price_styleized
    result_list["bids"] = bids
    result_list["combinedid"] = ID

    return result_list


def searchCraigslist(search_term, category, cl_location, from_price, to_price):
    # Categories:
    #   sya - Computers

    picture = []
    link = []
    title = []
    ID = []
    location = []
    postdate = []
    price = []
    price_styleized = []
    combinedid = []

    # https://orlando.craigslist.org/search/sya?query=server&sort=rel&search_distance=500&postal=29485&min_price=42&max_price=69
    URL = 'https://' + cl_location + '.craigslist.org/search/' + category + '?query=' + search_term + '&sort=rel&min_price=' + str(from_price) + '&max_price=' + str(to_price)
    print(URL)

    page = requests.get(URL)  # Get the page with http GET
    soup = BeautifulSoup(page.content, 'html.parser')  # Setup parser
    num_of_results = int(soup.find('span', class_='rangeTo').text)  # Get the number of listings
    # Limited to 100something because it doesnt support multiple pages
    mainDiv = soup.find('ul', class_='rows')
    listings = mainDiv.find_all('li')  # Get the listings
    listings = listings[:num_of_results]  # Strip the non local listings

    for listing in listings:
        ID.append(listing.attrs['data-pid'])
        price.append(int(listing.find('span', class_='result-price').text[1:].replace(",", "")))
        price_styleized.append(listing.find('span', class_='result-price').text)
        pictureid = listing.find('a', class_='result-image gallery').attrs['data-ids'].split(',')[0][2:]
        picture.append('https://images.craigslist.org/' + pictureid + '_600x450.jpg')
        postdate.append(listing.find('time', class_='result-date').text.strip())
        title.append(listing.find('h3', class_='result-heading').text.strip())
        link.append(listing.find('a').attrs['href'])
        if listing.find('span', class_='result-hood'):
            location.append(listing.find('span', class_='result-hood').text[2:-1])
        else:
            location.append('No location listed')

    result_list = {}
    result_list["num_of_results"] = num_of_results  #
    result_list['listingtype'] = 'normal'
    result_list["picture"] = picture  #
    result_list["link"] = link  #
    result_list["title"] = title  #
    result_list["location"] = location  #
    result_list["postdate"] = postdate  #
    result_list["auctionclose"] = None
    result_list["price"] = price  #
    result_list["price_styleized"] = price_styleized
    result_list["combinedid"] = ID  #

    return result_list


def searchGoDove(distance, zipcode, search_term, category, from_price, to_price):
    pagenumber = 1
    URL = 'https://www.go-dove.com/search?isAdvSearch=1&whichForm=item&timing=bySimple&timeType=atauction&category=215%2C29%2C217%2C219%2C220%2C221%2C222&categoryName=Computers+and+Networking&kWord=' + search_term + '&sPrice=' + str(from_price) + '&ePrice=' + str(to_price) + '&companyName=&model=&makebrand=&year=&ps=100&pn=' + str(pagenumber) + '&locationType=miles&zipcode=' + str(zipcode) + '&miles=' + str(distance) + '&milesKilo=miles&showMap=false&sf=currentbid&so=asc&results=noresults'
    print(URL)
    page = requests.get(URL)  # Get the page with http GET
    soup = BeautifulSoup(page.content, 'html.parser')  # Setup parser
    rowcount = soup.find('div', id='pagination_2')
    if rowcount == None:  # Check if there are results at all
        rowcount = 0
    else:
        rowcount = int(rowcount.text.split("of ")[1])
