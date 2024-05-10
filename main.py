import discord
from discord.ext import commands

TOKEN = 'OTU2MDExMzY4OTkyMDg4MDg0.GEqtmi.pTOKaC5Wl7gm3NAhLw76I3CrPLDQ54WDRHQk5A'

bot = commands.Bot(command_prefix='?', intents=discord.Intents.all())

message_counts = {}
invite_counts = {}
ROLES = {}
BLACKLISTED_CHANNELS = []

@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id in BLACKLISTED_CHANNELS:
        return

    for role_name, role_id in ROLES.items():
        if discord.utils.get(message.author.roles, id=int(role_id)):
            message_counts[role_id] = message_counts.get(role_id, 0) + 1

    await bot.process_commands(message)

@bot.event
async def on_invite_create(invite):
    for role_name, role_id in ROLES.items():
        if invite.inviter and discord.utils.get(invite.inviter.roles, id=int(role_id)):
            invite_counts[role_id] = invite_counts.get(role_id, 0) + 1

@bot.command()
async def reset(ctx):
    message_counts.clear()
    embed = discord.Embed(title="Reset Messages", description="Message counts have been reset.", color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command()
async def m(ctx, role_name):
    role_id = ROLES.get(role_name)
    if role_id:
        count = message_counts.get(role_id, 0)
        embed = discord.Embed(title="Message Count", description=f'The role "{role_name}" has sent {count} messages.', color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error", description="Role not found.", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command()
async def add(ctx, role_name: str, role_mention: discord.Role):
    role_id = role_mention.id
    ROLES[role_name] = role_id
    embed = discord.Embed(title="Add Role", description=f'Role "{role_name}" with ID {role_id} added for tracking.', color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command()
async def bl(ctx, channel_id: int):
    try:
        if channel_id not in BLACKLISTED_CHANNELS:
            BLACKLISTED_CHANNELS.append(channel_id)
            embed = discord.Embed(title="Blacklist Channel", description=f'Channel with ID {channel_id} has been blacklisted.', color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Error", description="Channel is already blacklisted.", color=discord.Color.red())
            await ctx.send(embed=embed)
    except commands.BadArgument:
        embed = discord.Embed(title="Error", description="Invalid channel ID. Please provide a valid integer representing the channel ID.", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command()
async def ubl(ctx, channel_id: int):
    if channel_id in BLACKLISTED_CHANNELS:
        BLACKLISTED_CHANNELS.remove(channel_id)
        embed = discord.Embed(title="Unblacklist Channel", description=f'Channel with ID {channel_id} has been unblacklisted.', color=discord.Color.green())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error", description="Channel is not blacklisted.", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command()
async def rr(ctx, role_name: str):
    if role_name in ROLES:
        del ROLES[role_name]
        embed = discord.Embed(title="Remove Role", description=f'Role "{role_name}" removed from tracking.', color=discord.Color.green())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error", description="Role not found.", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command()
async def list(ctx):
    embed = discord.Embed(title="Tracking Information", color=discord.Color.blue())

    if ROLES:
        roles_text = ""
        for role_name, role_id in ROLES.items():
            role = ctx.guild.get_role(role_id)
            if role:
                roles_text += f"{role.mention} - {role_id}\n"
            else:
                roles_text += f"{role_name} - {role_id}\n"
        embed.add_field(name="Tracked Roles", value=roles_text, inline=False)
    else:
        embed.add_field(name="Tracked Roles", value="No roles are being tracked.", inline=False)

    if BLACKLISTED_CHANNELS:
        channels_text = ""
        for channel_id in BLACKLISTED_CHANNELS:
            channel = ctx.guild.get_channel(channel_id)
            if channel:
                channels_text += f"{channel.mention} - {channel_id}\n"
            else:
                channels_text += f"Channel ID: {channel_id}\n"
        embed.add_field(name="Blacklisted Channels", value=channels_text, inline=False)
    else:
        embed.add_field(name="Blacklisted Channels", value="No channels are blacklisted.", inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def bot_help(ctx):
    embed = discord.Embed(title="Bot Commands", color=discord.Color.blue())

    embed.add_field(name="?reset", value="Reset message counts.", inline=False)
    embed.add_field(name="?m <role_name>", value="Check message count for a specific role.", inline=False)
    embed.add_field(name="?add <role_name> <role_id>", value="Add a role for tracking.", inline=False)
    embed.add_field(name="?bl <channel_id>", value="Blacklist a channel.", inline=False)
    embed.add_field(name="?ubl <channel_id>", value="Unblacklist a channel.", inline=False)
    embed.add_field(name="?rr <role_name>", value="Remove a role from tracking.", inline=False)
    embed.add_field(name="?list", value="List tracking information.", inline=False)

    await ctx.send(embed=embed)

bot.run(TOKEN)import discord
from discord.ext import commands

# Discord bot token
TOKEN = 'OTg1NTY3MDQ1NTE1MDg3OTAy.GyLWj9.wiigsSjyWc5OeatIURuiWvwNdU-p_opUuoXHdE'

# Create a bot instance with a command prefix
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Dictionary to store message counts of members for each role
message_counts = {}

# Dictionary to store invite counts of members for each role
invite_counts = {}

# Dictionary to store the role IDs you want to track
ROLES = {}

# List of channel IDs to exclude from tracking
BLACKLISTED_CHANNELS = []

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    print('Bot is ready.')

# Event triggered when a message is sent
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Check if the message is in a blacklisted channel
    if message.channel.id in BLACKLISTED_CHANNELS:
        return

    # Check if the message sender has any of the specified roles
    for role_name, role_id in ROLES.items():
        if discord.utils.get(message.author.roles, id=int(role_id)):
            # Increment message count for the message sender
            message_counts[role_id] = message_counts.get(role_id, 0) + 1

    await bot.process_commands(message)

# Event triggered when an invite is created
@bot.event
async def on_invite_create(invite):
    for role_name, role_id in ROLES.items():
        if invite.inviter and discord.utils.get(invite.inviter.roles, id=int(role_id)):
            invite_counts[role_id] = invite_counts.get(role_id, 0) + 1

# Command to reset message counts
@bot.command()
async def reset_messages(ctx):
    message_counts.clear()
    await ctx.send('Message counts have been reset.')

# Command to get message count of a member for a specific role
@bot.command()
async def message_count(ctx, role_name):
    role_id = ROLES.get(role_name)
    if role_id:
        count = message_counts.get(role_id, 0)
        await ctx.send(f'The role "{role_name}" has sent {count} messages.')
    else:
        await ctx.send('Role not found.')

# Command to add a role to track
@bot.command()
async def add_role(ctx, role_name: str, role_id: int):
    if role_name and role_id:
        ROLES[role_name] = role_id
        await ctx.send(f'Role "{role_name}" with ID {role_id} added for tracking.')
    else:
        await ctx.send('Please provide both role name and role ID.')

# Command to blacklist a channel
@bot.command()
async def bl(ctx, channel_id: int):
    try:
        if channel_id not in BLACKLISTED_CHANNELS:
            BLACKLISTED_CHANNELS.append(channel_id)
            await ctx.send(f'Channel with ID {channel_id} has been blacklisted.')
        else:
            await ctx.send('Channel is already blacklisted.')
    except commands.BadArgument:
        await ctx.send('Invalid channel ID. Please provide a valid integer representing the channel ID.')

# Command to unblacklist a channel
@bot.command()
async def ubl(ctx, channel_id: int):
    if channel_id in BLACKLISTED_CHANNELS:
        BLACKLISTED_CHANNELS.remove(channel_id)
        await ctx.send(f'Channel with ID {channel_id} has been unblacklisted.')
    else:
        await ctx.send('Channel is not blacklisted.')

# Command to remove a role from tracking
@bot.command()
async def rr(ctx, role_name: str):
    if role_name in ROLES:
        del ROLES[role_name]
        await ctx.send(f'Role "{role_name}" removed from tracking.')
    else:
        await ctx.send('Role not found.')

# Command to list tracked roles and blacklisted channels
@bot.command()
async def mtl(ctx):
    embed = discord.Embed(title="Tracking Information", color=discord.Color.blue())

    if ROLES:
        roles_text = ""
        for role_name, role_id in ROLES.items():
            role = ctx.guild.get_role(role_id)
            if role:
                roles_text += f"{role.mention} - {role_id}\n"
            else:
                roles_text += f"{role_name} - {role_id}\n"
        embed.add_field(name="Tracked Roles", value=roles_text, inline=False)
    else:
        embed.add_field(name="Tracked Roles", value="No roles are being tracked.", inline=False)

    if BLACKLISTED_CHANNELS:
        channels_text = ""
        for channel_id in BLACKLISTED_CHANNELS:
            channel = ctx.guild.get_channel(channel_id)
            if channel:
                channels_text += f"{channel.mention} - {channel_id}\n"
            else:
                channels_text += f"Channel ID: {channel_id}\n"
        embed.add_field(name="Blacklisted Channels", value=channels_text, inline=False)
    else:
        embed.add_field(name="Blacklisted Channels", value="No channels are blacklisted.", inline=False)

    await ctx.send(embed=embed)

# Run the bot
bot.run(TOKEN)
