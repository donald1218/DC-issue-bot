# 導入Discord.py模組
import discord
# 導入commands指令模組
from discord.ext import commands,tasks
import json

DC_token = ""
channel_ID = 0

# intents是要求機器人的權限
intents = discord.Intents.all()
# command_prefix是前綴符號，可以自由選擇($, #, &...)
bot = commands.Bot(command_prefix = "%", intents = intents)

issue_with_user = {}


with open("secrets.json") as f:
    data = json.load(f)
    DC_token = data['dc-token']
    channel_ID = data['channel_ID']

manager = []





# with open("data.json") as f:
#     data = json.load(f)
#     manager = data['users']






@bot.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")
    test1.start()
    test2.start()
    with open("data.json") as f:
        managers = json.load(f)
        channel = bot.get_channel(channel_ID)
        if channel:
            users = channel.members
            for user in users :
                if(user.name in managers):
                    manager.append(user)

@bot.command()
# 輸入%Hello呼叫指令
async def setting(ctx, user: discord.Member):
    # 替换 CHANNEL_ID 为你想要标记的频道 ID
    channel = bot.get_channel(channel_ID)
    if channel:
        await channel.send(f'{user.mention}, 你被标记了！')

@bot.command()
async def add_manager(ctx, user: discord.Member):
    channel = bot.get_channel(channel_ID)
    if channel:
        if user not in manager:
            manager.append(user)
            with open("data.json") as f:
                names = json.load(f)
                names.append(user.name)
            with open("data.json","w") as f:
                json.dump(names,f,indent=3)
            await channel.send(f'{user.display_name} has been recorded as an administrator.')
        else:
            await channel.send(f'{user.display_name}  is already an administrator.')

@bot.command()
async def assign(ctx, user: discord.Member,*, message: str):
    channel = bot.get_channel(channel_ID)
    # 替换 CHANNEL_ID 为你想要标记的频道 ID
    issue_with_user[message]=user
    print(issue_with_user)
    if channel:
        await channel.send(f' {issue_with_user[message].mention}')   

@bot.command()
async def remove(ctx, *, message: str):
    channel = bot.get_channel(channel_ID)
    # 替换 CHANNEL_ID 为你想要标记的频道 ID
    del issue_with_user[message]
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
