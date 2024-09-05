import discord
from discord.ext import commands
from transformers import AutoModel, AutoTokenizer
import os
import requests

model = AutoModel.from_pretrained('MiniCPM-V-2_6-int4', trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained('MiniCPM-V-2_6-int4', trust_remote_code=True)
model.eval()
# 替换为你的 Bot Token
DISCORD_TOKEN = 'XXX'

# 配置 Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# 创建 Bot 对象
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
msgs=[]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.event
async def on_message(message):
    # 避免 Bot 回复自己
    if message.author == bot.user:
        return

    # 处理 AI 回复
    if message.content.startswith('!ask'):
        query = message.content[len('!ask '):]  # 提取问题部分
        msgs.append({"role": "user", "content":query})
        response = await get_ai_response(msgs)
        msgs.append({"role": "assistant", "content": response})
        await message.channel.send(response)

    # 处理命令
    await bot.process_commands(message)

async def get_ai_response(query):
    try:
        res = model.chat(
            image=None,
            msgs=query,
            tokenizer=tokenizer
        )
        return res
    except Exception as e:
        return f"出错了: {e}"

@bot.command()
async def chat(ctx):
    if ctx.author == bot.user:
        return

    # 处理 AI 回复
    if ctx.message.content.startswith('!chat'):
        query = ctx.message.content[len('!chat '):]  # 提取问题部分
        msgs.append({"role": "user", "content":query})
        response = await get_ai_response(msgs)
        msgs.append({"role": "assistant", "content": response})
        await transform(response)

        # 发送预录音频文件到文本频道
        audio_file = "res/response.wav"
        if os.path.exists(audio_file):
            with open(audio_file, "rb") as audio:
                await ctx.send(file=discord.File(audio, audio_file))
        else:
            await ctx.send("我XX(此处已被屏蔽处理)")
    # 处理命令
    # await bot.process_commands(ctx.message)


@bot.command()
async def fudu(ctx):
    if ctx.author == bot.user:
        return

    # 处理 AI 回复
    if ctx.message.content.startswith('!fudu'):
        query = ctx.message.content[len('!fudu '):]  # 提取问题部分
        await transform(query)

        # 发送预录音频文件到文本频道
        audio_file = "res/response.wav"
        if os.path.exists(audio_file):
            with open(audio_file, "rb") as audio:
                await ctx.send(file=discord.File(audio, audio_file))
        else:
            await ctx.send("我XX(此处已被屏蔽处理)")
    # 处理命令


async def transform(query):
    data={
        "rever_wav_path":"prompt/1.wav",
        "prompt_text":"攻撃魔術,治癒魔術,召喚魔術,それぞれ初級",
        "prompt_language":"ja",
        "text":query,
        "text_language":"zh"
    }
    res=requests.post("http://127.0.0.1:9880",json=data)
    with open("res/response.wav","wb") as f:
        f.write(res.content)
# 运行 Bot
bot.run(DISCORD_TOKEN)
