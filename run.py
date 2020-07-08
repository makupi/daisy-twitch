import json
from twitchio.ext import commands
from bot import config
from bot.cogs import nookipedia


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            irc_token=config.irc_token,
            api_token=config.api_token,
            nick=config.nick,
            prefix=config.prefix,
            initial_channels=config.channels,
        )

    async def event_ready(self):
        print(f"Ready | {self.nick}")

    async def event_message(self, message):
        await self.handle_commands(message)

    @commands.command(name="join")
    async def join(self, ctx):
        await self.join_channels([ctx.author.name])
        config.channels.append(ctx.author.name)
        await ctx.send(f"Joined {ctx.author.name}.")
        config.save_channels()

    @commands.command(name="leave")
    async def leave(self, ctx):
        await self.part_channels([ctx.author.name])
        config.channels.remove(ctx.author.name)
        await ctx.send(f"Left {ctx.author.name}.")
        config.save_channels()


bot = Bot()
bot.add_cog(nookipedia.Nookipedia(bot))
bot.run()


