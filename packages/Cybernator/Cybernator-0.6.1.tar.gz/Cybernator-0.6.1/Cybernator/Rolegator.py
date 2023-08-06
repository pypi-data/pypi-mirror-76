import discord
import asyncio
from discord.ext import commands
from discord import utils


class Rolegator:
    def __init__(self, bot, **kwargs):
        self.bot = bot
        self.emoji_role = kwargs.get('emoji_role', dict)
        self.guild_id = kwargs.get('guild_id', int)
        self.guild_roles = kwargs.get('guild_roles', list)
        self.channel_id = kwargs.get('channel_id', int)
        self.message_id = kwargs.get('message_id', int)
        self.role_remove = kwargs.get('role_remove', False)
#        self.max_role = kwargs.get('max_role', int)
#        self.white_roles = kwargs.get('green_roles', list)

    async def on_member_join(self, member):
        if member.guild.id == self.guild_id:
            for i in self.guild_roles:
                role = utils.get(member.guild.roles, id=i)
                await member.add_roles(role)

    async def on_ready(self):
        message = await self.bot.get_channel(self.channel_id).fetch_message(self.message_id)
        for i in self.emoji_role:
            await message.add_reaction(i)

    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return False
        message = await self.bot.get_channel(self.channel_id).fetch_message(self.message_id)
        member = utils.get(message.guild.members, id=payload.user_id)
        await message.remove_reaction(payload.emoji, payload.member)
        if payload.message_id == self.message_id:
            try:
                role = utils.get(message.guild.roles, id=self.emoji_role[str(payload.emoji)])
                if self.role_remove is True:
                    if role in member.roles:
                        await member.remove_roles(role)
                else:
                    await member.add_roles(role)
            except KeyError as e:
                await message.remove_reaction(payload.emoji, payload.member)
            except Exception as e:
                print(repr(e))

    def start(self):
        self.bot.add_listener(self.on_raw_reaction_add, name='on_raw_reaction_add')
        self.bot.add_listener(self.on_ready, name='on_ready')
        self.bot.add_listener(self.on_member_join, name='on_member_join')