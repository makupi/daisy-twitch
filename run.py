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
        await self.join_channels([ctx.channel.name])
        config.channels.append(ctx.channel.name)
        await ctx.send(f";join")

    @commands.command(name="leave")
    async def leave(self, ctx):
        await self.part_channels([ctx.channel.name])
        config.channels.remove(ctx.channel.name)
        await ctx.send(f";leave")


bot = Bot()
bot.add_cog(nookipedia.Nookipedia(bot))
bot.run()

with open("channels.json", "w") as channels_file:
    json.dump({"channels": list(dict.fromkeys(config.channels))}, channels_file)
