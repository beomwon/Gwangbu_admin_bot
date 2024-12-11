import utils
import discord
from discord.ext import commands
from discord.ui import Select, Button, View

# Embed 생성 함수 수정
def make_embed(menu: dict) -> discord.Embed:
    embed = discord.Embed(
        color=discord.Color.green()
    )
    embed.set_author(name=f"현재 선택된 모드: {menu['emoji']} {menu['label'].replace('|','')}", icon_url='https://cdn-icons-png.flaticon.com/512/6900/6900555.png')
    return embed

async def ui(message):
    ticket_channel = await utils.make_ticket(message, "🔐 ADMIN")

    # 선택된 값을 저장하기 위한 변수
    selected_value = []

    # 기본 임베드 생성
    embed = make_embed({'label': '-', 'description': '먼저 선택해주세요.', 'emoji': ''})

    # 드롭다운 메뉴 생성
    select = Select(
        placeholder="기능을 선택해주세요.",
        options=[
            discord.SelectOption(label="| 조회", description="기간별, 유저별로 조회가 가능합니다.", emoji="🔎"),
            discord.SelectOption(label="| 포인트", description="유저에게 포인트를 부여할 수 있습니다.", emoji="🪙"),
            discord.SelectOption(label="| 공지사항", description="공지사항을 추가할 수 있습니다.", emoji="📢"),
            discord.SelectOption(label="| 블랙리스트", description="블랙리스트를 추가하고 삭제할 수 있습니다.", emoji="🚫"),
        ]
    )
    # 버튼 생성
    button = Button(label="확인", style=discord.ButtonStyle.primary)

    # 드롭다운 메뉴 선택 시 콜백 함수
    async def select_callback(interaction: discord.Interaction):
        nonlocal selected_value  # 외부 변수 수정 가능하도록 선언
        selected_value = [
            {
                'label': option.label,
                'description': option.description,
                'emoji': option.emoji
            }
            for option in select.options if option.label in select.values
        ][0]

        # 선택에 따라 임베드 업데이트
        updated_embed = make_embed(selected_value)
        await message.edit(embed=updated_embed)
        await interaction.response.defer()  # 상호작용 처리 완료

    # 버튼 클릭 시 콜백 함수
    async def button_callback(interaction: discord.Interaction):
        if selected_value:
            summary = '\n'.join([f"{key}: {value}" for key, value in selected_value.items()])
            await interaction.response.send_message(f"선택된 메뉴:\n\n{summary}", ephemeral=True)
        else:
            await interaction.response.send_message("아직 아무 것도 선택하지 않았습니다!", ephemeral=True)

    # 콜백 함수 연결
    select.callback = select_callback
    button.callback = button_callback

    # View 생성 후 버튼과 드롭다운을 추가
    view = View()
    view.add_item(select)
    view.add_item(button)

    # 티켓 채널에 임베드 메시지와 버튼/드롭다운을 함께 보내기
    message = await ticket_channel.send(embed=embed, view=view)
