import asyncio
import requests
import datetime
import discord
import os
import json
import sqlite3
import requests
import pytube
from youtubesearchpython import SearchVideos
import youtube_dl
from pendulum.parsing import parse_iso8601
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Bot
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

BOT_TOKEN = "NzQ2MDA0Mjg3NTIzNjUxNzQ0.Xz6Aog.lxDlD-XjxIS9MzyOiamZRw4XpbQ"
key = "AIzaSyBvBYDJhGf6SNm9kADqw6U9Lsl-kGE7Wkk"
BOT_GAME = discord.Game('착취 당')
BOT_PREFIX = "//"
BOT_STATUS = discord.Status.online
bot = Bot(command_prefix=BOT_PREFIX, status=BOT_STATUS, activity=BOT_GAME)

ORIGINAL_DIR = os.getcwd()
SERVER_DB = sqlite3.connect(os.path.join(ORIGINAL_DIR, "Server_List.db"))
SERVER_SQL = SERVER_DB.cursor()

SERVER_SQL.execute('create table if not exists Servers('
                   '"Num" integer not null primary key autoincrement, '
                   '"Server_ID" integer, '
                   '"Server_Name" text, '
                   '"Channel_ID" integer, '
                   '"Channel_Name" text, '
                   '"Voice_Status" integer, '
                   '"Call_User_Name" text, '
                   '"Total_Calls" integer, '
                   '"Language_Code" text, '
                   '"Repeat_Value" integer, '
                   '"Audio_Effect" text, '
                   '"Queue_Page" text, '
                   '"Playing_Status" text'
                   ')')
SERVER_DB.commit()

queue_message_set = {}
search_message_set = {}
search_set = {}
vc_set = {}
player_set = {}

def Server_Update(server_id, value_set):
    global SERVER_SQL, SERVER_DB
    for name, value in value_set.items():
        SERVER_SQL.execute(f'UPDATE Servers SET {name} = ? WHERE Server_ID = ?',
                            (value, server_id))
    SERVER_DB.commit()

def Queue_Update(server_id, server_name, command, video_info_set):
    QUEUE_DB = sqlite3.connect(os.path.join(
        ORIGINAL_DIR, f"Servers/Queue_{server_id}_{server_name}.db"))
    QUEUE_SQL = QUEUE_DB.cursor()
    if command == "APPEND":
        QUEUE_SQL.execute(f'insert into Queues('
                          'Song_Title ,'
                          'Song_Channel, '
                          'Song_Link, '
                          'Song_Lyric_Value, '
                          'Duration, '
                          'Request_User_ID, '
                          'Request_User_Name) '
                          'values(?,?,?,?,?,?,?)'
                          , video_info_set)
        QUEUE_DB.commit()

def Parsing(content):
    data = list(map(int,content.split(':')))
    if len(data) == 3:
        timestamp = "{:02}:{:02}:{:02}".format(data[0], data[1], data[2])
    elif len(data) == 2:
        timestamp = "{:02}:{:02}".format(data[0], data[1])
    else:
        timestamp = "{:02}:{:02}".format(0, data[0])
    return timestamp


@bot.event
async def on_ready():
    print('Bot is on ready')


@bot.command()
async def 입장(ctx):
    method = "Join"
    log_message = ""
    guild = ctx.guild
    server_id = guild.id
    server_name = str(guild)
    channel = ctx.message.author.voice.channel
    channel_id = channel.id
    channel_name = str(channel)
    voice_status = 1
    call_user_name = str(ctx.message.author)
    total_calls = 1
    language_code = ''
    repeat_value = 0
    audio_effect = 'Default'
    queue_page = 1
    playing_status = 'Stop'
    vc_set[str(server_id)] = get(bot.voice_clients, guild=guild)

    SERVER_SQL.execute('SELECT * FROM Servers')
    for i in SERVER_SQL.fetchall():
        if server_id == i[1]:
            language_code = i[8]
            total_calls = i[7] + 1
    if language_code == '':
        language_code = 'en-US'

    SERVER_SQL.execute(f'SELECT Channel_ID FROM Servers WHERE Server_ID = {server_id}')
    if vc_set[str(server_id)] and vc_set[str(server_id)].is_connected():
        if SERVER_SQL.fetchone()[0] == channel_id:
            log_message += f'<{datetime.datetime.now()}> [{method}] This bot is already in {channel_name}' + "\n"
            await ctx.send(f'This bot is already in {channel_name}')
        else:
            await vc_set[str(server_id)].move_to(channel)
            log_message += f'<{datetime.datetime.now()}> [{method}] The bot has moved to {channel_name}' + "\n"
            await ctx.send(f'The bot has moved to {channel_name}')
    else:
        vc_set[str(server_id)] = await channel.connect()
        log_message += f'<{datetime.datetime.now()}> [{method}] The bot has connected to {channel_name}' + "\n"
        await ctx.send(f'The bot has connected to {channel_name}')

    server_info = (server_id,
                   server_name,
                   channel_id,
                   channel_name,
                   voice_status,
                   call_user_name,
                   total_calls,
                   language_code,
                   repeat_value,
                   audio_effect,
                   queue_page,
                   playing_status)
    SERVER_SQL.execute(f'delete from Servers where Server_ID = {server_id}')
    SERVER_SQL.execute('insert into Servers('
                       'Server_ID, '
                       'Server_Name, '
                       'Channel_ID, '
                       'Channel_Name, '
                       'Voice_Status, '
                       'Call_User_Name, '
                       'Total_Calls, '
                       'Language_Code, '
                       'Repeat_Value, '
                       'Audio_Effect, '
                       'Queue_Page, '
                       'Playing_Status) '
                       'values(?,?,?,?,?,?,?,?,?,?,?,?)', server_info)
    SERVER_DB.commit()
    QUEUE_DB = sqlite3.connect(os.path.join(
        ORIGINAL_DIR, f"Servers/Queue_{server_id}_{server_name}.db"))
    QUEUE_SQL = QUEUE_DB.cursor()
    QUEUE_SQL.execute('create table if not exists Queues('
                      '"Num" integer not null primary key, '
                      '"Song_Title" text, '
                      '"Song_Channel" text, '
                      '"Song_Link" text, '
                      '"Song_Lyric_Value" text, '
                      '"Duration" text, '
                      '"Request_User_ID" text, '
                      '"Request_User_Name" text'
                      ')')
    QUEUE_DB.commit()

    with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
        f.write(log_message)


