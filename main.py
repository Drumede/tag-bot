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

def tags_file(serverid:int):
    file_path = Path.cwd() / "servers" / (str(serverid)+".json")
    if not file_path.exists():
        with open(file_path,"w") as file:
            file.write("{}")
    return file_path

def tag_files_read(serverid:int):
    path = Path.cwd() / "servers"
    if not path.exists():
        path.mkdir(parents=True,exist_ok=True)

    file_path = tags_file(serverid)
    tags_dict = {}
    with open(file_path,"r") as file:
        tags_dict = json.loads(file.read())
    return tags_dict

def tags_file_update(serverid:int,updated_tags:dict):
    file_path = tags_file(serverid)
    with open(file_path,"w") as file:
        file.write(json.dumps(updated_tags))

def tag_main(selected_tag:str,server_tags:dict):
    if selected_tag in server_tags.keys():
        return server_tags[selected_tag]
    else:
        return f"tag `{selected_tag}` does not exist"

def tag_create(data:str,server_tags:dict):
    if data == None:
        return "nothing specified"
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

def tag_remove(data:str,server_tags:dict):
    if data == None:
        return "no tag specified"
    cutoff = data.find(" ")
    if cutoff == -1:
        cutoff = len(data)
    selected_tag = data[:cutoff].strip()
    if not selected_tag in server_tags.keys():
        return f"tag `{selected_tag}` does not exist"
    server_tags.pop(selected_tag)
    return f"tag `{selected_tag}` removed"

@bot.command()
async def tag(ctx,command:str,*,data:str = None):
    tags = tag_files_read(ctx.guild.id)
    if command == None:
        await ctx.send("no tag specified")
    if command == "create":
        retstring = tag_create(data,tags)
        await ctx.send(retstring)
        tags_file_update(ctx.guild.id,tags)
        return
    if command == "random":
        retstring = tag_random(tags)
        await ctx.send(retstring)
        return
    if command == "list":
        taglist = tag_list(tags)
        await ctx.send(taglist)
        return
    if command == "remove":
        retstring = tag_remove(data,tags)
        await ctx.send(retstring)
        tags_file_update(ctx.guild.id,tags)
        return
    tag_return = tag_main(command,tags)
    await ctx.send(tag_return)


bot.run(TOKEN)