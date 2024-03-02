import discord
from discord.ext import commands,tasks
from github import Github
import datetime
import json

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!',intents = intents)


username = ""
g = Github()
user = g.get_user(username)

DC_token = ""
channel_ID = 0

with open("secrets.json") as f:
    data = json.load(f)
    DC_token = data['dc-token']
    channel_ID = data['channel_ID']

manager= []

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    check_github_for_updates.start()
    check_github_for_new.start()

@bot.command()
async def add_manager(ctx, user: discord.Member):
    if user not in manager:
        manager.append(user)
        await ctx.send(f'{user.display_name} has been recorded as an administrator.')
    else:
        await ctx.send(f'{user.display_name}  is already an administrator.')

@bot.command()
async def remove_manager(ctx, user: discord.Member):
    if user not in manager:
        await ctx.send(f'{user.display_name} is not an administrator.')
    else:
        manager.remove(user)
        await ctx.send(f'{user.display_name}  was removed from administrators.')        


@tasks.loop(datetime.time(hour = 12,minute=0))  
async def check_github_for_new():
    global channel_ID
    channel = bot.get_channel(channel_ID)
    yesterday = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=1)
    if manager:
        try:
            repo = user.get_repo("free5gc")
            issues = repo.get_issues(state='open',since=yesterday)
            for issue in issues:
                if(issue.created_at>yesterday):
                    message = ', '.join([admin.mention for admin in manager])
                    await channel.send(f'{message} new issue : '+ issue.title)
        except Exception as e:
            print(f'Error occurred while checking GitHub for updates: {e}')

    else:
        await channel.send('There are currently no recorded administrators。')

@tasks.loop(datetime.time(hour = 12,minute=1))  
async def check_github_for_updates():
    global channel_ID
    yesterday = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=1)
    channel = bot.get_channel(channel_ID)
    if manager:
        try:
            repo = user.get_repo("free5gc")
            issues = repo.get_issues(state='open',since=yesterday)
            for issue in issues:
                if(issue.created_at<yesterday):
                    message = ', '.join([admin.mention for admin in manager])
                    await channel.send(f'{message} issue update : '+ issue.title)
        except Exception as e:
            print(f'Error occurred while checking GitHub for updates: {e}')
    else:
        await channel.send('There are currently no recorded administrators。')


@check_github_for_updates.before_loop
async def before_check_github_for_updates():
    await bot.wait_until_ready()

@check_github_for_new.before_loop
async def before_check_github_for_new():
    await bot.wait_until_ready()

bot.run(DC_token)


