
import discord, random, json, os, time
from discord.ext import commands
from discord.ext.commands import cooldown
from discord import File, Color

#COLOURS
BLUE = 0x3498db
PURPLE = 0x9b59b6
GOLD = 0xf1c40f

os.chdir()

client = commands.Bot(command_prefix = "wish.")

@client.event
async def on_ready():
    print("Wish Bot is ready!")

@client.event
async def on_member_join(member):
    print("{} has joined the server.".format(member))

@client.command()
async def shopchannel(ctx):
    '''
    Creates the Shop text-channel in the Server.
    '''
    guild = ctx.message.guild
    shop = await guild.create_text_channel('💎purchase-with-primogems')

    await shop.set_permissions(guild.default_role,
                                view_channel = True,
                                read_message_history = True,
                                send_messages = False, 
                                add_reactions = False, 
                                manage_permissions = False,
                                manage_channels = False,
                                manage_webhooks = False,
                                manage_messages = False,
                                embed_links = False,
                                attach_files = False,
                                create_instant_invite = False,
                                send_tts_messages = False,
                                use_external_emojis = False,
                                mention_everyone = False)


    acquaint = "🟣"
    intertwined = "🔵"

    emb = discord.Embed(title = "Purchase With Primogems!",color = 0x1abc9c)
    emb.add_field(name = "\u200B",value = "React with {} to purchase Intertwined Fate, or react with {} to purchase Acquaint Fate. Costs 160 Primogems each.".format(acquaint,intertwined))
    message = await shop.send(embed = emb)
    await message.add_reaction(acquaint)
    await message.add_reaction(intertwined)

@client.event
async def on_reaction_add(reaction,user):
    
    if reaction.count > 1:
        await reaction.remove(user)
        await add_traveler(user)
        users = await get_user_data() 

        if reaction.message.channel.name == "💎purchase-with-primogems":

            if users[str(user.id)]["primogems"] >= 160:

                if reaction.emoji == "🟣":
                    users[str(user.id)]["primogems"] -= 160
                    users[str(user.id)]["intertwined"] += 1

                elif reaction.emoji == "🔵":
                    users[str(user.id)]["primogems"] -= 160
                    users[str(user.id)]["acquaint"] += 1
                   
                with open("currencies.json","w") as file:
                    json.dump(users,file)

@client.command()
async def balance(ctx):
    '''
    Client command to check user's balance.
    '''
    await add_traveler(ctx.author)
    user = ctx.author
    users = await get_user_data() 

    primos = users[str(user.id)]["primogems"] 
    intertwined = users[str(user.id)]["intertwined"]
    acquaint = users[str(user.id)]["acquaint"]

    emb = discord.Embed(title = "{} has ".format(ctx.author.name),color = 0x2ecc71)
    emb.add_field(name = "Primogems",value = primos)
    emb.add_field(name = "Intertwined Fates",value = intertwined)
    emb.add_field(name = "Acquaint Fates",value = acquaint)
    await ctx.send(embed = emb)

async def add_traveler(user):

    users = await get_user_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["primogems"] = 1600
        users[str(user.id)]["intertwined"] = 10
        users[str(user.id)]["acquaint"] = 10
        users[str(user.id)]["standard5pity"] = 0
        users[str(user.id)]["standard4pity"] = 0
        users[str(user.id)]["char5pity"] = 0
        users[str(user.id)]["char4pity"] = 0
        users[str(user.id)]["weap5pity"] = 0
        users[str(user.id)]["weap4pity"] = 0
        users[str(user.id)]["chars"] = []
        users[str(user.id)]["weaps"] = []

    with open("currencies.json","w") as file:
        json.dump(users,file)
    return True

async def get_user_data():
    with open("currencies.json","r") as file:
        users = json.load(file)
    
    return users

#EARNING PRIMOGEMS
@client.command()
@cooldown(1,3600,commands.BucketType.user)
async def hourly(ctx):
    '''
    Gives user 60 primogems, can be once claimed every hour.
    '''
    await add_traveler(ctx.author)
    user = ctx.author
    users = await get_user_data() 

    users[str(user.id)]["primogems"] += 60
    await ctx.send("{} has claimed 60 Primogems!".format(ctx.message.author.mention))

    with open("currencies.json","w") as file:
        json.dump(users,file)

