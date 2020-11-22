import discord
import requests
import json
from discord import channel
from discord.ext import commands

TOKEN = "Nzc4NDAzMzI2MzU0MTI4OTE2.X7Relw.QnTXHM7IkylhZhONktC_72xupm0"
client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    activity = discord.Game(name="!faceit help", type=3)
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("Bot is ready!")


@client.command()
async def user(ctx, arg):
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer 46ccb61d-e643-4cd3-a7fe-a36e4bba4a23',
    }
    params = (
        ('nickname', arg),
        ('game', 'csgo'),
    )
    response = requests.get('https://open.faceit.com/data/v4/players?', headers=headers, params=params)
    user = response.json()
    print(user)
    # ============================================================================================================

    player_id = user['player_id']

    def ranking():
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer 46ccb61d-e643-4cd3-a7fe-a36e4bba4a23',
        }

        url = "https://open.faceit.com/data/v4/rankings/games/csgo/regions/EU/players/" + player_id
        response = requests.get(
            url, headers=headers)
        rank = response.json()
        pos = rank['position']
        return pos

    def stats():
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer 46ccb61d-e643-4cd3-a7fe-a36e4bba4a23',
        }

        url = "https://open.faceit.com/data/v4/players/" + player_id + "/stats/csgo"
        response = requests.get(
            url, headers=headers)
        stat = response.json()
        all = stat['lifetime']
        global wins
        global winrate
        global hs
        global kd
        global winstreak
        wins = stat['lifetime']['Wins']
        winrate = stat['lifetime']['Win Rate %'] + " %"
        hs = stat['lifetime']['Average Headshots %'] + " %"
        kd = stat['lifetime']['Average K/D Ratio'] + " k/d"
        winstreak = stat['lifetime']['Longest Win Streak']
        print(all)

    stats()

    try:
        pays = user['country']
    except:
        await ctx.send("Ce joueur n'existe pas...")
    nickname = user['nickname']
    try:
        lvl = user['games']['csgo']['skill_level']
    except:
        await ctx.send("Ce joueur n'a pas rajouté csgo...")
    global idfaceit
    idfaceit = user['player_id']

    elo1 = user['games']['csgo']['faceit_elo']
    steamidxyz = user['platforms']['steam']
    elo = "Elo : " + str(elo1)

    # ============================================================================================================

    def steamid_to_64bit(steamid):
        steam64id = 76561197960265728  # I honestly don't know where
        # this came from, but it works...
        id_split = steamid.split(":")
        steam64id += int(id_split[2]) * 2  # again, not sure why multiplying by 2...
        if id_split[1] == "1":
            steam64id += 1
        return steam64id

    text = "steam"
    steamprofil = "http://steamcommunity.com/profiles/" + str(steamid_to_64bit(steamidxyz))
    steamprofil = "[Steam](" + steamprofil + ")"
    faceitprofil = "https://www.faceit.com/fr/players/" + nickname
    faceitprofil = "[Faceit](" + faceitprofil + ")"
    profil = steamprofil + " // " + faceitprofil

    # ============================================================================================================

    global lvlicon
    lvlicon = "https://i.imgur.com/zW0YZQL.png"
    lvl = str(user['games']['csgo']['skill_level'])
    if lvl == "1":
        lvlicon = "https://i.imgur.com/zW0YZQL.png"
        color=discord.Colour.darker_grey()
    if lvl == "2":
        lvlicon = "https://www.zupimages.net/up/20/47/95q2.png"
        color=discord.Colour.green()
    if lvl == "3":
        lvlicon = "https://i.imgur.com/JzwT1zz.png"
        color = discord.Colour.green()
    if lvl == "4":
        lvlicon = "https://www.zupimages.net/up/20/47/yj48.png"
        color = discord.Colour.gold()
    if lvl == "5":
        lvlicon = "https://i.imgur.com/m8V2jma.png"
        color = discord.Colour.gold()
    if lvl == "6":
        lvlicon = "https://i.imgur.com/rnFa22r.png"
        color = discord.Colour.gold()
    if lvl == "7":
        lvlicon = "https://i.imgur.com/XYBHhEq.png"
        color = discord.Colour.gold()
    if lvl == "8":
        lvlicon = "https://i.imgur.com/P8FMPlG.png"
        color = discord.Colour.orange()
    if lvl == "9":
        lvlicon = "https://i.imgur.com/bF07xuy.png"
        color = discord.Colour.orange()
    if lvl == "10":
        lvlicon = "https://i.imgur.com/2ZDNlBD.png"
        color = discord.Colour.red()

    userstr = "Stats of " + arg
    country = ":flag_" + pays + ":"
    pays = pays.upper()
    ranker = "Rank: " + str(ranking()) + " " + pays + " Rank: "

    # ============================================================================================================

    embed = discord.Embed(title=userstr, colour=color,
                          url="",
                          description=profil)
    embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/2111/2111370.svg")
    embed.set_author(name=elo,
                     icon_url=lvlicon)
    embed.set_footer(text=ranker,
                     icon_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/microsoft/209/earth-globe-europe-africa_1f30d.png")
    embed.add_field(name="Country: ", value=country, inline=True)
    embed.add_field(name="Wins :", value=wins, inline=True)
    embed.add_field(name="WinRate :", value=winrate, inline=True)
    embed.add_field(name="K/D :", value=kd, inline=True)
    embed.add_field(name="HS% :", value=hs, inline=True)
    embed.add_field(name="Winstreak :", value=winstreak, inline=True)
    await ctx.send(embed=embed)


client.run(TOKEN)
