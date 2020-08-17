import discord
from discord.ext import commands

import random
import math
from datetime import datetime

# links bot to application
token_file = open("token.txt", "r")
token = token_file.read()
token_file.close()

# create instance of a bot
client = commands.Bot(command_prefix=".")

# personal note: @client.event is an method decorator. discord.event() is called whenever
# something happens, by using the method decorator we add extra code to the method
@client.event
async def on_ready():
    # setup after initialization
    print("Bot is ready.")

@client.event
async def on_member_join(member):
    print(f"{member} has joined a server.")

@client.event
async def on_member_remove(member):
    print(f"{member} has left a server")

# method names become what to call (for instance, def ping is called with .ping)
# ctx is just the text typed (context)
@client.command()
async def ping(ctx):
    await ctx.send(f"pong! {round(client.latency * 1000)}ms")

# note: discord.py separates variables by spaces by default. * tells it not to do that
@client.command(aliases=['8ball','fortune'])
async def _8ball(ctx, *, question):
    responses = ["It is certain",
                "yeah",
                "maybe",
                "idk bro",
                "prob not",
                "Very doubtful."]
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")
    
    print("Returned fortune.")

@client.command()
async def clear(ctx, amount=5):
    guild = ctx.guild
    await ctx.channel.purge(limit=amount)
    print(f"Cleared {amount} messages")

@client.command()
async def firstMessage(ctx):
    # not sure if this works
    # channel = client.get_channel(691044588126994445)
    guild = client.get_guild(691044588126994442)
    channel_list = guild.text_channels
    for channel in channel_list:
        messages = await channel.history(limit=50, oldest_first=True).flatten()
        if len(messages) == 0: continue

        # channels are objects
        raw_channel = channel.name
        # messages are objects too
        raw_message = None
        for i in range(len(messages)):
            if messages[i].type == discord.MessageType.new_member:
                continue
            else:
                raw_message = messages[i].clean_content
                break
        
        await ctx.send(f"First message in channel <{raw_channel}>: {raw_message}")
    
    print("Found all first messages")


@client.command()
async def listMessages(ctx, member : discord.Member):
    filepath = f"scrapes/{member.display_name}"
    guild = ctx.guild
    channel_list = guild.text_channels
    for channel in channel_list:
        async for message in channel.history(limit=2000):
            if message.author == member:
                await ctx. send(f"Sent by {member.display_name}: {message.clean_content}")
    
    print(f"Finished scraping {member.display_name}'s messages")


@client.command()
async def scrapeMessages(ctx, member: discord.Member):
    # only I can do it
    if ctx.message.author.id == 427975421028728844:
        filepath = f"scrapes/{member.display_name}.txt"
        with open(filepath, "a+", encoding="utf-8") as msg_file:
            guild = ctx.guild
            channel_list = guild.text_channels
            print(f"scraping member: {member.display_name}\n\n")
            for channel in channel_list:
                print (f"scraping channel {channel.name}")
                async for message in channel.history(limit=math.inf):
                    if message.author == member and not message.clean_content == "":
                        msg_file.write("\n")
                        msg_file.write(message.clean_content)
                        msg_file.write("\n\n")
                        # await ctx. send(f"Sent by {member.display_name}: {message.clean_content}")
    
        print(f"Finished scraping {member.display_name}'s messages")
    else:
        await ctx.send("Permission not granted. Only callable by @64_bit")
        print("Did not scrape")

client.run(token)
