from discord_webhook import DiscordWebhook, DiscordEmbed

import time


def discordPost(resultarray, webhook_url, ignore, keywords):


    # Time to sort results
    for i in range(0, resultarray['num_of_results']):

        # Check if the auction title matches any keywords.
        if bool([ele for ele in keywords if (ele.lower() in resultarray['title'][i].lower())]):
            # Check if the item has already been seen by the program
            if not bool([ele for ele in ignore if (ele in resultarray['combinedid'][i])]):
                # If not: print the name, add the product to the list of listings checked
                print(resultarray["title"][i])
                ignore.append(str(resultarray['combinedid'][i]))


                webhook = DiscordWebhook(url=webhook_url)
                embed = DiscordEmbed(title=resultarray['title'][i], description=resultarray['link'][i], color=242424)
                embed.set_image(url=resultarray['picture'][i])
                embed.set_timestamp()

                embed.add_embed_field(name="Price", value=resultarray['price_styleized'][i])
                embed.add_embed_field(name="Bids", value=resultarray['bids'][i])
                embed.add_embed_field(name="Location", value=resultarray['location'][i])
                embed.add_embed_field(name="ID: ", value=resultarray['ID'][i])
                embed.set_footer(text="Ends on " + str(resultarray['auctionclose'][i]) + ".    Found")
                webhook.add_embed(embed)
                responce = webhook.execute()
                if responce.status_code == 204:
                    check = False
                else:
                    print("Limit reached, waiting 30 seconds")
                    time.sleep(29)
                time.sleep(1)



    # Update the list of listings checked
    f = open('ignore.txt', 'w')
    for x in ignore:
        f.write(x + '\n')
    f.close()