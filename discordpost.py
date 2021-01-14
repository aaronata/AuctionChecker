from discord_webhook import DiscordWebhook, DiscordEmbed

import time
import configparser

config = configparser.ConfigParser()
config.read('discordtokens.ini')
a_webhookurl = config['Discord']['a_webhookurl']
s_webhookurl = config['Discord']['s_webhookurl']

post_to_a_discord = True
post_to_s_discord = True


def repeatedPost(resultarray):
    # Filter out auctions weve already seen
    f = open('ignore.txt', 'r')
    ignore = f.readlines()
    f.close()
    ignore = [sub.replace('\n', '') for sub in ignore]  # strip out the newlines

    f = open('keywords.txt', 'r')
    keywords = f.readlines()
    f.close()
    keywords = [sub.replace('\n', ' ') for sub in keywords]  # strip out the newlines

    for i in range(0, resultarray['num_of_results']):

        # Check if the auction title matches any keywords.
        if bool([ele for ele in keywords if (ele.lower() in resultarray['title'][i].lower())]):
            # Check if the item has already been seen by the program
            if not bool([ele for ele in ignore if (ele in resultarray['combinedid'][i])]):
                # If not: print the name, add the product to the list of listings checked
                ignore.append(str(resultarray['combinedid'][i]))
                print(resultarray["title"][i])
                # ----- Done when new listing is found ------- #

                if resultarray['listingtype'] == 'auction':
                    if post_to_a_discord: auctionPost(resultarray, i, a_webhookurl)
                    if post_to_s_discord: auctionPost(resultarray, i, s_webhookurl)

                if resultarray['listingtype'] == 'normal':
                    if post_to_a_discord: sellingPost(resultarray, i, a_webhookurl)
                    if post_to_s_discord: sellingPost(resultarray, i, s_webhookurl)

        # Update the list of listings checked
    f = open('ignore.txt', 'w')
    for x in ignore:
        f.write(x + '\n')
    f.close()


def auctionPost(result, i, webhook_url):
    webhook = DiscordWebhook(url=webhook_url)
    embed = DiscordEmbed(title=result['title'][i], description=result['link'][i], color=242424)
    embed.set_image(url=result['picture'][i])
    embed.set_timestamp()

    embed.add_embed_field(name="Price", value=result['price_styleized'][i])
    embed.add_embed_field(name="Bids", value=result['bids'][i])
    embed.add_embed_field(name="Location", value=result['location'][i])
    embed.add_embed_field(name="ID: ", value=result['combinedid'][i])
    embed.set_footer(text="Ends on " + str(result['auctionclose'][i]) + ".    Found")
    webhook.add_embed(embed)
    responce = webhook.execute()
    print('Posted to discord. Status code: ' + str(responce[0].status_code))
    if responce[0].status_code == 200:
        check = False
    else:
        print("Limit reached, waiting 30 seconds")
        time.sleep(29)
    time.sleep(1)


def sellingPost(result, i, webhook_url):
    webhook = DiscordWebhook(url=webhook_url)
    embed = DiscordEmbed(title=result['title'][i], description=result['link'][i], color=242424)
    embed.set_image(url=result['picture'][i])
    embed.set_timestamp()

    embed.add_embed_field(name="Price", value=result['price_styleized'][i])
    embed.add_embed_field(name="Location", value=result['location'][i])
    embed.add_embed_field(name="ID: ", value=result['combinedid'][i])
    embed.set_footer(text="Posted on " + str(result['postdate'][i]) + ".    Found")
    webhook.add_embed(embed)
    responce = webhook.execute()
    print('Posted to discord. Status code: ' + str(responce[0].status_code))
    if responce[0].status_code == 200:
        check = False
    else:
        print("Limit reached, waiting 30 seconds")
        time.sleep(29)
    time.sleep(1)
