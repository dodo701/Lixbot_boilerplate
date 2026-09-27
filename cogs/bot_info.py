import discord
from discord import app_commands
from discord.ext import commands
import os
import aiohttp

class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_token = os.getenv("LIX_BOT_TOKEN")

    @app_commands.command(name="정보", description="현재 연동된 LIX 봇의 정보를 확인합니다.")
    async def 정보(self, interaction: discord.Interaction):
        # 응답을 지연시켜 API 통신 시간 확보
        await interaction.response.defer()
        
        url = "https://lixcampus.com/api/v1/lix-bot/me"
        headers = {
            "Authorization": f"Bot {self.api_token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    await interaction.followup.send("봇 정보를 불러오는데 실패했습니다.", ephemeral=True)
                    return
                
                try:
                    data = await response.json()
                except Exception:
                    await interaction.followup.send("데이터를 파싱하는 중 오류가 발생했습니다.", ephemeral=True)
                    return
                
                bot_info = data.get("bot", {})

        # 필요한 데이터 추출
        name = bot_info.get("name", "알 수 없음")
        description = bot_info.get("description", "설명 없음")
        enabled = bot_info.get("enabled", False)
        
        # 활성화 여부 텍스트 변환
        status_text = "🟢 활성화됨" if enabled else "🔴 비활성화됨"

        # 임베드 생성
        embed = discord.Embed(
            title=f"봇 정보: {name}",
            description=description,
            color=discord.Color.green() if enabled else discord.Color.red()
        )
        embed.add_field(name="활성화 여부", value=status_text, inline=False)
        
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BotInfo(bot))
