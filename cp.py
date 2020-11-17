import discord
import random
import requests
import os
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from itertools import cycle
import datetime
import time
import asyncio
import json


client = commands.Bot(command_prefix = '.')
status = cycle(['with sid', 'GTA V']) 

@client.event

async def on_ready():
    change_status.start()
    print('Bot is ready.')
    

@tasks.loop(seconds = 10000)
async def change_status():
    await client.change_presence(status= discord.Status.do_not_disturb , activity = discord.Game(next(status)))

''' All Commands'''

@client.command()
async def ping(ctx):
    '''Pong'''
    pong = discord.Embed(title='Pong! Response Time:',
    					 description=str(round(client.latency * 1000)) + ' ms',
                         color=0x00ffff)
    pong.set_thumbnail(url = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.IQKhnqVW4dHFT0Cj7aDXdQHaFj%26pid%3DApi&f=1')
    await ctx.send(embed = pong)


@client.command(aliases = ['8ball'])
async def _8ball(ctx, *, question):
    '''Answers a question positively'''
    responses = [
                    "It is certain",
                    "Without a doubt",
                    "You may rely on it",
                    "Yes definitely",
                    "It is decidedly so",
                    "As I see it, yes",
                    "Most likely",
                    "Yes",
                    "Outlook good",
                    "Signs point to yes"
                ]

    ans = discord.Embed(title = '8BALL:',
                        description = "Iam always positive",
                        color = 0x00ffff)
    ans.add_field(name = 'Question:', value = question , inline = True)
    ans.add_field(name = 'Answer:', value = random.choice(responses), inline = True)
    ans.set_thumbnail(url = 'https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.pngmart.com%2Ffiles%2F3%2F8-Ball-Pool-PNG-Photos.png&f=1&nofb=1')
    await ctx.send(embed = ans)
    #await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
    

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    '''Deletes Messages'''
    await ctx.channel.purge(limit = amount)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'.clear [amount of messages] try again')


@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason = 'None'):
    '''Kicks member from the server'''
    await member.kick(reason = reason)    
    await ctx.send(f'{member.mention} was kicked for {reason}')

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = 'None'):
    '''Bans member from the server'''
    await member.ban(reason = reason) 
    await ctx.send(f'{member.mention} was banned for {reason}') 

@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    '''Unbans previously banned member from the server'''
    banned_users = await ctx.guild.bans()
    member_name , member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@client.command()
