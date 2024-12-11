import discord
from discord.ui import Select, Button, View, TextInput, Modal 

async def delete_message(ctx):
    await ctx.channel.purge(limit=1)  # 최신 메시지 하나 삭제

async def make_ticket(ctx, category_name: str):
    guild = ctx.guild
    category = discord.utils.get(guild.categories, name=category_name)
    if not category:
        category = await guild.create_category(category_name)
    
    # 채널 생성
    ticket_channel = await category.create_text_channel(f"🐤")
    
    # 권한 설정
    await ticket_channel.set_permissions(guild.default_role, read_messages=False)  # 기본 역할은 채널을 읽을 수 없음
    await ticket_channel.set_permissions(ctx.author, read_messages=True)  # 명령어 실행자만 채널을 읽을 수 있음

    # 채널 객체 리턴
    return ticket_channel

class DateRangeModal(Modal):
    def __init__(self):
        super().__init__(title="가입 기간 설정")

        # 시작일과 종료일을 받는 TextInput 필드 추가
        self.start_date = TextInput(
            label="시작일 (YYYY-MM-DD)",
            placeholder="예: 2023-01-01",
            required=True,
            max_length=10
        )
        self.end_date = TextInput(
            label="끝 날짜 (YYYY-MM-DD)",
            placeholder="예: 2023-12-31",
            required=True,
            max_length=10
        )

        # 폼에 필드 추가
        self.add_item(self.start_date)
        self.add_item(self.end_date)

    async def on_submit(self, interaction: discord.Interaction):
        # 사용자로부터 받은 날짜
        start_date = self.start_date.value
        end_date = self.end_date.value

        # 임베드 객체 생성
        embed = discord.Embed(
            title="가입기간 내 유저조회",
            description=f"시작일: {start_date}\n끝 날짜: {end_date}\n\n기간에 맞는 유저를 조회합니다.",
            color=discord.Color.blue()
        )

        # 메시지 업데이트
        await interaction.message.edit(content=None, embed=embed, view=None)

        # 확인 메시지 전송
        await interaction.response.send_message(f"시작일: {start_date}, 끝 날짜: {end_date} 기간에 대해 조회를 시작합니다!", ephemeral=True)

# 각 옵션별 실행 함수 정의
async def handle_user_query(interaction: discord.Interaction):
    # 임베드 객체 생성
    embed = discord.Embed(
        title="가입기간 내 유저조회",
        description="여기에서 가입 기간을 기반으로 유저를 조회할 수 있습니다.",
        color=discord.Color.blue()
    )

    # 임베드를 메시지에 설정
    modal = DateRangeModal()
    await interaction.response.send_modal(modal)
    await interaction.message.edit(content=None, embed=embed, view=None)

# async def handle_all_user_data(ctx):

# async def handle_single_user_data(ctx):

# async def handle_event_points(ctx):

# async def handle_announcement(ctx):

async def create_menu() -> View:
    # 선택된 값을 저장하기 위한 변수
    selected_value = []

    # 드롭다운 메뉴 생성
    select = Select(
        placeholder="메뉴를 선택해주세요.",
        options=[
            discord.SelectOption(label="| 가입기간 내 유저조회", description="입력한 가입기간 내 유저들의 정보", emoji="🔎"),
            discord.SelectOption(label="| 기간 내 전체 유저 데이터 조회", description="입력한 기간 내 유저들의 활동내역", emoji="📑"),
            discord.SelectOption(label="| 기간 내 단일 유저 데이터 조회", description="입력한 기간 내 유저 개인의 활동내역", emoji="🎥"),
            discord.SelectOption(label="| 이벤트 포인트 부여", description="유저들에게 이벤트 포인트 부여", emoji="💎"),
            discord.SelectOption(label="| 공지사항 추가 및 삭제", description="공지사항 추가 및 삭제", emoji="📢")
        ]
    )

    # 버튼 생성
    button = Button(label="확인", style=discord.ButtonStyle.primary)

    # 드롭다운 메뉴 선택 시 콜백 함수
    async def select_callback(interaction: discord.Interaction):
        nonlocal selected_value
        selected_value = [
            {
                'label': option.label,
                'description': option.description,
                'emoji': option.emoji
            }
            for option in select.options if option.label in select.values
        ][0]
        await interaction.response.defer()  # 상호작용 처리 완료

    # 버튼 클릭 시 콜백 함수
    async def button_callback(interaction: discord.Interaction):
        if not selected_value:
            await interaction.followup.send("아직 아무 것도 선택하지 않았습니다!", ephemeral=True, delete_after=3)
    
        # 선택된 값에 따라 함수 실행
        if selected_value['label'] == "| 가입기간 내 유저조회":
            await handle_user_query(interaction)
            await interaction.response.defer()
            

        # elif selected_value['label'] == "| 기간 내 전체 유저 데이터 조회":
        #     await handle_all_user_data(ctx)
        # elif selected_value['label'] == "| 기간 내 단일 유저 데이터 조회":
        #     await handle_single_user_data(ctx)
        # elif selected_value['label'] == "| 이벤트 포인트 부여":
        #     await handle_event_points(ctx)
        # elif selected_value['label'] == "| 공지사항 추가":
        #     await handle_announcement(ctx)

    # 콜백 함수 연결
    select.callback = select_callback
    button.callback = button_callback

    # View 생성 후 버튼과 드롭다운 추가
    view = View()
    view.add_item(select)
    view.add_item(button)

    return view