@bot.command()
async def 퇴장(ctx):
    method = "Leave"
    log_message = ""
    guild = ctx.guild
    server_id = guild.id
    server_name = str(guild)
    channel = ctx.message.author.voice.channel
    channel_name = str(channel)
    vc_set[str(server_id)] = get(bot.voice_clients, guild=guild)

    if str(server_id) in queue_message_set.keys():
        await queue_message_set[f'{server_id}'].delete()
        del queue_message_set[f'{server_id}']
    if str(server_id) in search_message_set.keys():
        await search_message_set[f'{server_id}'].delete()
        del search_message_set[f'{server_id}']
    if vc_set[str(server_id)] and vc_set[str(server_id)].is_connected():
        await vc_set[str(server_id)].disconnect()
        del vc_set[str(server_id)]
        Server_Update(server_id, {"Voice_Status" : 0,
                                  "Playing_Status" : "Stop"})
        log_message += f'<{datetime.datetime.now()}> [{method}] The bot has disconnected to {channel_name} in {server_name}' + "\n"
        await ctx.send(f'The bot has disconnected to {channel_name}')
    else:
        log_message += f'<{datetime.datetime.now()}> [{method}] The bot is not in any voice channel in {server_name}' + "\n"
        await ctx.send(f'The bot is not in any voice channel')
    with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
        f.write(log_message)


@bot.command()
async def 큐(ctx, *args):
    method = "Queue"
    log_message = ""
    guild = ctx.guild
    server_id = guild.id
    server_name = str(guild)
    SERVER_SQL.execute(f"SELECT Queue_Page FROM Servers WHERE Server_ID = {server_id}")
    now_page = int(SERVER_SQL.fetchall()[0][0])
    QUEUE_DB = sqlite3.connect(os.path.join(
        ORIGINAL_DIR, f"Servers/Queue_{server_id}_{server_name}.db"))
    QUEUE_SQL = QUEUE_DB.cursor()
    QUEUE_SQL.execute('SELECT Song_Title FROM Queues')
    queue = QUEUE_SQL.fetchall()
    embed = None
    if queue == []:
        log_message += f'<{datetime.datetime.now()}> [{method}] Have no queue' + "\n"
        embed = discord.Embed(
            title="There is no music in Queue",
            color=0x00ff56
        )
    else:
        log_message += f'<{datetime.datetime.now()}> [{method}] Have queue' + "\n"
        str_num = ""
        str_songs = ""
        total_items = len(queue)
        total_pages = total_items // 10 + 1 if total_items % 10 != 0 else total_items // 10
        for i in range((now_page - 1) * 10, now_page * 10 if now_page != total_pages else (now_page - 1) * 10 + total_items % 10):
            str_num += str(i + 1) + "\n"
            song_name = queue[i][0][:32] + '...' if len(queue[i][0]) > 35 else queue[i][0]
            str_songs += song_name + "\n"
        embed = discord.Embed(
            title=f"Queue Page[{now_page}/{total_pages}]  Total: {total_items}",
            color=0x00ff56
        )
        embed.add_field(name="번호", value=str_num, inline=True)
        embed.add_field(name="제목", value=str_songs, inline=True)

    if not str(server_id) in queue_message_set.keys():
        log_message += f'<{datetime.datetime.now()}> [{method}] First message' + "\n"
    else:
        log_message += f'<{datetime.datetime.now()}> [{method}] After message' + "\n"
        queue_message_set[f"{server_id}"].delete()

    queue_message_set[f"{server_id}"] = await ctx.send(embed=embed)
    with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
        f.write(log_message)

