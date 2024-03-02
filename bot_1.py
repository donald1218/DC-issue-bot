import discord
from discord.ext import commands,tasks
from github import Github
import datetime
import json

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='%',intents = intents)



username = ""
DC_token = ""
channel_ID = 0
repo_name =""

manager= []
issue_with_user = {}

with open("secrets.json") as f:
    data = json.load(f)
    DC_token = data['dc-token']
    channel_ID = data['channel_ID']
    username = data['user_name']
    repo_name = data['repo_name']

g = Github()
user = g.get_user(username)



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    check_github_for_updates.start()
    check_github_for_new.start()

@bot.command()
async def add_manager(ctx, user: discord.Member):
    channel = bot.get_channel(channel_ID)
    if channel:
        if user not in manager:
            manager.append(user)
            await channel.send(f'{user.display_name} has been recorded as an administrator.')
        else:
            await channel.send(f'{user.display_name}  is already an administrator.')

@bot.command()
async def remove_manager(ctx, user: discord.Member):
    channel = bot.get_channel(channel_ID)
    if channel:
        if user not in manager:
            await channel.send(f'{user.display_name} is not an administrator.')
        else:
            manager.remove(user)
            await channel.send(f'{user.display_name}  was removed from administrators.')        

@bot.command()
async def assign(ctx, user: discord.Member,*, message: str):
    issue_with_user[message]=user
    channel = bot.get_channel(channel_ID)
    if channel:
        await channel.send(f'{message} is assigned to {issue_with_user[message].mention}')   

# @tasks.loop(time=datetime.time(hour = 12,minute=0))  
@tasks.loop(minutes=1)
async def check_github_for_new():
    channel = bot.get_channel(channel_ID)
    yesterday = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=1)
    if manager:
        try:
            repo = user.get_repo(repo_name)
            issues = repo.get_issues(state='open',since=yesterday)
            for issue in issues:
                if(issue.created_at>yesterday):
                    message = ', '.join([admin.mention for admin in manager])
                    await channel.send(f'{message} new issue : '+ issue.title)
        except Exception as e:
            print(f'Error occurred while checking GitHub for updates: {e}')


# @tasks.loop(time=datetime.time(hour = 12,minute=1))  
@tasks.loop(minutes=1)
async def check_github_for_updates():
    yesterday = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(minutes=1)
    channel = bot.get_channel(channel_ID)
    if channel:
        await channel.send(f'{issue_with_user} ')
        try:
            repo = user.get_repo(repo_name)
            issues = repo.get_issues(state='open',since=yesterday)
            for issue in issues:
                if(issue.created_at<yesterday):
                    if(issue.title in issue_with_user):
                        await channel.send(f'{issue_with_user[issue.title].mention} '+issue.title+' is update ')
                    else:
                        await channel.send(f'test 6 ')
        except Exception as e:
            print(f'Error occurred while checking GitHub for updates: {e}')


@check_github_for_updates.before_loop
async def before_check_github_for_updates():
    await bot.wait_until_ready()

@check_github_for_new.before_loop
async def before_check_github_for_new():
    await bot.wait_until_ready()

bot.run(DC_token)


