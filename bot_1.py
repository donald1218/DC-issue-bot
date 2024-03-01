import discord
from discord.ext import commands,tasks
from github import Github
import datetime

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!',intents = intents)

DISCORD_TOKEN = ""

username = ""
g = Github()
user = g.get_user(username)
channak_ID = 0

lasttime = datetime.datetime(2024,1,1,0,0,0, tzinfo=datetime.timezone.utc)

manager= []

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    check_github_for_updates.start()

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


@tasks.loop(hours=24)  
async def check_github_for_updates():
    global lasttime
    channel = bot.get_channel(channak_ID)
    if manager:
        try:
            repo = user.get_repo("free5gc")
            issues = repo.get_issues(state='open',since=lasttime)
            issues = issues[:issues.totalCount-1]
            for issue in issues:
                print(issue.title,issue.updated_at)
                message = ', '.join([admin.mention for admin in manager])
                await channel.send(f'{message} new issue : '+ issue.title)
                if(issue.updated_at>lasttime):
                    lasttime = issue.updated_at

        except Exception as e:
            print(f'Error occurred while checking GitHub for updates: {e}')

    else:
        await channel.send('There are currently no recorded administrators。')


@check_github_for_updates.before_loop
async def before_check_github_for_updates():
    await bot.wait_until_ready()

bot.run(DISCORD_TOKEN)


