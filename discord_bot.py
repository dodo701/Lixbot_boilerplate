import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

class MyBot(commands.Bot):
    def __init__(self):
        # Intents 설정
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # cogs 폴더 안의 모든 모듈을 찾아서 확장으로 로드
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and not filename.startswith("__"):
                await self.load_extension(f"cogs.{filename[:-3]}")
        # 슬래시 명령어 동기화
        await self.tree.sync()

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})") # type: ignore
        print("------")

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("DISCORD_TOKEN이 .env 파일에 설정되지 않았습니다.")
    else:
        bot = MyBot()
        bot.run(DISCORD_TOKEN)

