import settings, admin, utils
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.check
async def globally_check_admin(ctx):
    if "ᴀᴅᴍɪɴ" not in [role.name for role in ctx.author.roles]:
        await utils.delete_message(ctx)
        await ctx.send("이 명령어를 실행할 권한이 없습니다.", ephemeral=True, delete_after=5)
        return False
    
    if ctx.channel.category and ctx.channel.category.name != "🔐 ADMIN":
        await utils.delete_message(ctx)
        await ctx.send("이 명령어는 🔐 ADMIN 카테고리에서만 사용할 수 있습니다.", ephemeral=True, delete_after=5)
        return False
    
    return True

@bot.command()
async def 메뉴(ctx):
    await utils.delete_message(ctx)
    await ctx.send(view=await utils.create_menu())

if __name__ == "__main__":
    bot.run(settings.BOT_TOKEN)