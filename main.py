import os
os.system("pip install discord.py==1.7.3")
os.system("pip install colorama")
os.system('cls' if os.name == 'nt' else 'clear')
 
import json,discord,re,asyncio
from colorama import Fore,Style,init
from discord.ext import commands

init(autoreset=True)

_prefix_="!"
TienThanh = commands.Bot(command_prefix=_prefix_, case_insensitive=True, self_bot=True, intents=discord.Intents.all())
TienThanh.remove_command("help")

running = True


async def refresh_console():
    await TienThanh.wait_until_ready()
    while not TienThanh.is_closed():
        os.system('cls' if os.name == 'nt' else 'clear')
        user = TienThanh.user
        guild_count = len(TienThanh.guilds)
        total_running = sum(1 for sess in acs.values() if sess['running'])
        total_done = sum(sess.get('count', 0) for sess in acs.values())

        menu = f"""
{Fore.LIGHTCYAN_EX}{Style.BRIGHT}╔═══════════════════════╗
{Fore.LIGHTCYAN_EX}{Style.BRIGHT}║       {Fore.LIGHTGREEN_EX}MENU USER{Fore.LIGHTCYAN_EX}       ║
{Fore.LIGHTCYAN_EX}{Style.BRIGHT}╚═══════════════════════╝
{Fore.LIGHTRED_EX}{Style.BRIGHT}>> Tên người dùng [ {Style.RESET_ALL}@{user.name}{Fore.LIGHTRED_EX}{Style.BRIGHT} ]
{Fore.LIGHTRED_EX}{Style.BRIGHT}>> ID [ {Style.RESET_ALL}{user.id}{Fore.LIGHTRED_EX}{Style.BRIGHT} ]
{Fore.LIGHTRED_EX}{Style.BRIGHT}>> Thời gian tạo tài khoản [ {Style.RESET_ALL}{user.created_at.strftime('%d/%m/%Y | %H:%M:%S')}{Fore.LIGHTRED_EX}{Style.BRIGHT} ]
{Fore.LIGHTRED_EX}{Style.BRIGHT}>> Prefix [ {Style.RESET_ALL}{_prefix_}{Fore.LIGHTRED_EX}{Style.BRIGHT} ]
{Fore.LIGHTRED_EX}{Style.BRIGHT}>> Có [ {Style.RESET_ALL}{guild_count}{Fore.LIGHTRED_EX}{Style.BRIGHT} ] máy chủ
{Fore.LIGHTRED_EX}{Style.BRIGHT}>> Đang chạy [ {Style.RESET_ALL}{total_running}{Fore.LIGHTRED_EX}{Style.BRIGHT} ] nhiệm vụ
{Fore.LIGHTRED_EX}{Style.BRIGHT}>> Đã làm [ {Style.RESET_ALL}{total_done}{Fore.LIGHTRED_EX}{Style.BRIGHT} ] nhiệm vụ
{Fore.LIGHTCYAN_EX}{Style.BRIGHT}═════════════════════════
"""
        print(menu)
        await asyncio.sleep(30)

@TienThanh.event
async def on_ready():
    user = TienThanh.user
    guild_count = len(TienThanh.guilds)
    menu = f"""
{Fore.LIGHTCYAN_EX}{Style.BRIGHT}╔═══════════════════════╗
{Fore.LIGHTCYAN_EX}{Style.BRIGHT}║       {Fore.LIGHTGREEN_EX}MENU USER{Fore.LIGHTCYAN_EX}       ║
{Fore.LIGHTCYAN_EX}{Style.BRIGHT}╚═══════════════════════╝
{Fore.LIGHTRED_EX}{Style.BRIGHT}>> Tên người dùng [ {Style.RESET_ALL}@{user.name}{Fore.LIGHTRED_EX}{Style.BRIGHT} ]
{Fore.LIGHTRED_EX}{Style.BRIGHT}>> ID [ {Style.RESET_ALL}{user.id}{Fore.LIGHTRED_EX}{Style.BRIGHT} ]
{Fore.LIGHTRED_EX}{Style.BRIGHT}>> Thời gian tạo tài khoản [ {Style.RESET_ALL}{user.created_at.strftime('%d/%m/%Y | %H:%M:%S')}{Fore.LIGHTRED_EX}{Style.BRIGHT} ]
{Fore.LIGHTRED_EX}{Style.BRIGHT}>> Prefix [ {Style.RESET_ALL}{_prefix_}{Fore.LIGHTRED_EX}{Style.BRIGHT} ]
{Fore.LIGHTRED_EX}{Style.BRIGHT}>> Có [ {Style.RESET_ALL}{guild_count}{Fore.LIGHTRED_EX}{Style.BRIGHT} ] máy chủ
{Fore.LIGHTCYAN_EX}{Style.BRIGHT}═════════════════════════
"""
    print(menu)

@TienThanh.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"⚠ Lệnh không tồn tại. Gõ {_prefix_}help để xem danh sách lệnh.")
    else:
        raise error

def conv(number: int) -> str:
    bold_digits = {
        '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒',
        '5': '𝟓', '6': '𝟔', '7': '𝟕', '8': '𝟖', '9': '𝟗'
    }
    return ''.join(bold_digits[c] for c in str(number))

