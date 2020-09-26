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
from multiprocessing import Process, Queue
#from YouPy.youtube_item import YouTubeItem

BOT_TOKEN = "NzQ2MDA0Mjg3NTIzNjUxNzQ0.Xz6Aog.EKEz3onTr8TP-jg3k6klsA4DqZE"
key = ""
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
play_message_set = {}
thumbnail_message_set = {}
lyric_message_set = {}
status_set = {}
search_set = {}
vc_set = {}
player_set = {}
timer_set = {}


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
                          'Request_User_Name, '
                          'Thumbnail_Link) '
                          'values(?,?,?,?,?,?,?,?)'
                          , video_info_set)
        QUEUE_DB.commit()
    elif command == "DELETE":
        for i in video_info_set:
            QUEUE_SQL.execute(f'delete from Queues LIMIT 1 OFFSET {i-1}')
        QUEUE_DB.commit()

def Status_Update(server_id):
    guild = ctx.guild
    server_id = guild.id

def Parsing(content):
    if str(type(content)) == "<class 'int'>":
        return "{:02}:{:02}:{:02}".format(int((content // 60) // 60), int((content // 60) % 60), int(content % 60))
    elif str(type(content)) == "<class 'float'>":
        content = int(content)
        return "{:02}:{:02}:{:02}".format(int((content // 60) // 60), int((content // 60) % 60), int(content % 60))
    else:
        data = list(map(int,content.split(':')))
        if len(data) == 3:
            timestamp = "{:02}:{:02}:{:02}".format(data[0], data[1], data[2])
        elif len(data) == 2:
            timestamp = "00:{:02}:{:02}".format(data[0], data[1])
        else:
            timestamp = "00:00:{:02}".format(data[0])
        return timestamp

def Un_Parsing(content):
    format_content = tuple(map(int, content.split(":")))
    return format_content[0] * 3600 + format_content[1] * 60 + format_content[2]

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
    voice_status = 0
    call_user_name = str(ctx.message.author)
    total_calls = 1
    language_code = ''
    repeat_value = 0
    audio_effect = 'Default'
    queue_page = 1
    playing_status = 'Stop'
    vc_set[str(server_id)] = get(bot.voice_clients, guild=guild)

    status_set[str(server_id)] = "Stop"

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
                      '"Request_User_Name" text, '
                      '"Thumbnail_Link" text'
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
    if str(server_id) in play_message_set.keys():
        await play_message_set[f'{server_id}'].delete()
        del play_message_set[f'{server_id}']
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
        temp_video_info = [(i['link'], i['title'], i['channel'], Parsing(i['duration']), i['thumbnails'][0]) for i in data]
        print(data)
        search_set[str(server_id)] = tuple(temp_video_info)
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
    method = "Play"
    value = "".join(args)
    if len(value) != 1:
        log_message += f'<{datetime.datetime.now()}> [{method}] Invalid arguments (len)' + "\n"
        await ctx.send('`You have to input for 1~5`')
    elif str(server_id) not in search_set.keys():
        log_message += f'<{datetime.datetime.now()}> [{method}] No search before playing' + "\n"
        await ctx.send('`You have to search before you choose music`')
    elif search_message_set[str(server_id)] != None:
        if value.isdigit() and 0 < int(value) < 6:
            data = search_set[str(server_id)][int(value)-1]
            yt = pytube.YouTube(data[0]).captions
            caption_value = "False" if len(yt.keys()) == 0 else "True"
            with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
                f.write(f'<{datetime.datetime.now()}> [{method}] Captions detected' + "\n")
            Queue_Update(server_id, server_name, "APPEND", (data[1],
                                                            data[2],
                                                            data[0],
                                                            caption_value,
                                                            data[3],
                                                            str(ctx.message.author),
                                                            ctx.message.author.name,
                                                            data[4]))
            await search_message_set[str(server_id)].delete()
            del search_message_set[str(server_id)]
            del search_set[str(server_id)]
            if status_set[str(server_id)] == "Stop":
                await ctx.send('`Now, start playing music`')
                await Playing(ctx)
                with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
                    f.write(f'<{datetime.datetime.now()}> [{method}] Player start' + "\n")
            else:
                log_message += f'<{datetime.datetime.now()}> [{method}] Change to method, Append' + "\n"
                await ctx.send('`YoutoBe already playing music. I\'ll just append to queue.`')
        else:
            log_message += f'<{datetime.datetime.now()}> [{method}] Invalid arguments (type)' + "\n"
            await ctx.send('`You have to input for 1~5`')

    with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
        f.write(log_message)


async def Playing(ctx):
    method = "Player"
    server = ctx.guild
    server_id = server.id
    server_name = str(server)
    vc = vc_set[str(server_id)]
    QUEUE_DB = sqlite3.connect(os.path.join(
        ORIGINAL_DIR, f"Servers/Queue_{server_id}_{server_name}.db"))
    QUEUE_SQL = QUEUE_DB.cursor()
    SERVER_SQL = SERVER_DB.cursor()
    Server_Update(server_id, {"Playing_Status": "Play"})
    status_set[str(server_id)] = "Play"
    while True:
        QUEUE_SQL.execute('select * from Queues LIMIT 1')
        queue_data = QUEUE_SQL.fetchall()
        SERVER_SQL.execute(f'select * from Servers where Server_ID={server_id}')
        server_data = SERVER_SQL.fetchall()
        repeat_value = server_data[0][9]
        sound_effect = server_data[0][10]
        if queue_data == []:
            log_message += f'<{datetime.datetime.now()}> [{method}] Player end' + "\n"
            print('break')
            break
        else:
            num, \
            song_title, \
            song_channel, \
            song_link, \
            song_lyric_value, \
            duration, \
            request_user_id, \
            request_user_name, \
            thumbnail_link = queue_data[0]

            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                              'options': '-vn'}

            lyric = "Loading..."

            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(song_link, download=False)
            URL = info['formats'][0]['url']
            vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

            with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
                f.write(f'<{datetime.datetime.now()}> [{method}] Player playing music [{song_title}] [{song_link}]' + "\n")

            timer_set[str(server_id)] = [datetime.datetime.now(), datetime.datetime.now(), -1, -1, Un_Parsing(duration), duration, -1, 0]
            timer_set[str(server_id)][-1] = (timer_set[str(server_id)][1] - timer_set[str(server_id)][0]).total_seconds()
            play_embed = discord.Embed(title=f"Playing status           [00:00:00 / {timer_set[str(server_id)][-3]}]",color=discord.Colour.blue())
            play_embed.add_field(name="| Music Title", value=f"`{song_title}`", inline=False)
            play_embed.add_field(name="| Repeat Value", value=f"`{repeat_value}`", inline=True)
            play_embed.add_field(name="| Sound Effect", value=f"`{sound_effect}`", inline=True)
            play_embed.add_field(name="| Status", value="`Play`", inline=True)
            play_embed.add_field(name="| Lyric", value=lyric, inline=False)
            play_message_set[str(server_id)] = await ctx.send(embed=play_embed)
            with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
                f.write(f'<{datetime.datetime.now()}> [{method}] Print play_status_embed' + "\n")
            lyric_groups = None
            if song_lyric_value == "True":
                yt = pytube.YouTube(song_link)
                caption = yt.captions.get_by_language_code('ko')
                if "(자동 생성됨)" in str(caption):
                    caption = None
                if caption == None:
                    caption = yt.captions.get_by_language_code('en')
                    if "(자동 생성됨)" in str(caption):
                        caption = None
                    if caption == None:
                        caption = yt.captions.all()[0]
                caption_language_value = caption.code
                lyric_groups = [(x.split('\n')[1].split(',')[0], x.split('\n')[2]) for x in caption.generate_srt_captions().split('\n\n')]
                start_caption_time = lyric_groups[0][0]
                lyrics_groups = [f'`< Intro >`\n** {lyric_groups[0][1]}**\n`{lyric_groups[1][1]}`'] + ["\n".join(("`" + lyric_groups[i][1] + "`", "** " + lyric_groups[i+1][1] + "**", "`" + lyric_groups[i+2][1] + "`")) for i in range(len(lyric_groups)-2)] + [f'`{lyric_groups[-2][1]}`\n** {lyric_groups[-1][1]}**\n`< End >`']
            lyric = "No Lyric"
            while timer_set[str(server_id)][-2] < timer_set[str(server_id)][-4]:
                start_time = datetime.datetime.now()
                if status_set[str(server_id)] == "Pause":
                    timer_set[str(server_id)][2] = datetime.datetime.now()
                    with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
                        f.write(f'<{datetime.datetime.now()}> [{method}] Detected method [Pause]' + "\n")
                    vc.pause()
                    while True:
                        SERVER_SQL.execute(f'select Playing_Status from Servers where Server_ID={server_id}')
                        await asyncio.sleep(0.7)
                        play_embed = discord.Embed(
                            title=f"Playing status           [{Parsing(timer_set[str(server_id)][-2])}/ {timer_set[str(server_id)][-3]}]",
                            color=discord.Colour.blue())
                        play_embed.add_field(name="| Music Title", value=f"`{song_title}`", inline=False)
                        play_embed.add_field(name="| Repeat Value", value=f"`{repeat_value}`", inline=True)
                        play_embed.add_field(name="| Sound Effect", value=f"`{sound_effect}`", inline=True)
                        play_embed.add_field(name="| Status", value="`Pause`", inline=True)
                        play_embed.add_field(name="| Lyric", value=lyric, inline=False)
                        await play_message_set[str(server_id)].edit(embed=play_embed)
                        if status_set[str(server_id)] == "Resume":
                            timer_set[str(server_id)][3] = datetime.datetime.now()
                            with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
                                f.write(f'<{datetime.datetime.now()}> [{method}] Detected method [Resume]' + "\n")
                            vc.resume()
                            break
                        if status_set[str(server_id)] == "Skip":
                            timer_set[str(server_id)][3] = datetime.datetime.now()
                            with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
                                f.write(f'<{datetime.datetime.now()}> [{method}] Detected method [Skip], Escaped pause loop' + "\n")
                            break
                        if status_set[str(server_id)] == "Stop":
                            timer_set[str(server_id)][3] = datetime.datetime.now()
                            with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
                                f.write(f'<{datetime.datetime.now()}> [{method}] Detected method [Stop], Escaped pause loop' + "\n")
                            break
                    timer_set[str(server_id)][-1] += (timer_set[str(server_id)][3] - timer_set[str(server_id)][2]).total_seconds()
                if status_set[str(server_id)] == "Skip":
                    status_set[str(server_id)] = "Play"
                    with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
                        f.write(f'<{datetime.datetime.now()}> [{method}] Detected method [Skip]' + "\n")
                    break
                if status_set[str(server_id)] == "Stop":
                    with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
                        f.write(f'<{datetime.datetime.now()}> [{method}] Detected method [Stop], Escaped playing loop' + "\n")
                    break
                timer_set[str(server_id)][1] = datetime.datetime.now()
                timer_set[str(server_id)][-2] = (timer_set[str(server_id)][1] - timer_set[str(server_id)][0]).total_seconds() - timer_set[str(server_id)][-1]
                if song_lyric_value == 'True':
                    for k in [k[0] for k in lyric_groups]:
                        if timer_set[str(server_id)][-2] < Un_Parsing(start_caption_time):
                            lyric = f'**< Lyric_language = {caption_language_value} >**\n**< Intro >**\n`{lyric_groups[0][1]}`'
                            break
                        elif timer_set[str(server_id)][-2] < Un_Parsing(lyric_groups[0][0]):
                            pass
                        else:
                            del lyric_groups[0]
                            lyric = lyrics_groups.pop(0)
                play_embed = discord.Embed(
                    title=f"Playing status           [{Parsing(timer_set[str(server_id)][-2])}/ {timer_set[str(server_id)][-3]}]",
                    color=discord.Colour.blue())
                play_embed.add_field(name="| Music Title", value=f"`{song_title}`", inline=False)
                play_embed.add_field(name="| Repeat Value", value=f"`{repeat_value}`", inline=True)
                play_embed.add_field(name="| Sound Effect", value=f"`{sound_effect}`", inline=True)
                play_embed.add_field(name="| Status", value="`Play`", inline=True)
                play_embed.add_field(name="| Lyric", value=lyric, inline=False)
                await play_message_set[str(server_id)].edit(embed=play_embed)
                await asyncio.sleep(0.7)
            await play_message_set[str(server_id)].delete()
            del play_message_set[str(server_id)]
            if status_set[str(server_id)] == "Stop":
                vc.stop()
                with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
                    f.write(f'<{datetime.datetime.now()}> [{method}] Detected method [Stop], Escaped queue loop' + "\n")
                break
            Queue_Update(server_id, server_name, "DELETE", [1])
            vc.stop()
    Server_Update(server_id, {"Playing_Status": "Stop"})


@bot.command()
async def 일시정지(ctx):
    method = "Pause"
    server = ctx.guild
    server_id = server.id
    server_name = str(server)
    status_set[str(server_id)] = "Pause"
    Server_Update(server_id, {"Playing_Status": "Pause"})
    with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
        f.write(f'<{datetime.datetime.now()}> [{method}]' + "\n")


@bot.command()
async def 계속(ctx):
    method = "Resume"
    server = ctx.guild
    server_id = server.id
    server_name = str(server)
    status_set[str(server_id)] = "Resume"
    Server_Update(server_id, {"Playing_Status": "Play"})
    with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
        f.write(f'<{datetime.datetime.now()}> [{method}]' + "\n")


@bot.command()
async def 스킵(ctx):
    method = "Skip"
    server = ctx.guild
    server_id = server.id
    server_name = str(server)
    status_set[str(server_id)] = "Skip"
    with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
        f.write(f'<{datetime.datetime.now()}> [{method}]' + "\n")

@bot.command()
async def 정지(ctx):
    method = "Stop"
    server = ctx.guild
    server_id = server.id
    server_name = str(server)
    status_set[str(server_id)] = "Stop"
    with open(os.path.join(ORIGINAL_DIR, f"Logs/Log_{server_id}_{server_name}.txt"), 'a') as f:
        f.write(f'<{datetime.datetime.now()}> [{method}]' + "\n")

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