@bot.command()
async def 검색(ctx, *args):
    global key
    server_id = ctx.guild.id
    server_name = str(ctx.guild)
    method = "Search"
    log_message = ""
    if "".join(args) != "":

        search = SearchVideos(" ".join(args), offset=1, mode="json", max_results=5)
        data = json.loads(search.result())['search_result']
        #form : id, title, channel
        temp_video_info = [(i['link'], i['title'], i['channel'], Parsing(i['duration'])) for i in data]
        search_set[str(server_id)] = tuple(temp_video_info)
        print(search_set[str(server_id)])

        message = ""
        for i in range(5):
            message += "**" +str(i+1) + "번 : ( " + search_set[str(server_id)][i][3] + " )** `" + search_set[str(server_id)][i][1] + "` \n"
        if str(server_id) in search_message_set.keys():
            await search_message_set[str(server_id)].delete()
            log_message += f'<{datetime.datetime.now()}> [{method}] After message' + "\n"
        else:
            log_message += f'<{datetime.datetime.now()}> [{method}] First message' + "\n"
        search_message_set[str(server_id)] = await ctx.send(message)
        log_message += f'<{datetime.datetime.now()}> [{method}] Searched [{" ".join(args)}]' + "\n"

    else:
        log_message += f'<{datetime.datetime.now()}> [{method}] There is no searching words' + "\n"
        if str(server_id) in search_message_set.keys():
            await search_message_set[str(server_id)].delete()
            log_message += f'<{datetime.datetime.now()}> [{method}] After message' + "\n"
        else:
            log_message += f'<{datetime.datetime.now()}> [{method}] After message' + "\n"
        search_message_set[str(server_id)] = await ctx.send("`There is no word to search`")
    with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
        f.write(log_message)

@bot.command()
async def 재생(ctx, *args):
    server_id = ctx.guild.id
    server_name = str(ctx.guild)
    log_message = ""
    value = "".join(args)
    if value == "":
        pass
    elif search_message_set[str(server_id)] != None:
        if value.isdigit() and 0 < int(value) < 6:
            data = search_set[str(server_id)][int(value)-1]
            yt = pytube.YouTube(data[0]).captions.all()
            caption_value = "False" if yt == None else "True"
            Queue_Update(server_id, server_name, "APPEND", (data[1],
                                                            data[2],
                                                            data[0],
                                                            caption_value,
                                                            data[3],
                                                            str(ctx.message.author),
                                                            ctx.message.author.name))
        await Playing(ctx)

async def Playing(ctx):
    server = ctx.guild
    server_id = server.id
    server_name = str(server)
    vc = vc_set[str(server_id)]
    QUEUE_DB = sqlite3.connect(os.path.join(
        ORIGINAL_DIR, f"Servers/Queue_{server_id}_{server_name}.db"))
    QUEUE_SQL = QUEUE_DB.cursor()
    SERVER_SQL = SERVER_DB.cursor()
    while True:
        QUEUE_SQL.execute('select * from Queues LIMIT 1')
        queue_data = QUEUE_SQL.fetchall()
        SERVER_SQL.execute(f'select * from Servers where Server_ID={server_id}')
        server_data = SERVER_SQL.fetchall()
        repeat_value = server_data[0][9]
        sound_effect = server_data[0][10]
        if queue_data == []:
            break
        else:

            num, \
            song_title, \
            song_channel, \
            song_link, \
            song_lyric_value, \
            duration, \
            request_user_id, \
            request_user_name = queue_data[0]

            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                              'options': '-vn'}

            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(song_link, download=False)
            URL = info['formats'][0]['url']
            vc_set[str(server_id)].play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            while vc_set[str(server_id)].is_playing:


@bot.command()
async def 테스트(ctx):
    await 입장(ctx)
    await 검색(ctx, "망상감상대상연맹")
    await 재생(ctx, "1")


@bot.event
async def on_error(ctx, error):
    guild = ctx.guild
    server_id = guild.id
    server_name = str(guild)
    log_message = ""
    method = "on_error"
    log_message += f'<{datetime.datetime.now()}> [{method}] {error}' + "\n"
    with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
        f.write(log_message)

@bot.event
async def on_command_error(ctx, error):
    guild = ctx.guild
    server_id = guild.id
    server_name = str(guild)
    log_message = ""
    method = "on_command_error"
    log_message += f'<{datetime.datetime.now()}> [{method}] {error}' + "\n"
    with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
        f.write(log_message)


bot.run(BOT_TOKEN)

