import disnake
import sqlite3
import random
from disnake.ext import commands
import time
earnings = [
    "You work extra hard at the office today, but instead of a promotion, you find a large, uncut diamond in your desk drawer.",
    "You stream your gaming skills for 12 hours straight, and your top subscriber sends you a delivery van full of solid chocolate gold coins.",
    "You write a brilliant novel, and your publisher pays your advance in a single, massive bar of 24-karat gold.",
    "You help an old lady cross the street, and she presses a small, authentic Fabergé egg into your palm as thanks.",
    "You complete a complex online survey, and the reward is a genuine meteorite fragment mounted on a marble stand.",
    "You perform a daring stunt for a viral video, and a sponsor pays you with a chest filled with rare, collectible gemstones.",
    "You sell your old comic book collection, and the buyer throws in a vintage Rolex watch as a bonus.",
    "You work a double shift at the space station, and your bonus is a moon rock in a presentation case.",
    "You solve a difficult problem for a client, and their payment is a handcrafted titanium sculpture worth a fortune.",
    "You water your neighbor's plants, and they return with a small, perfectly formed platinum ingot as a gift.",
    "You win a hot dog eating contest, and the grand prize is a solid silver hot dog statue on a pedestal.",
    "You return a lost wallet, and the owner gives you a painting from their private collection that turns out to be a lost masterpiece.",
    "You babysit some energetic toddlers, and the parents pay you with a bag of rare, uncirculated historical coins.",
    "You attend a focus group, and your compensation is a limited-edition sculpture made of aerogel and gold foil.",
    "You fix a stranger's laptop, and they hand you an antique pocket watch with a solid emerald in the lid.",
    "You clean your attic and find a dusty violin that is identified as a Stradivarius.",
    "You participate in a medical trial, and the thank-you gift is a necklace with a large, flawless sapphire.",
    "You dog-sit for a celebrity's pet, and they give you one of their old championship racing trophies made of solid silver.",
    "You make a funny comment online, and a random billionaire sends you a case of ultra-rare, aged wine from their cellar.",
    "You survive a season on a reality show, and your prize is a custom-made suit of armor inlaid with precious metals."
]
settings = {
    "valuable":"💲",
    "minGet":100,
    "maxGet":200,
    "cooldownWork":10,
    "startBalance":100,
    "modRoleId":1459555929593876661
}
worked = {}


