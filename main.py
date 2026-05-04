import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import random
import json
from pathlib import Path

load_dotenv()
TOKEN = os.environ.get("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="t.", intents=intents)

def tag_files_read(serverid:int):
    path = Path.cwd() / "servers"
    if not path.exists():
        path.mkdir(parents=True,exist_ok=True)

    file_path = path / (str(serverid)+".json")
    if not file_path.exists():
        with open(file_path,"w") as file:
            file.write("{}")
    tags_json = {}
    with open(file_path,"r") as file:
        tags_json = json.loads(file.read())
    return tags_json

def tag_main(new_tag:str,server_tags:dict):
    if new_tag in server_tags.keys():
        return server_tags[new_tag]
    else:
        return "tag "

def tag_create(data:str,server_tags:dict):
    if data == None:
        return "nothing specified dumbfuck"
    cutoff = data.find(" ")
    if cutoff == -1:
        return "no tag contents specified"
    tag_name = data[:cutoff].strip()
    tag_contents = data[cutoff + 1:].strip()
    server_tags[tag_name] = tag_contents
    return f"tag `{tag_name}` created"

def tag_random(server_tags:dict):
    chosen_tag = random.choice(list(server_tags))
    tag_contents = server_tags[chosen_tag]
    return f"showing tag: `{chosen_tag}`\n\n{tag_contents}"

def tag_list(server_tags:dict):
    return "\n".join(server_tags.keys())

@bot.command()
async def tag(ctx,command:str,*,data:str = None):
    tags = tag_files_read(ctx.guild.id)
    if command == "create":
        tag_return = tag_create(data,tags)
        await ctx.send(tag_return)
        return
    if command == "random":
        rand_str = tag_random(tags)
        await ctx.send(rand_str)
        return
    if command == "list":
        taglist = tag_list(tags)
        await ctx.send(taglist)
        return
    tag_return = tag_main(command,tags)
    await ctx.send(tag_return)


bot.run(TOKEN)