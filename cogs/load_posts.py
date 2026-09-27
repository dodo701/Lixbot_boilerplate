import discord
from discord import app_commands
from discord.ext import commands
import os
import aiohttp
from utils.jsonparser import parse_post_to_embed

class LoadPosts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_token = os.getenv("LIX_BOT_TOKEN")

    @app_commands.command(name="글확인", description="API에서 게시글을 불러옵니다.")
    @app_commands.describe(limit="불러올 게시글의 개수를 입력하세요 (기본값: 5, 최대: 100).")
    async def 글확인(self, interaction: discord.Interaction, limit: int = 5):
        # 응답 지연시키기 (API 통신 시간이 걸릴 수 있으므로)
        await interaction.response.defer()
        
        selected_limit = max(1, min(limit, 100))
        url = f"https://lixcampus.com/api/v1/lix-bot/posts?limit={selected_limit}"
        headers = {
            "Authorization": f"Bot {self.api_token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    await interaction.followup.send("게시글을 불러오는데 실패했습니다.", ephemeral=True)
                    return
                
                try:
                    data = await response.json()
                except Exception:
                    await interaction.followup.send("데이터를 파싱하는 중 오류가 발생했습니다.", ephemeral=True)
                    return
                
                posts = data.get("data", [])

        if not posts:
            await interaction.followup.send("게시글이 없습니다.", ephemeral=True)
            return

        embeds = [parse_post_to_embed(post) for post in posts]

        # 디스코드에는 한 번에 최대 10개의 임베드를 묶어서 보낼 수 있음
        for i in range(0, len(embeds), 10):
            chunk = embeds[i:i+10]
            await interaction.followup.send(embeds=chunk)

async def setup(bot):
    await bot.add_cog(LoadPosts(bot))