async def displayembed(ctx):

    embed = discord.Embed(
        title = 'SLYTHERIN HOUSE',
        description = 'best house ever',
        color = 0x0d6127
    )

    embed.set_footer(text = 'Slytherin House info')
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/704625973316026378/711650080226148512/giphy_4.gif')
    embed.set_thumbnail(url = 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.086zKvMuMdA7LrqZdMU8KAHaHB%26pid%3DApi&f=1')
    embed.set_author(name = 'SLYTHERIN', 
    icon_url ='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.086zKvMuMdA7LrqZdMU8KAHaHB%26pid%3DApi&f=1' )
    embed.add_field(name = 'HOUSE HEAD', value = 'Prof. Snape', inline = False)

    await ctx.send(embed = embed)


@client.command()
async def userinfo(ctx, member: discord.Member = None ):
    '''See information about a user or yourself.'''
    server = ctx.guild.name
    member = member or ctx.message.author
    avi = member.avatar_url
    #await ctx.send(f'{member.mention} {server} \n {avi}')

    roles = sorted(member.roles, key=lambda c: c.position)
    roles = roles[::-1]
    color = 0x000000
    for role in roles:
        if str(role.color) != "#000000":
            color = int(str(role.color)[1:], 16)
            break

    rolenamelist = []
    for role in roles:
        if role.name != "@everyone":
            rolenamelist.append(role.name)
    rolenames = ', '.join(rolenamelist) or 'None'
    #await ctx.send(f'{rolenamelist}')

    #time = ctx.message.timestamp
    desc = '{0} is chilling in {1} mode.'.format(member.name,member.status)
    member_number = sorted(ctx.guild.members,key=lambda m: m.joined_at).index(member) + 1
    em = discord.Embed(colour=color,description = desc)
    em.add_field(name='Nick', value=member.nick, inline=False)
    em.add_field(name='Member No.',value=str(member_number),inline = False)
    em.add_field(name='Account Created', value=member.created_at.__format__('%A, %d. %B %Y'))
    em.add_field(name='Join Date', value=member.joined_at.__format__('%A, %d. %B %Y'), inline=False)
    em.add_field(name='Roles', value=rolenames, inline=False)
    em.set_footer(text='User ID: '+str(member.id))
    em.set_thumbnail(url=avi)
    em.set_author(name=member, icon_url='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fpngimg.com%2Fuploads%2Fhacker%2Fhacker_PNG27.png&f=1&nofb=1')
    try:
        await ctx.send(embed=em)
    except discord.HTTPException:
        await ctx.send("I need the embed links permissions to send this")



@client.command(aliases=['s','serverinfo','si'], no_pm=True)
async def server(ctx):
    '''See information about the server.'''
    server = ctx.guild
    
    total_users = len(ctx.guild.members)
    #await ctx.send(f'{server} {total_users}')

    online = len([m.status for m in server.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle or
                      m.status == discord.Status.dnd])
    #await ctx.send(f'{online}')
    text_channels = len([x for x in ctx.guild.channels
                        if x.type == discord.ChannelType.text])
    category_channels = len([x for x in ctx.guild.channels
                        if x.type == discord.ChannelType.category])
    voice_channels = len(server.channels) - text_channels - category_channels
    #await ctx.send(f'{text_channels} and {voice_channels}')
    passed = str(server.created_at)
    created_at = (f'Since {passed[:10]}')
    #await ctx.send(f'{created_at}')

    data = discord.Embed(
        description=created_at,
        colour=0xFF0000)
    data.add_field(name="Region", value=str(server.region), inline= False)
    data.add_field(name="Users", value="{}/{}".format(online, total_users), inline= False)
    data.add_field(name="Text Channels", value=text_channels, inline= False)
    data.add_field(name="Voice Channels", value=voice_channels, inline= False)
    data.add_field(name="Roles", value=len(server.roles), inline= False)
    data.add_field(name="Owner", value=str(server.owner), inline= False)
    data.set_footer(text="Server ID: " + str(server.id))

    if server.icon_url:
        data.set_author(name=server.name, icon_url=server.icon_url)
        data.set_thumbnail(url=server.icon_url)
    else:
        data.set_author(name=server.name)
        print(data.to_dict())

    try:
        await ctx.send(embed=data)
            
    except discord.HTTPException:
        await ctx.send("I need the `Embed links` permission "
                           "to send this")


@client.command(aliases=["ri","role"], no_pm = True)
async def roleinfo(ctx, *, role: discord.Role=None):
    '''Shows information about a role'''
    server = ctx.guild

    if not role:
        role = server.default_role

        
    role_created = role.created_at
    created_on = str(role_created)
    #await ctx.send(f'Created On {role_created}')
    users = len([x for x in server.members if role in x.roles])
    

    em = discord.Embed(colour=role.colour)
    em.set_author(name=role.name)
    em.add_field(name="ID", value=role.id, inline=False)
    em.add_field(name="Users", value=users, inline=False)
    em.add_field(name="Mentionable", value=role.mentionable, inline=False)
    em.add_field(name="Hoist", value=role.hoist, inline=False)
    em.add_field(name="Position", value=role.position, inline=False)
    em.add_field(name="Managed", value=role.managed, inline=False)
    em.add_field(name="Colour", value=str(role.colour), inline=False)
    em.set_footer(text=f'Created On: {created_on[:10]}')

    try:
        await ctx.send(embed=em)
    except discord.HTTPException:
        await ctx.send("I need the `Embed links` permission "
                           "to send this")



@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')   

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

            
            
client.run('BOT TOKEN')
