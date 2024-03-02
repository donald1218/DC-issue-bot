# 導入Discord.py模組
import discord
# 導入commands指令模組
from discord.ext import commands,tasks
import json

DC_token = ""
channel_ID = 0

with open("secrets.json") as f:
    data = json.load(f)
    DC_token = data['dc-token']
    channel_ID = data['channel_ID']


# intents是要求機器人的權限
intents = discord.Intents.all()
# command_prefix是前綴符號，可以自由選擇($, #, &...)
bot = commands.Bot(command_prefix = "%", intents = intents)

issue_with_user = {}

@bot.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")
    test1.start()
    test2.start()

@bot.command()
# 輸入%Hello呼叫指令
async def setting(ctx, user: discord.Member):
    # 替换 CHANNEL_ID 为你想要标记的频道 ID
    global channel_ID
    channel = bot.get_channel(channel_ID)
    if channel:
        await channel.send(f'{user.mention}, 你被标记了！')

@bot.command()
async def assign(ctx, user: discord.Member,*, message: str):
    # 替换 CHANNEL_ID 为你想要标记的频道 ID
    issue_with_user[message]=user
    channel = bot.get_channel(channel_ID)
    print(issue_with_user)
    if channel:
        await channel.send(f' {issue_with_user[message].mention}')   

@bot.command()
async def remove(ctx, *, message: str):
    # 替换 CHANNEL_ID 为你想要标记的频道 ID
    del issue_with_user[message]
    channel = bot.get_channel(channel_ID)
    print(issue_with_user)
    if channel:
        await channel.send(f' {issue_with_user}')   

@tasks.loop(hours=10)  
async def test1():
    channel = bot.get_channel(channel_ID)
    print('test1')
    if channel:
        await channel.send(f'test1') 

@tasks.loop(hours=15)  
async def test2():
    channel = bot.get_channel(channel_ID)
    print('test2')
    if channel:
        await channel.send(f'test2') 

@test1.before_loop
async def before_test1():
    await bot.wait_until_ready()    

@test2.before_loop
async def before_test2():
    await bot.wait_until_ready() 

bot.run(DC_token)