@hourly.error
async def hourly_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        if (error.retry_after > 60):
            await ctx.send("{} Hourly Primogems already claimed! Please try again in {:.0f} minute(s).".format(ctx.message.author.mention, (error.retry_after)/60))
        else:
            await ctx.send("{} Hourly Primogems already claimed! Please try again in {:.0f} second(s).".format(ctx.message.author.mention, error.retry_after))

@client.command()
@cooldown(1,86400,commands.BucketType.user)
async def daily(ctx):
    '''
    Gives user 1600 primogems, can be claimed once every day.
    '''
    await add_traveler(ctx.author)
    user = ctx.author
    users = await get_user_data() 

    users[str(user.id)]["primogems"] += 1600

    await ctx.send("{} has claimed 1600 Primogems!".format(ctx.message.author.mention))

    with open("currencies.json","w") as file:
        json.dump(users,file)

@daily.error
async def daily_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        if (error.retry_after > 3600):
            await ctx.send("{} Daily Primogems already claimed! Please try again in {:.0f} hour(s).".format(ctx.message.author.mention, (error.retry_after)/3600))
        elif (error.retry_after > 60):
            await ctx.send("{} Daily Primogems already claimed! Please try again in {:.0f} minute(s).".format(ctx.message.author.mention, (error.retry_after)/60))
        else:
            await ctx.send("{} Daily Primogems already claimed! Please try again in {:.0f} second(s).".format(ctx.message.author.mention, error.retry_after))
        

#BANNERS
@client.command()
async def standard(ctx):
    '''
    The standard Wanderlust Invocation wish.
    '''
    await add_traveler(ctx.author)
    user = ctx.author
    users = await get_user_data() 

    if (users[str(user.id)]["acquaint"] > 0):
        fiveStarChar = ["Jean","QiQi","Keqing","Mona","Diluc"]
        fiveStarWeap = ["Amos' Bow","Skyward Harp","Lost Prayer to the Sacred Winds","Skyward Atlas"
        "Wolf's Gravestone","Skyward Pride", "Primordial Jade Winged-Spear",
        "Skyward Spine", "Aquila Favonia","Skyward Blade"]
        fourStarChar = ["Sucrose","Chongyun","Kaeya","Fischl","Beidou","Razor","Lisa",
        "Noelle","Ningguang","Xingqiu","Barbara","Bennett","Xiangling","Amber","Diona","Xinyan"]
        fourStarWeap = ["Rust","Sacrificial Bow","The Stringless","Favonius Warbow"
        "Eye of Perception","Favonius Codex","Sacrificial Fragments","The Widsith",
        "Rainslasher","Sacrifical Greatsword","The Bell","Favonius Greatsword",
        "Favonius Lance","Dragon's Bane","Lion's Roar","Sacrificial Sword","The Flute",\
        "Favonius Sword"] 
        threeStarWeap = ["Slingshot","Raven Bow","Sharpshooter's Oath","Emerald Orb",
        "Thrilling Tales of Dragon Slayers","Magic Guide","Debate Club",
        "Bloodtainted Greatsword","Ferrous Shadow","Black Tassel","Skyrider Sword",
        "Harbinger of Dawn","Cool Steel"]

        draw = random.uniform(0,100)
        
        if (users[str(user.id)]["standard5pity"] == 89):
            draw = 0.1
        elif (users[str(user.id)]["standard4pity"] == 9):
            draw = 1.0

        if (0 <= draw <= 0.6): #five star
            rarity = "★★★★★"
            stars = "⭐⭐⭐⭐⭐"
            color = GOLD
            weapOrChar = random.randint(0,1)
            if (weapOrChar == 0): #weapon
                itemType = "Weapon"
                weap = random.randint(0,len(fiveStarWeap)-1)
                drop = fiveStarWeap[weap]
            else: #character
                itemType = "Character"
                char = random.randint(0,len(fiveStarChar)-1)
                drop = fiveStarChar[char]
            users[str(user.id)]["standard5pity"] = 0
        elif (0.7 <= draw <= 5.8): #four star
            color = PURPLE
            rarity = "★★★★"
            stars = "⭐⭐⭐⭐"
            weapOrChar = random.randint(0,1)
            users[str(user.id)]["standard5pity"] += 1
            if (weapOrChar == 0): #weapon
                itemType = "Weapon"
                weap = random.randint(0,len(fourStarWeap)-1)
                drop = fourStarWeap[weap]
            else: #character
                itemType = "Character"
                char = random.randint(0,len(fourStarChar)-1)
                drop = fourStarChar[char]
            users[str(user.id)]["standard4pity"] = 0
        else: #three star
            users[str(user.id)]["standard5pity"] += 1
            users[str(user.id)]["standard4pity"] += 1
            rarity = "★★★"
            stars = "⭐⭐⭐"
            color = BLUE
            itemType = "Weapon"
            weap = random.randint(0,len(threeStarWeap)-1)
            drop = threeStarWeap[weap]

        emb = discord.Embed(title = "{} wished on Wanderlust Invocation and received\n".format(ctx.author.name),color = color)
        emb.add_field(name = "Name\n",value = drop,inline = False)
        emb.add_field(name = "Type",value = itemType,inline = False)
        emb.add_field(name = "Rarity",value = stars,inline = False)

        if itemType == "Character":
            file = discord.File("Characters/{}.png".format(drop.lower()),filename = "char_image.png")
            emb.set_image(url="attachment://char_image.png")

            if drop not in users[str(user.id)]["chars"]:
                users[str(user.id)]["chars"].append(drop + " (" + rarity + ")")
        else:
            file = discord.File("Weapons/{}.png".format(drop.lower()),filename = "weap_image.png")
            emb.set_image(url="attachment://weap_image.png")

            if drop not in users[str(user.id)]["weaps"]:
                users[str(user.id)]["weaps"].append(drop + " (" + rarity + ")")

        await ctx.send(file = file, embed = emb)

        users[str(user.id)]["acquaint"] -= 1


        with open("currencies.json","w") as file:
            json.dump(users,file)

    else:
        await ctx.send('Not enough Acquaint Fate to wish on this banner. You can purchase more in the "💎purchase-with-primogems" channel!')

