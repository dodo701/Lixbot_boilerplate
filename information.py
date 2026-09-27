import json


def embed(title, description, color="#5865F2"):
    #LIX Bot 채널에 표시할 카드 데이터를 만듭니다.
    return {
        "type": "embed",
        "title": title,
        "description": description,
        "color": color,
    }


def command(message):
    #/도움말 또는 /규칙 명령을 처리합니다.
    message = message.strip()

    if message == "/도움말":
        return embed("LIX 안내봇 도움말", "/도움말 - 명령어 보기\n/규칙 - 커뮤니티 규칙 보기")

    if message == "/규칙":
        return embed("커뮤니티 규칙", "개인정보를 올리지 말고, 광고·사기성 홍보를 하지 마세요.", "#2F9E44")

    return embed("알 수 없는 명령어", "`/도움말`을 입력해 보세요.", "#E5484D")


print("LIX 안내봇 테스트 — /도움말 또는 /규칙 입력, 종료: exit")
while True:
    user_message = input("> ")
    if user_message == "exit":
        break
    print(json.dumps(command(user_message), ensure_ascii=False, indent=2)) 