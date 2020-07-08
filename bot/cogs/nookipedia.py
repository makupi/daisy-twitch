from twitchio.ext import commands
from nookipedia import Nookipedia as NookipediaAPI
from bot.config import nookipedia_key


def split_string_categories(string):
    if ")" not in string:
        return string
    split = string.split(")")
    for s in split:
        if "New Horizons" in s:
            s = s.split("(")
            return s[0]
    string.replace(")", "), ")



class Nookipedia:
    def __init__(self, bot):
        self.bot = bot
        self.api = NookipediaAPI(api_key=nookipedia_key, cached_api=True)
        # self.villagers = list()
        # self.critters = list()
        # self.personality_data = dict()

    # @commands.listener()
    # async def on_ready(self):
    #     self.villagers = await self.query_villager_list()
    #     self.critters = await self.query_critter_list()
    #     self.personality_data = await self.query_personalities()
    #     print(f"{type(self).__name__} Cog ready.")

    @commands.command()
    async def villager(self, ctx, *, name: str):
        """*Look up a villager by name*

        **Usage**: `{prefix}villager <name>`
        **Example**: `{prefix}villager marshal` """
        v = await self.api.get_villager(name)
        if not v:
            await ctx.send(f'Villager "{name}" not found.')
        else:
            message = f'Villager "{v.name}" | Species: {v.species} ' \
                      f'| Birthday: {v.birthday} | Personality: {v.personality}'
            await ctx.send(message)

    @commands.command(aliases=["bug", "fish"])
    async def critter(self, ctx, *, name: str):
        """*Look up a critter by name*

        **Usage**: `{prefix}critter <name>`
        **Example**: `{prefix}critter sea bass` """
        c = await self.api.get_critter(name)
        if not c:
            await ctx.send(f'Critter "{name}" not found.')
        else:
            message = f'Critter "{c.name}" Location: {c.location} ' \
                      f'| Rarity: {c.rarity} | Value: {split_string_categories(c.price)}'
            await ctx.send(message)

    @commands.command()
    async def personalities(self, ctx):
        """*Get a list of personalities*

        **Example**: `{prefix}personalities` """
        embed = await create_embed(title="Personalities")
        desc = ""
        for k in self.personality_data.keys():
            desc += f" - {k}\n"
        embed.description = desc
        await ctx.send(embed=embed)

    @commands.command()
    async def personality(self, ctx, name: str):
        """*Get all villagers with a certain personality*

        **Usage**: `{prefix}personality <name>`
        **Example**: `{prefix}personality jock` """
        name = name.capitalize()
        embed = await create_embed()
        if name not in self.personality_data:
            embed.description = f"Personality `{name}` not found."
            await ctx.send(embed=embed)
            return
        embed.title = f"{name} villagers"
        data = self.personality_data.get(name)
        counter = 0
        msg = "```"
        for name in data:
            msg += f"{name:^10}\t"
            counter += 1
            if counter == 4:
                msg += "\n"
                counter = 0
        msg += "```"

        embed.description = msg
        embed.set_footer(text="Powered by https://nookipedia.com/")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Nookipedia(bot))