db = sqlite3.connect("TrusikiShowDatabase.sqlite")
cursor = db.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER UNIQUE PRIMARY KEY,
username TEXT UNIQUE NOT NULL,
money INTEGER,
moneyinbank INTEGER
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Servers (
id INTEGER UNIQUE PRIMARY KEY,
guildid INTEGER UNIQUE NOT NULL,
moneysymb STRING NOT NULL,
modroleid INTEGER
)
''')
try:
    cursor.execute("CREATE UNIQUE INDEX ids ON Users (id)")
except:
    print("Index was already created!")
try:
    cursor.execute("CREATE UNIQUE INDEX servids ON Servers (guildid)")
except:
    print("Server Index was already created!")


bot = commands.InteractionBot(intents=disnake.Intents.all())
def getguild(guildid):
    return cursor.execute("SELECT * FROM Servers WHERE guildid = ?",(guildid,)).fetchone()

@bot.slash_command(name="ping")
async def ping(interaction:disnake.AppCommandInteraction):
    await interaction.send("Работает!")
@bot.slash_command(name="deposit")
async def deposit(interaction:disnake.AppCommandInteraction,amount:int):
    if amount > 0:
        moneyafter = cursor.execute("SELECT * FROM Users WHERE username = ?",(interaction.user.name,)).fetchone()[2] - amount
        moneybankafter = cursor.execute("SELECT * FROM Users WHERE username = ?",(interaction.user.name,)).fetchone()[3] + amount
        if moneybankafter > 0 and moneyafter > 0:
            cursor.execute("UPDATE Users SET money = ? WHERE username = ?", (moneyafter, interaction.user.name))
            cursor.execute("UPDATE Users SET moneyinbank = ? WHERE username = ?", (moneybankafter, interaction.user.name))
            await interaction.send(embed=disnake.Embed(title="Deposited " + str(amount) + getguild(interaction.guild_id)[2] + " into bank. Now people cant steal them.\nCurrent balance : " + str(cursor.execute("SELECT * FROM Users WHERE username = ?",(interaction.user.name,)).fetchone()[2]) + getguild(interaction.guild_id)[2] + " in your pocket and " + str(cursor.execute("SELECT * FROM Users WHERE username = ?",(interaction.user.name,)).fetchone()[3]) + getguild(interaction.guild_id)[2] + " in bank."))
        else:
            await interaction.send(embed=disnake.Embed(title="Dont have enough money to deposit."))
    else:
        await interaction.send(embed=disnake.Embed(title="You cant deposit negative money bruh."))
    db.commit()
@bot.slash_command(name="draw")
async def draw(interaction:disnake.AppCommandInteraction,amount:int):
    if amount > 0:
        moneyafter = cursor.execute("SELECT * FROM Users WHERE username = ?",(interaction.user.name,)).fetchone()[2] + amount
        moneybankafter = cursor.execute("SELECT * FROM Users WHERE username = ?",(interaction.user.name,)).fetchone()[3] - amount
        if moneybankafter > 0 and moneyafter > 0:
            cursor.execute("UPDATE Users SET money = ? WHERE username = ?", (moneyafter, interaction.user.name))
            cursor.execute("UPDATE Users SET moneyinbank = ? WHERE username = ?", (moneybankafter, interaction.user.name))
            await interaction.send(embed=disnake.Embed(title="Drew " + str(amount) + getguild(interaction.guild_id)[2] + " from bank. Be careful. People now can steal them.\nCurrent balance : " + str(cursor.execute("SELECT * FROM Users WHERE username = ?",(interaction.user.name,)).fetchone()[2]) + getguild(interaction.guild_id)[2] + " in your pocket and " + str(cursor.execute("SELECT * FROM Users WHERE username = ?",(interaction.user.name,)).fetchone()[3]) + getguild(interaction.guild_id)[2] + " in bank."))
        else:
            await interaction.send(embed=disnake.Embed(title="Dont have enough money to draw."))
    else:
        await interaction.send(embed=disnake.Embed(title="You cant draw negative money bruh."))
    db.commit()

    

@bot.slash_command(name="work")
async def work(interaction:disnake.AppCommandInteraction):
    canwork = False
    if interaction.user.name in worked.keys() and time.time() - worked[interaction.user.name] >= settings["cooldownWork"]:
        canwork = True
    elif interaction.user.name in worked.keys() and not time.time() - worked[interaction.user.name] >= settings["cooldownWork"]:
        await interaction.send(embed=disnake.Embed(title="❌",description="You cant work now! Please wait for " + str(round(settings["cooldownWork"] - (time.time() - worked[interaction.user.name]),1)) + " before using /work again!"))
    else:
        canwork = True
    if canwork:
        chosen = random.choice(earnings)
        money = random.randint(settings["minGet"],settings["maxGet"])
        string = "**SUCCES**\n" + chosen + " You get : " + str(money) + getguild(interaction.guild_id)[2]
        print(string)
        worked[interaction.user.name] = time.time()
        cursor.execute("UPDATE Users SET money = money + ? WHERE username = ?", (money, interaction.user.name))
        await interaction.send(embed=disnake.Embed(description=string,title="✅"))
    db.commit()
@bot.slash_command(name = "set-currency")
async def setcurrency(inter:disnake.AppCommandInteraction,string:str):
    if inter.user.get_role(getguild(inter.guild_id)[3]):
        cursor.execute("UPDATE Servers SET moneysymb = ? WHERE guildid = ?", (string, inter.guild_id))
        db.commit()
        await inter.send(embed=disnake.Embed(title="Server's currency is set to "+string))
    else:
        await inter.send(embed=disnake.Embed(title="❌",description="Not enough permission"))
@bot.event
async def on_ready():
    for guild in bot.guilds:
        try:
            cursor.execute('INSERT INTO Servers (guildid,moneysymb,modroleid) VALUES (?, ?, ?)', (guild.id, "$", 0))
        except:
            print("Server was already created!")
        for client in guild.members:
            try:
                cursor.execute('INSERT INTO Users (username,money,moneyinbank) VALUES (?, ?, ?)', (client.name, 0, settings["startBalance"]))
            except:
                print("User was already registred!")
    db.commit()
    print("Бот готов!")
file = open("env.env","r")
token = file.readline()
file.close()
bot.run(token)

