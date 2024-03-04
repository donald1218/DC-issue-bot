import discord
from discord.ext import commands,tasks
from github import Github
import datetime
import json

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!',intents = intents)



username = ""
DC_token = ""
channel_ID = 0
repo_name =""

managers= []
issue_with_user = {}
with open("issue.json") as f:
    issue_with_user = json.load(f)


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
    check_github_for_closed.start()
    with open("data.json") as f:
        manager = json.load(f)
        channel = bot.get_channel(channel_ID)
        if channel:
            users = channel.members
            for user in users :
                if(user.name in manager):
                    managers.append(user)

@bot.command()
async def add_manager(ctx, user: discord.Member):
    channel = bot.get_channel(channel_ID)

    if channel:
        if user not in managers:
            managers.append(user)
            with open("data.json") as f:
                names = json.load(f)
                names.append(user.name)
            with open("data.json","w") as f:
                json.dump(names,f,indent=3)
            await channel.send(f'{user.display_name} has been recorded as an administrator.')
        else:
            await channel.send(f'{user.display_name}  is already an administrator.')

@bot.command()
async def remove_manager(ctx, user: discord.Member):
    channel = bot.get_channel(channel_ID)
    if channel:
        if user not in managers:
            await channel.send(f'{user.display_name} is not an administrator.')
        else:
            managers.remove(user)
            await channel.send(f'{user.display_name}  was removed from administrators.')        

@bot.command()
async def assign(ctx, user: discord.Member,*, message: str):
    issue_with_user[message]=user.name
    channel = bot.get_channel(channel_ID)
    if channel:
        await channel.send(f'issue #{message} is assigned to {user.mention}')
        with open("issue.json","w") as f:
            json.dump(issue_with_user,f,indent=3)

@tasks.loop(time=datetime.time(hour = 4,minute=30))
async def check_github_for_new():
    channel = bot.get_channel(channel_ID)
    yesterday = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=1)
    if managers:
        try:
            repo = user.get_repo(repo_name)
            issues = repo.get_issues(state='open',since=yesterday)
            for issue in issues:
                if(issue.created_at>yesterday):
                    message = ', '.join([admin.mention for admin in managers])
                    await channel.send(f'{message} new issue : #'+ str(issue.number))
                    await channel.send(issue.html_url)
                    
        except Exception as e:
            print(f'Error occurred while checking GitHub for updates: {e}')


@tasks.loop(time=datetime.time(hour = 4,minute=31)) 
async def check_github_for_updates():
    yesterday = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=1)
    td = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(minutes=1)
    channel = bot.get_channel(channel_ID)
    if channel:
        try:
            repo = user.get_repo(repo_name)
            issues = repo.get_issues(state='open',since=yesterday)
            for issue in issues:
                if(issue.created_at<td):
                    for key in issue_with_user:
                        if(int(key) == issue.number):
                            users = channel.members
                            for member in users:
                                if(member.name == issue_with_user[str(issue.number)]):
                                    await channel.send(f'{member.mention} issue #'+str(issue.number)+' is update ')
                            await channel.send(issue.html_url)
                            break
        except Exception as e:
            print(f'Error occurred while checking GitHub for updates: {e}')

@tasks.loop(time=datetime.time(hour = 4,minute=0)) 
async def check_github_for_closed():
    try:
        repo = user.get_repo(repo_name)
        issues = repo.get_issues(state='open')
        delete = []
        for issue_num in issue_with_user:
                isOpen = False
                for issue in issues:
                    if(issue.number==int(issue_num)):
                        isOpen = True
                        break
                if(isOpen==False):
                    delete.append(issue_num)

        for num in delete:
            del issue_with_user[num]
        with open("issue.json","w") as f:
            json.dump(issue_with_user,f,indent=3)

    except Exception as e:
        print(f'Error occurred while checking GitHub for updates: {e}')


@check_github_for_updates.before_loop
async def before_check_github_for_updates():
    await bot.wait_until_ready()

@check_github_for_new.before_loop
async def before_check_github_for_new():
    await bot.wait_until_ready()

@check_github_for_closed.before_loop
async def before_check_github_for_closed():
    await bot.wait_until_ready()


bot.run(DC_token)