@client.command()
async def character(ctx):
    '''
    The character event wish.
    '''
    await add_traveler(ctx.author)
    user = ctx.author
    users = await get_user_data() 

    if (users[str(user.id)]["intertwined"] > 0):

        rateUp5 = "Albedo"
        rateUp4 = ["Fischl","Bennett","Sucrose"]

        fiveStarChar = ["Albedo","Jean","QiQi","Keqing","Mona","Diluc"]

        fourStarChar = ["Chongyun","Beidou",
        "Noelle","Ningguang","Xingqiu","Xiangling","Diona","Xinyan"]

        fourStarWeap = ["Rust","Sacrificial Bow","The Stringless","Favonius Warbow"
        "Eye of Perception","Favonius Codex","Sacrificial Fragments","The Widsith",
        "Rainslasher","Sacrifical Greatsword","The Bell","Favonius Greatsword",
        "Favonius Lance","Dragon's Bane","Lion's Roar","Sacrificial Sword","The Flute",\
        "Favonius Sword"] 

        threeStarWeap = ["Slingshot","Raven Bow","Sharpshooter's Oath","Emerald Orb",
        "Thrilling Tales of Dragon Slayers","Magic Guide","Debate Club",
        "Bloodtainted Greatsword","Ferrous Shadow","Black Tassel","Skyrider Sword",
        "Harbinger of Dawn","Cool Steel"]

        draw = random.uniform(0,100)
        
        if (users[str(user.id)]["char5pity"] == 89):
            draw = 0.1
        elif (users[str(user.id)]["char4pity"] == 9):
            draw = 1.0

        if (0 <= draw <= 0.6): #five star

            rarity = "★★★★★"
            stars = "⭐⭐⭐⭐⭐"
            color = GOLD
            itemType = "Character"
            featured = random.randint(0,1)

            if featured == 0:
                drop = rateUp5
            else:
                char = random.randint(0,len(fiveStarChar)-1)
                drop = fiveStarChar[char]

            users[str(user.id)]["char5pity"] = 0
            users[str(user.id)]["char4pity"] += 1

        elif (0.7 <= draw <= 5.8): #four star
            rarity = "★★★★"
            stars = "⭐⭐⭐⭐"
            color = PURPLE
            weapOrChar = random.randint(0,1)
            
            if (weapOrChar == 0): #weapon
                itemType = "Weapon"
                weap = random.randint(0,len(fourStarWeap)-1)
                drop = fourStarWeap[weap]
            else: #character
                itemType = "Character"
                featured = random.randint(0,1)

                if featured == 0:
                    char = random.randint(0,len(rateUp4)-1)
                    drop = rateUp4[char]
                else:
                    char = random.randint(0,len(fourStarChar)-1)
                    drop = fourStarChar[char]

            users[str(user.id)]["char4pity"] = 0
            users[str(user.id)]["char5pity"] += 1

        else: #three star
            users[str(user.id)]["char5pity"] += 1
            users[str(user.id)]["char4pity"] += 1
            rarity = "★★★"
            stars = "⭐⭐⭐"
            color = BLUE
            itemType = "Weapon"
            weap = random.randint(0,len(threeStarWeap)-1)
            drop = threeStarWeap[weap]

        emb = discord.Embed(title = "{} wished on Secretum Secretorum and received\n".format(ctx.author.name),color = color)
        emb.add_field(name = "Name\n",value = drop,inline = False)
        emb.add_field(name = "Type",value = itemType,inline = False)
        emb.add_field(name = "Rarity",value = stars,inline = False)

        if itemType == "Character": 
            file = discord.File("Characters/{}.png".format(drop.lower()),filename = "char_image.png")
            emb.set_image(url="attachment://char_image.png")

            if drop not in users[str(user.id)]["chars"]:
                users[str(user.id)]["chars"].append(drop + " (" + rarity + ")")
        else:
            file = discord.File("Weapons/{}.png".format(drop.lower()),filename = "weap_image.png")
            emb.set_image(url="attachment://weap_image.png")

            if drop not in users[str(user.id)]["weaps"]:
                users[str(user.id)]["weaps"].append(drop + " (" + rarity + ")")

        await ctx.send(file = file, embed = emb)


        users[str(user.id)]["intertwined"] -= 1
        with open("currencies.json","w") as file:
            json.dump(users,file)

    else:
        await ctx.send('Not enough Intertwined Fate to wish on this banner. You can purchase more in the "💎purchase-with-primogems" channel!')

