import discord
from datetime import datetime, timedelta

def parse_post_to_embed(post: dict) -> discord.Embed:
    """
    API 응답에서 받은 게시글(post) 딕셔너리 데이터를
    디스코드 Embed 객체로 변환하여 반환합니다.
    """
    title = post.get("title", "제목 없음")
    content = post.get("content", "내용 없음")
    
    # Embed description 길이는 4096자로 제한됨
    if len(content) > 4000:
        content = content[:4000] + "..."

    embed = discord.Embed(title=title, description=content, color=discord.Color.blue())
    
    # 우측 상단 이미지 (Thumbnail)
    image_url = post.get("imageUrl")
    if image_url and isinstance(image_url, str) and image_url.strip() != "" and image_url.strip().lower() != "null":
        image_url = image_url.strip()
        # 상대 경로인 경우 도메인 추가
        if not image_url.startswith(("http://", "https://")):
            if not image_url.startswith("/"):
                image_url = "/" + image_url
            image_url = "https://lixcampus.com" + image_url
        
        # 최종적으로 올바른 형태의 URL인지 확인
        if image_url.startswith(("http://", "https://")):
            embed.set_thumbnail(url=image_url)
    
    # KST 시간 변환
    # createdAt: '2026-09-25T05:06:09.145Z' 형식
    created_at_str = post.get("createdAt")
    if created_at_str:
        try:
            # 'Z'를 제거하고 파싱한 뒤 9시간을 더해 KST로 변환
            dt_utc = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
            dt_kst = dt_utc + timedelta(hours=9)
            time_str = dt_kst.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            time_str = created_at_str
    else:
        time_str = "알 수 없음"

    region = post.get("region", "알 수 없음")
    views = post.get("views", 0)

    footer_text = f"지역: {region} | 조회수: {views} | 작성일(KST): {time_str}"
    embed.set_footer(text=footer_text)
    
    return embed
