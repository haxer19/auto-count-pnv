import os
os.system("pip install discord.py==1.7.3")
os.system("pip install colorama")
os.system(
    "sleep 2 && clear >/dev/null 2>&1 &"
    if os.name == "posix"
    else "timeout /t 2 >nul 2>&1 && cls"
)
if os.name == 'nt': 
    os.system('cls')
else:  
    os.system('clear')

import json
from colorama import Fore, Style, init
import discord
from discord.ext import commands
import re,asyncio,random

_prefix_="!"
TienThanh = commands.Bot(command_prefix=_prefix_, case_insensitive=True, self_bot=True, intents=discord.Intents.all())
TienThanh.remove_command("help")

running = True

print(f"""{Fore.BLUE}

 █████╗ ██╗   ██╗████████╗ ██████╗      ██████╗ ██████╗ ██╗   ██╗███╗   ██╗████████╗
██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗    ██╔════╝██╔═══██╗██║   ██║████╗  ██║╚══██╔══╝
███████║██║   ██║   ██║   ██║   ██║    ██║     ██║   ██║██║   ██║██╔██╗ ██║   ██║   
██╔══██║██║   ██║   ██║   ██║   ██║    ██║     ██║   ██║██║   ██║██║╚██╗██║   ██║   
██║  ██║╚██████╔╝   ██║   ╚██████╔╝    ╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║   ██║   
╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝      ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝                                                                                                                                                        
{Style.RESET_ALL}""")

init(autoreset=True)

@TienThanh.event
async def on_ready():
    print(f"{Fore.LIGHTRED_EX} >Username:{Style.RESET_ALL}",f"{Fore.LIGHTGREEN_EX}{TienThanh.user}{Style.BRIGHT}{Style.RESET_ALL}\n")

def conv(number: int) -> str:
    bold_digits = {
        '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒',
        '5': '𝟓', '6': '𝟔', '7': '𝟕', '8': '𝟖', '9': '𝟗'
    }
    return ''.join(bold_digits[c] for c in str(number))

@TienThanh.command()
async def help(ctx):
    _help = f"""
**Auto Count** (Author: TienThanh)

**Prefix:** `{_prefix_}`

**Lệnh:**
- `{_prefix_}start <guild_id> <channel_id>` → Bắt đầu tự động nối số
- `{_prefix_}stop <số thứ tự>` → Dừng nhiệm vụ theo số thứ tự (xem số thứ tự bằng `status`)
- `{_prefix_}stopall` → Dừng toàn bộ nhiệm vụ
- `{_prefix_}status` → Xem trạng thái nhiệm vụ

**Ví dụ sử dụng:**
- `{_prefix_}start 1234567890 9876543210`
- `{_prefix_}stop 1`
- `{_prefix_}stopall`
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
        await ctx.send(f"⚠ Đã có một phiên đếm đang chạy cho server {guild_id} | kênh {channel_id}")
        return

    guild = discord.utils.get(TienThanh.guilds, id=guild_id)
    if not guild:
        await ctx.send(f"⚠ Không tìm thấy server với ID {guild_id}")
        return

    channel = discord.utils.get(guild.channels, id=channel_id)
    if not isinstance(channel, discord.TextChannel):
        await ctx.send(f"⚠ Không tìm thấy kênh text với ID {channel_id} trong server {guild_id}")
        return

    session = {"running": True, "task": None}
    acs[key] = session
    await ctx.send(f"⚔️ Bắt đầu tự động nối số ở server {guild_id} | kênh <#{channel_id}>")
    async def count_loop():
        while session["running"]:
            try:
                last_number = 0
                async for msg in channel.history(limit=100):
                    if msg.author.id == TienThanh.user.id:
                        continue
                    number = e_num(msg.content)
                    if number:
                        last_number = number
                        break

                if last_number == 0:
                    print(f"[{guild_id} | {channel_id}] ⚠ Không tìm thấy số nào từ người khác.")
                    await asyncio.sleep(5)
                    continue

                next_number=last_number+1
                #await channel.send(f"{next_number} → tớ là Kiz, hành trình đi tới đầu bảng (chat {next_number+1} đi)")
                #await channel.send(f"{next_number} → chat {conv(next_number +1)} đi bạn ở dưới 👇")
                await channel.send(str(next_number))
                print(f"[{guild_id} | {channel_id}] 🔖 Đã gửi số: {next_number}")
                await asyncio.sleep(30)
            except Exception as e:
                print(f"❗ Lỗi trong count_loop [{guild_id} | {channel_id}]: {e}")
                await asyncio.sleep(5)

    session["task"] = asyncio.create_task(count_loop())

@TienThanh.command()
async def status(ctx):
    if not acs:
        await ctx.send("⚠ Không có phiên auto count nào đang chạy.")
        return

    status_msg = "**📊 Các phiên auto count đang hoạt động:**\n"
    for idx, ((guild_id, channel_id), sess) in enumerate(acs.items(), start=1):
        state = "🟢 Đang chạy" if sess["running"] else "🔴 Đã dừng"
        status_msg += f"`{idx}` → **Guild:** `{guild_id}` | **Channel:** `{channel_id}` → {state}\n"

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
        await ctx.send(f"🛑 Đã dừng phiên `{index}` → Server `{key[0]}` | Kênh `{key[1]}`")
    else:
        await ctx.send("⚠ Số thứ tự không hợp lệ.")

@TienThanh.command()
async def stopall(ctx):
    count = 0
    for sess in acs.values():
        if sess["running"]:
            sess["running"] = False
            count += 1
    await ctx.send(f"🛑 Đã dừng toàn bộ `{count}` phiên auto count đang chạy.")

with open("config.json", "r") as config_file:
    config = json.load(config_file)

TienThanh.run(config["TOKEN"], bot=False)