@TienThanh.command()
async def help(ctx):
    _help = f"""
*Thông tin và cách sử dụng*

**Prefix:** {_prefix_}

**Lệnh:**
- {_prefix_}start <guild_id> <channel_id> → Bắt đầu tự động nối số
- {_prefix_}stop <số thứ tự>` → Dừng nhiệm vụ theo số thứ tự (xem số thứ tự bằng `status`)
- {_prefix_}stopall → Dừng toàn bộ nhiệm vụ
- {_prefix_}status → Xem trạng thái nhiệm vụ
- {_prefix_}play → Đặt trạng thái đang chơi

**Ví dụ sử dụng:**
- {_prefix_}start 1234567890 9876543210
- {_prefix_}stop 1
- {_prefix_}stopall
- {_prefix_}play kiz đẹp trai

### Được làm bởi TienThanh
"""
    await ctx.send(_help)

acs = {}  # auto count sessions

def e_num(text):
    cleaned = re.sub(r'<:\w+:(\d+)>', '', text)
    numbers = re.findall(r'\b\d+\b', cleaned)
    return int(numbers[-1]) if numbers else None

@TienThanh.command()
async def start(ctx, guild_id: int, channel_id: int):
    key = (guild_id, channel_id)

    if key in acs and acs[key]['running']:
        await ctx.send(f"⚠ Đã có một phiên đếm cho <#{channel_id}>")
        return

    guild = discord.utils.get(TienThanh.guilds, id=guild_id)
    if not guild:
        await ctx.send(f"⚠ Không tìm thấy server với ID **{guild_id}**")
        return

    channel = discord.utils.get(guild.channels, id=channel_id)
    if not isinstance(channel, discord.TextChannel):
        await ctx.send(f"⚠ Không tìm thấy kênh text với ID **{channel_id}** trong server **{guild_id}**")
        return

    session = {"running": True, "task": None, "count": 0}
    acs[key] = session
    asyncio.create_task(refresh_console()) 
    #await ctx.send(f"⚔️ Bắt đầu tự động nối số ở server {guild_id} | kênh <#{channel_id}>")
    await ctx.send(f"⚔️ <#{channel_id}>")
    async def count_loop():
        last_sent_number = 0
        last_author_id = None
        while session["running"]:
            try:
                last_number = 0
                async for msg in channel.history(limit=100):
                    number = e_num(msg.content)
                    if number:
                        last_number = number
                        last_author_id = msg.author.id
                        break

                if last_number == 0:
                    print(f"-> {Fore.LIGHTYELLOW_EX}{Style.BRIGHT}[{guild_id} | {channel_id}] ⚠ Không tìm thấy số nào từ người khác.")
                    await asyncio.sleep(5)
                    continue

                if last_author_id == TienThanh.user.id:
                    print(f"-> {Fore.LIGHTYELLOW_EX}{Style.BRIGHT}[{guild_id} | {channel_id}] ⏳ Đang chờ người khác nối tiếp sau số {Style.RESET_ALL}{last_number}")
                    await asyncio.sleep(10)
                    continue

                next_number=last_number+1
                #await channel.send(f"{next_number} → tớ là Kiz, hành trình đi tới đầu bảng (chat {conv(next_number +1)} đi)")
                #await channel.send(f"{next_number} → chat {conv(next_number +1)} đi bạn ở dưới 👇")
                await channel.send(str(next_number))
                print(f"-> {Fore.LIGHTGREEN_EX}{Style.BRIGHT}[{guild_id} | {channel_id}] 🔖 Đã gửi số: {Style.RESET_ALL}{next_number}")
                session['count']+=1
                await asyncio.sleep(30)
            except Exception as e:
                print(f"-> {Fore.LIGHTRED_EX}{Style.BRIGHT}Lỗi trong count_loop [{guild_id} | {channel_id}]: {Fore.LIGHTYELLOW_EX}{e}")
                await asyncio.sleep(5)

    session["task"] = asyncio.create_task(count_loop())

@TienThanh.command()
async def status(ctx):
    if not acs:
        await ctx.send("⚠ Không có phiên nào đang chạy.")
        return

    status_msg = "**📊 Các phiên đang hoạt động:**\n"
    for idx, ((guild_id, channel_id), sess) in enumerate(acs.items(), start=1):
        state = "🟢 hoạt động" if sess["running"] else "🔴 dừng"
        #status_msg += f"`{idx}` → **Guild:** `{guild_id}` | **Channel:** `{channel_id}` → {state}\n"
        status_msg += f"{idx} → **Nhiệm Vụ:** <#{channel_id}> → {state}\n"

    await ctx.send(status_msg)


@TienThanh.command()
async def stop(ctx, index: int):
    if not acs:
        await ctx.send("⚠ Không có phiên nào đang chạy.")
        return

    items = list(acs.items())
    if 1 <= index <= len(items):
        key, sess = items[index - 1]
        sess["running"] = False
        #await ctx.send(f"🛑 Đã dừng phiên `{index}` → Server `{key[0]}` | Kênh `{key[1]}`")
        await ctx.send(f"🛑 Đã dừng **{index}** → **Nhiệm Vụ:** <#{key[1]}>")
    else:
        await ctx.send("⚠ Số thứ tự không hợp lệ.")

@TienThanh.command()
async def stopall(ctx):
    count = 0
    for sess in acs.values():
        if sess["running"]:
            sess["running"] = False
            count += 1
    await ctx.send(f"🛑 Đã dừng toàn bộ **{count}** phiên auto count đang chạy.")

@TienThanh.command()
async def play(ctx, *, game_name: str = None):
    if not game_name:
        await ctx.send(f"⚠ Vui lòng nhập nội dung. Ví dụ: `{_prefix_}play kiz đẹp trai")
        return
    await TienThanh.change_presence(activity=discord.Game(name=game_name))
    await ctx.send(f"Đã set trạng thái **{game_name}**")
    
with open("config.json", "r") as config_file:
    config = json.load(config_file)

TienThanh.run(config["TOKEN"], bot=False)
