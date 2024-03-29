import discord
from discord import Option
from dotenv import load_dotenv
import openai

openai.api_key = "Open AI API Key" # < WARNING do not share this key
TOKEN = "Discord Bot Key" # < WARNING do not share this key
load_dotenv()


bot = discord.Bot()
GUILD_IDS = [1123178363364847627]  # ← You server's IDs
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]


@bot.event
async def on_ready():
    print(f"Bot name:{bot.user} On ready!!")


@bot.slash_command(description="Says your name, or the name on the optinal input field", guild_ids=GUILD_IDS)
async def hello(
        ctx: discord.ApplicationContext,
        name: Option(str, required=False, description="Enter a name", )):
    if not name:
        name = ctx.author
    await ctx.respond(f"Hello！ {name} ！")


@bot.slash_command(description="Ask a question to openAI", guild_ids=GUILD_IDS)
async def ask(ctx: discord.ApplicationContext, prompt: Option(str, required=True, description="question", )):
    await ctx.response.defer()
    messages.append({"role": "user", "content": prompt})
    response = openai.chat.completions.create(

        model="gpt-3.5-turbo",# ← You can change the model as you wish
        # Additionally, you may also use a custom model you trained yourself
        messages=messages,
        temperature=0,
    )

    messages.append({"role": "system", "content": response.choices[0].message.content})
    await ctx.followup.send(response.choices[0].message.content)

bot.run(TOKEN)
