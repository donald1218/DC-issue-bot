# 導入Discord.py模組
import discord
# 導入commands指令模組
from discord.ext import commands
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



@bot.event
# 當機器人完成啟動
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")

@bot.command()
# 輸入%Hello呼叫指令
async def setting(ctx, user: discord.Member):
    # 替换 CHANNEL_ID 为你想要标记的频道 ID
    global channel_ID
    channel = bot.get_channel(channel_ID)
    if channel:
        await channel.send(f'{user.mention}, 你被标记了！')
        

bot.run(DC_token)
