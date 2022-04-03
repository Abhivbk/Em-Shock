# GNU GENERAL PUBLIC LICENSE

# Version 3, 29 June 2007

# Copyright (C) 2021 AbHiK Inc.

# Author --> Abhinav Kulkarni
# Email --> abhivbk13@gmail.com

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from cogs import music

load_dotenv()

cogs = [music]
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)

client.run(os.getenv('TOKEN'))