@client.command()
async def weapon(ctx):
    '''
    The weapon event wish.
    '''
    await add_traveler(ctx.author)
    user = ctx.author
    users = await get_user_data() 

    if (users[str(user.id)]["intertwined"] > 0):

        rateUp5 = ["Summit Shaper","Skyward Atlas"]
        rateUp4 = ["The Stringless","Sacrificial Fragments","Favonius Greatsword","Favonius Sword","Favonius Lance"]

        fiveStarWeap = ["Amos' Bow","Skyward Harp","Lost Prayer to the Sacred Winds",
        "Wolf's Gravestone","Skyward Pride", "Primordial Jade Winged-Spear",
        "Skyward Spine", "Aquila Favonia","Skyward Blade"]

        fourStarChar = ["Sucrose","Chongyun","Kaeya","Fischl","Beidou","Razor","Lisa",
        "Noelle","Ningguang","Xingqiu","Barbara","Bennett","Xiangling","Amber","Diona","Xinyan"]

        fourStarWeap = ["Rust","Sacrificial Bow","Favonius Warbow"
        "Eye of Perception","Favonius Codex","The Widsith",
        "Rainslasher","Sacrifical Greatsword","The Bell","Dragon's Bane","Lion's Roar","Sacrificial Sword","The Flute"] 

        threeStarWeap = ["Slingshot","Raven Bow","Sharpshooter's Oath","Emerald Orb",
        "Thrilling Tales of Dragon Slayers","Magic Guide","Debate Club",
        "Bloodtainted Greatsword","Ferrous Shadow","Black Tassel","Skyrider Sword",
        "Harbinger of Dawn","Cool Steel"]

        draw = random.uniform(0,100)
        
        if (users[str(user.id)]["char5pity"] == 89):
            draw = 0.1
        elif (users[str(user.id)]["char4pity"] == 9):
            draw = 1.0

        if (0 <= draw <= 0.6): #five star

            rarity = "★★★★★"
            stars = "⭐⭐⭐⭐⭐"
            color = GOLD
            itemType = "Weapon"
            featured = random.randint(0,1)

            if featured == 0:
                weap = random.randint(0,len(rateUp5)-1)
                drop = rateUp5[weap]
            else:
                weap = random.randint(0,len(fiveStarWeap)-1)
                drop = fiveStarWeap[weap]

            users[str(user.id)]["weap5pity"] = 0
            users[str(user.id)]["weap4pity"] += 1

        elif (0.7 <= draw <= 5.8): #four star
            rarity = "★★★★"
            stars = "⭐⭐⭐⭐"
            color = PURPLE
            weapOrChar = random.randint(0,1)
            
            if (weapOrChar == 0): #weapon

                itemType = "Weapon"
                featured = random.randint(0,1)

                if featured == 0:
                    weap = random.randint(0,len(rateUp4)-1)
                    drop = rateUp4[weap]
                else:
                    weap = random.randint(0,len(fourStarChar)-1)
                    drop = fourStarWeap[weap]

            else: #character

                itemType = "Character"
                featured = random.randint(0,1)
                char = random.randint(0,len(fourStarChar)-1)
                drop = fourStarChar[char]

            users[str(user.id)]["weap4pity"] = 0
            users[str(user.id)]["weap5pity"] += 1

        else: #three star
            users[str(user.id)]["weap5pity"] += 1
            users[str(user.id)]["weap4pity"] += 1
            rarity = "★★★"
            stars = "⭐⭐⭐"
            color = BLUE
            itemType = "Weapon"
            weap = random.randint(0,len(threeStarWeap)-1)
            drop = threeStarWeap[weap]

        emb = discord.Embed(title = "{} wished on Epitome Invocation and received\n".format(ctx.author.name),color = color)
        emb.add_field(name = "Name\n",value = drop,inline = False)
        emb.add_field(name = "Type",value = itemType,inline = False)
        emb.add_field(name = "Rarity",value = stars,inline = False)

        if itemType == "Character":
            file = discord.File("Characters/{}.png".format(drop.lower()),filename = "char_image.png")
            emb.set_image(url="attachment://char_image.png")

            if drop not in users[str(user.id)]["chars"]:
                users[str(user.id)]["chars"].append(drop + " (" + rarity + ")")

        else:
            file = discord.File("Weapons/{}.png".format(drop.lower()),filename = "weap_image.png")
            emb.set_image(url="attachment://weap_image.png")

            if drop not in users[str(user.id)]["weaps"]:
                users[str(user.id)]["weaps"].append(drop + " (" + rarity + ")")

        await ctx.send(file = file, embed = emb)
        
            
        users[str(user.id)]["intertwined"] -= 1
        with open("currencies.json","w") as file:
            json.dump(users,file)

    else:
        await ctx.send('Not enough Intertwined Fate to wish on this banner. You can purchase more in the "💎purchase-with-primogems" channel!')

#USER'S COLLECTION
@client.command()
async def collection(ctx):
    '''
    Checks user's full collection of characters and weapons.
    '''
    await add_traveler(ctx.author)
    user = ctx.author
    users = await get_user_data() 
    emb = discord.Embed(title = "{}'s Collection".format(ctx.author.name),color = 0x2ecc71)

    charList = ""
    weapList = ""

    for i in users[str(user.id)]["chars"]:
        charList += i + "\n"
    for j in users[str(user.id)]["weaps"]:
        weapList += j + "\n"

    if charList != "":
        emb.add_field(name = "Characters",value = charList)
    if weapList != "":
        emb.add_field(name = "Weapons",value = weapList,inline = False)

    await ctx.send(embed = emb)

client.run()
