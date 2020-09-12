import asyncio
import discord
import random
import datetime
import urllib
import time
import support2
import os
import subprocess
import pytube
import shutil
import re
from pytube import Playlist
from wcwidth import wcswidth
from mutagen.mp3 import MP3
from discord.ext import commands
from selenium import webdriver
from bs4 import BeautifulSoup
from YouPy.youtube_item import YouTubeItem

"""Accounts
ID: TubeDiscordDown1
PW: TDD@TDD1
"""

cookie = 'YSC=iGSgDWVhbcY; GPS=1; VISITOR_INFO1_LIVE=FFFSv19insU; HSID=AnJxAZZJAjp76_5Li; SSID=AA3KGJYbP_X5uoRCd; APISID=7ZmAWiaP4ZNR3tSI/AO8vdqe09wIyZLR8i; SAPISID=Ie10uXQyjwU-IaRO/ALHmwchdAwFvnBCUZ; __Secure-3PAPISID=Ie10uXQyjwU-IaRO/ALHmwchdAwFvnBCUZ; YTSESSION-1titawv=413f9b3c6cfe544c629153f14f4efa67c2MAAABBTmJxSk5tN1Y3OG92aG1SUlh5TDdpX1czeEdFdzZSN19WRXdzMmV1MGZ6a043V0Y2QzZxdm45UHoxSC00MFpxaENZVHpBRURqMjRlQzkwMzM2dERFUlFRbWE3QzVzM3NmZHM=; SID=0we97sEkPIf9Q_koJ6dEWo90pfx5eKrLxrk5JH0514_4ee3Zl7e5aewHZHw1RBblrIsfjQ.; __Secure-3PSID=0we97sEkPIf9Q_koJ6dEWo90pfx5eKrLxrk5JH0514_4ee3Z-I4JSWW1EoybevODP5dmGA.; LOGIN_INFO=AFmmF2swRQIhAL44yYdoxjQIV7XkhcJsVEhqvAJW1bMuQigBT2CbU2UYAiAZRWFiexEP7qlEnt6w0XN9Pz1cLnub_bu4y1FaNIuGog:QUQ3MjNmeF95OHZYUXNabm1RUW9GZ0hEOVVja1BXRF90V2Q1OWNuQjBXWEdUdU9rRkFTZWRla29pZDJ3X2JuQnFVakRlUk52bUhlUTNOMVlBekpPNHdvd0VjT2stQXlNV241WmZoWXJsT2xsdGQ3SVJiRU1mNV85elpDT1p5QUlvSXAtekN5bnJXVElYWVBZQkgybFYzR3NNQ3lTbjdkbEtGLXFFVzNjdDB1c2NvRE0teDloSlNj; SIDCC=AJi4QfGAZjPvUWJz-a93SGCZEX6eVJL9PniOLQkt0Z9rhsGtXa4a4Rx2WdnS01_LQy9z2j90; __Secure-3PSIDCC=AJi4QfEYoRhiUyRrp2DOR_sd08ieo5n9CM4kNer-0q6Mk8TaTawV3ixbQRPLm1oyPM_lAlkY3A'

token = "NzQ2MDA0Mjg3NTIzNjUxNzQ0.Xz6Aog.WRMKU4a3PcLYwHCabobM5itI07k"
PATH = 'E:/mp3 폴더/전체/'
Client_id = 746004287523651744
game = discord.Game('착취 당')
bot = commands.Bot(command_prefix='//', status= discord.Status.online, activity= game)
skip_value = 0
repeat_value = 0
one_repeat_value = 0
list_value = 0
status_value = False
volume_ = 0.5
now_page=1
queue_now_page = 1
queue_total_page = 1
value='가수'
search_value = 0
lists = []
first_stat_value = 0
now_index = 0
play_value = 0
content_value = '전체'
search_list = []
fail_list = []
eq_value = '기본'

link_data = ''

title_list = []
url_list = []
len_= 5
num = 1
t_list = ''

ctx_global = None

msg_youtube = None
msg_queue = None
msg_book = None

Play_status_massage = '재생 중'

url_select_num = "1번\n2번\n3번\n4번\n5번"

if not 'chromedriver.exe' in os.listdir('.'):
    support2.Get_driver()
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("disable-gpu")
driver = webdriver.Chrome(chrome_options=options)
site_url = 'https://www.youtube.com'

async def play_list(ctx, vc, channel):
    global skip_value, repeat_value, status_value, volume_, PATH, queue, first_stat_value, now_index, play_value, repeat_value, one_repeat_value, Voice_detected_value, Voice_command_value, Play_status_massage, msg
    with open('C:/Users/bomou/OneDrive/문서/Discord/mp3 player bot/Voice_command_data.txt','w') as f:
        f.write('')
    print('play_list run')
    rep_while_value = 1
    now=''
    sec_O = min_O = hour_O = 0
    pause_value = 0
    msg = 0
    play_value = 1
    now_index = 0
    for i in queue:
        now_index += 1
        if i =='Dump':
            vc.stop()
            await ctx.send('모든 리스트가 재생되었습니다.')
            play_value = 0
            break
        now=i.split('/')[-1]
        audio = MP3(f'{i}')
        length = int(audio.info.length)
        sec_O, min_O, hour_O = length%60, (length//60)%60, (length//60)//60
        options_ = None
        eq_value_in = ''
        if eq_value == '기본':
            options_ = None
            eq_value_in = '기본'
        elif eq_value == '에코':
            options_ = '-af aecho=0.9:0.88:60:0.4'
            eq_value_in = '에코'
        else:
            options_ == None
            eq_value_in = '기본'
        vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=f"{i}", options=options_))
        vc.source = discord.PCMVolumeTransformer(vc.source, volume=volume_)
        print(volume_)
        vc.source.volume = volume_
        print('Endpoint')
        print(f'Now progress_{now}')
        pause_time = 0
        total_pause = 0
        sec_ = min_ = hour_ = 0
        print_time = '00:00:00'
        start_time = datetime.datetime.now()
        if repeat_value == 1:
            repeat_status_str = '현재 상태: 전체 반복'
        elif one_repeat_value == 1:
            repeat_status_str = '현재 상태: 단일 반복'
        else:
            repeat_status_str = '현재 상태: 순차 재생'
        print_time_O = datetime.datetime(2000,10,1,hour=hour_O, minute=min_O, second=sec_O).strftime('%H:%M:%S')
        play_embed = discord.Embed(title=f"Playing status           [00:00:00 / {print_time_O}]", color=discord.Colour.blue())
        play_embed.add_field(name="| 현재 노래", value=now.replace(".mp3",""), inline=False)
        play_embed.add_field(name="| 가사\n로딩 중", value='.', inline=False)
        play_embed.add_field(name="| 반복 여부", value=repeat_status_str.replace('현재 상태: ', ''), inline=True)
        play_embed.add_field(name="| 사운드 이펙트", value=eq_value_in, inline=True)
        play_embed.add_field(name="| 현재 재생 상태", value=Play_status_massage, inline=True)
        msg = await ctx.send(embed=play_embed)

        print('now timer start')
        caption_content = ''
        captions_list = []
        caption_groups = []
        now_caption = '존재하지 않음'
        start_caption_time = ''
        if i.split('/')[-1].replace(".mp3",".txt") in os.listdir("E:/mp3 폴더/유튭/"):
            with open("E:/mp3 폴더/유튭/" + i.split('/')[-1].replace(".mp3",".txt"),'r') as f:
                caption_content = f.read()
            captions_list = caption_content.split('\n\n')
            caption_groups = [(x.split('\n')[1].split(',')[0],x.split('\n')[2]) for x in captions_list]
            start_caption_time = caption_groups[0][0]
        while vc.is_playing() or status_value:
            while status_value :
                if pause_value == 0:
                    pause_now =  datetime.datetime.now()
                    pause_value = 1
                await asyncio.sleep(1)
            if pause_value == 1:
                pause_end = datetime.datetime.now()
                pause_times = (pause_end - pause_now).total_seconds()
                total_pause += pause_times
                pause_value = 0
            if skip_value == 1:
                print('스킵 처리')
                vc.stop()
                print('완료')
                skip_value = 0
                break
            await asyncio.sleep(0.7)
            vc.source.volume = volume_
            Progress_time = (datetime.datetime.now() - start_time).total_seconds() - total_pause
            if length <= Progress_time:
                Progress_time = length
            sec_, min_, hour_ = int(Progress_time%60), int((Progress_time//60)%60), int((Progress_time//60)//60)
            print_time = datetime.datetime(2000,10,1,hour=hour_, minute=min_, second=sec_).strftime('%H:%M:%S')
            print_time_O = datetime.datetime(2000,10,1,hour=hour_O, minute=min_O, second=sec_O).strftime('%H:%M:%S')
            if caption_content != '':
                for k in [x[0] for x in caption_groups]:
                    if f'{print_time}' < start_caption_time:
                        back_caption = ''
                        now_caption = '전주 중'
                        for_caption = ''
                        break
                    elif f'{print_time}' < k:
                        now_caption = now_caption
                    else:
                        now_caption = caption_groups[0][1]
                        caption_groups.pop(0)
            repeat_status_str = ''
            if repeat_value == 1:
                repeat_status_str = '현재 상태: 전체 반복'
            elif one_repeat_value == 1:
                repeat_status_str = '현재 상태: 단일 반복'
            else:
                repeat_status_str = '현재 상태: 순차 재생'
            play_embed = discord.Embed(title=f"Playing status           [ {print_time} / {print_time_O} ]", color=discord.Colour.blue())
            play_embed.add_field(name="| 현재 노래", value=now.replace(".mp3",""), inline=False)
            play_embed.add_field(name="| 가사 \n"+now_caption+" ", value='.', inline=False)
            play_embed.add_field(name="| 반복 여부", value=repeat_status_str.replace('현재 상태: ', ''), inline=True)
            play_embed.add_field(name="| 사운드 이펙트", value=eq_value_in, inline=True)
            play_embed.add_field(name="| 현재 재생 상태", value=Play_status_massage, inline=True)
            await msg.edit(embed=play_embed)
        await msg.delete()
        if repeat_value == 1:
            queue.pop(-1)
            queue.append(i)
            queue.append('Dump')
        if one_repeat_value == 1:
            queue.insert(now_index, i)

def fmt(x, w, align='r'):
    x = str(x)
    l = wcswidth(x)
    s = w-l
    if s <= 0:
        return x
    if align == 'l':
        return x + ' '*s
    if align == 'c':
        sl = s//2
        sr = s - sl
        return ' '*sl + x + ' '*sr
    return ' '*s + x

@bot.event
async def on_ready():
    global list_value
    print('봇이 준비되었습니다')
    list_value = 0

@bot.command()
async def 도움(ctx):
    print('[도움] 커맨드가 전달되었습니다')
    await ctx.send('무엇을 도와드릴까요?')
    print('[도움] 커맨드가 전달되었습니다')

@bot.command()
async def 이퀄라이저(ctx, value='에코'):
    print('[이퀄라이저] 커맨드가 전달되었습니다')
    global eq_value
    eq_value = value
    if value == '에코' or value == '기본':
        await ctx.send(f'이퀄라이저 [{value}]를 적용합니다')
    else:
        await ctx.send(f'그런건...몰라...')

@bot.command()
async def 교체(ctx, value):
    print('[교체] 커맨드가 전달되었습니다')
    await 끼워넣기(ctx, value)
    await 스킵(ctx)
    await 큐(ctx)

@bot.command()
async def 제거(ctx, value=2):
    print('[제거] 커맨드가 전달되었습니다')
    global queue, now_index
    queue.pop(now_index+value-2)
    await 큐(ctx)

@bot.command()
async def 검색(ctx, *args):
    print("[검색] 커맨드가 전달되었습니다")
    global files, search_value, search_list
    if search_value == 1:
        files = os.listdir(PATH)
    if args == []:
        await ctx.send('뭐라도 입력해야할거 아냐...')
    else:
        sentence = "".join(args)
        files = [result for result in files if sentence.lower() in result.lower().replace(" ","")]
        if len(files) == 0:
            await ctx.send('그런건...없다구...')
        else:
            search_value = 1
            search_list = [sentence]
            await 책(ctx)

@bot.command()
async def 이어서검색(ctx, *args):
    print('[이어서검색] 커맨드가 전달되었습니다')
    global search_value, files
    if search_value ==1:
        if args == []:
            await ctx.send('뭐라도 입력해야할거 아냐...')
        else:
            sentence = "".join(args)
            files = [result for result in files if sentence.lower() in result.lower().replace(" ","")]
            if len(files) == 0:
                await ctx.send('그런건...없다구...')
            else:
                search_list.append(sentence)
            search_value = 1
            await 책(ctx)
    else:
        await ctx.send('이전 검색이 존재하지 않습니다')

@bot.command()
async def 유튭(ctx, *args):
    print('[유튭] 커맨드가 전달되었습니다')
    global driver, title_list, url_list, len_, num, url_select_num, t_list, now_index, queue, msg_youtube, link_data, new_filename
    new_filename = ''
    value = " ".join(args)
    link_data = ''
    if value.startswith('https') or value.startswith('youtube.com') or value.startswith('youtu.be'):
        if '&list' in value:
            link_data = value
            playlist = Playlist(link_data)
            playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
            listlink_len = len(playlist)
            await ctx.send(f'이 링크는 {listlink_len}개의 재생목록을 포함하고 있습니다. 이 작업은 모든 프로세스를 임시 중단하며 이 동안 봇의 이용이 불가합니다.')
            await ctx.send('재생목록이 아닌 단일목록을 다운로드하려면 링크의 &list 와 그 뒷부분을 모두 지우고 입력하세요.')
            await ctx.send('정말 이 명령을 실행하시려면 [//실행] 커맨드를 입력하여주세요.')
        else:
            select = value
            yt = YouTubeItem(select, request_headers={'cookie':cookie})
            vids= yt.streams.all()
            vids[0].download("E:/mp3 폴더/유튭/")

            default_filename = vids[0].default_filename
            new_filename = default_filename.replace(".mp4",".mp3")
            print("E:/mp3 폴더/유튭/"+new_filename)
            if new_filename in os.listdir("E:/mp3 폴더/유튭/"):
                temp = ''
            else:
                subprocess.call(['ffmpeg', '-i',                 #cmd 명령어 수행
                    os.path.join("E:/mp3 폴더/유튭/", default_filename),
                    os.path.join("E:/mp3 폴더/유튭/", new_filename)
                ])
                await ctx.send(f'[ {new_filename.replace(".mp3","")} ] 항목을 저장했습니다.')
                print('mp3 변환 완료')
            if new_filename.replace(".mp3",".txt") in os.listdir("E:/mp3 폴더/유튭/"):
                print('자막 존재')
                await ctx.send('자막 파일을 추가하였습니다.')
            else:
                caption = yt.captions.get_by_language_code('ko')
                if caption == None:
                    caption = yt.captions.get_by_language_code('en')
                    if caption == None:
                        caption = yt.captions.all()[0]
                if caption != None:
                    with open("E:/mp3 폴더/유튭/" + new_filename.replace(".mp3",".txt"),'w') as f:
                        f.write(caption.generate_srt_captions())
                print('자막 저장 완료')
            os.remove("E:/mp3 폴더/유튭/"+default_filename)
            shutil.copy("E:/mp3 폴더/유튭/"+new_filename, "E:/mp3 폴더/전체/")
            if play_value  == 0:
                queue = ["E:/mp3 폴더/유튭/"+new_filename, 'Dump']
                user=ctx.message.author
                voice_channel=user.voice.channel
                channel=voice_channel.name
                await ctx.send('현재 접속 채널: '+ channel)
                await play_list(ctx, vc, channel)
            else:
                queue.insert(now_index,"E:/mp3 폴더/유튭/"+new_filename)
            await 큐(ctx)
    elif not value.isdigit():
        title_list = []
        url_list = []
        num = 1
        print(value)
        driver.get(f'https://www.youtube.com/results?search_query={urllib.parse.quote(value)}')
        await asyncio.sleep(1)
        page = driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        all_videos = soup.find_all(id='dismissable')
        for video in all_videos:
            if num <= len_:
                num += 1
            else: break
            title = video.find(id='video-title')
            url = video.find(id='thumbnail').attrs['href']
            if len(title.text.strip())>0:
                if title.text.replace("\n","") in title_list:
                    num-=1
                else:
                    title_list.append(title.text.replace("\n",""))
                    url_list.append(site_url+url)
        t_list = f'[{value}] 유튜브 검색 결과'
        for i in range(5):
            t_list += '\n' + str(i+1) + '번: ' + title_list[i]
        if not msg_youtube is None :
            await msg_youtube.delete()
            msg_youtube = await ctx.send(t_list)
        else:
            msg_youtube = await ctx.send(t_list)
    else:
        if len(title_list) == 0:
            await ctx.send('아무 검색어도 입력하지 않았습니다')
        else:
            num = int(value) - 1
            select = url_list[num]
            print(title_list[num])
            print(select)
            if msg_youtube != None:
                await msg_youtube.delete()
            msg_youtube = None
            await ctx.send(f'{value}번 - {title_list[num]}를 선택하였습니다.')
            yt = YouTubeItem(select, request_headers={'cookie':cookie})
            vids= yt.streams.all()
            vids[0].download("E:/mp3 폴더/유튭/")

            default_filename = vids[0].default_filename
            new_filename = default_filename.replace(".mp4",".mp3")
            print("E:/mp3 폴더/유튭/"+new_filename)
            if new_filename in os.listdir("E:/mp3 폴더/유튭/"):
                temp = ''
            else:
                subprocess.call(['ffmpeg', '-i',                 #cmd 명령어 수행
                    os.path.join("E:/mp3 폴더/유튭/", default_filename),
                    os.path.join("E:/mp3 폴더/유튭/", new_filename)
                ])
                await ctx.send(f'[ {new_filename.replace(".mp3","")} ] 항목을 저장했습니다.')
                print('mp3 변환 완료')
            if new_filename.replace(".mp3",".txt") in os.listdir("E:/mp3 폴더/유튭/"):
                print('자막 존재')
            else:
                caption = yt.captions.get_by_language_code('ko')
                if caption == None:
                    caption = yt.captions.get_by_language_code('en')
                    if caption == None:
                        caption = yt.captions.all()[0]
                if caption != None:
                    with open("E:/mp3 폴더/유튭/" + new_filename.replace(".mp3",".txt"),'w') as f:
                        f.write(caption.generate_srt_captions())
                print('자막 저장 완료')
                await ctx.send('자막 파일을 추가하였습니다.')
            os.remove("E:/mp3 폴더/유튭/"+default_filename)
            shutil.copy("E:/mp3 폴더/유튭/"+new_filename, "E:/mp3 폴더/전체/")
            if play_value  == 0:
                queue = ["E:/mp3 폴더/유튭/"+new_filename, 'Dump']
                user=ctx.message.author
                voice_channel=user.voice.channel
                channel=voice_channel.name
                await ctx.send('현재 접속 채널: '+ channel)
                await play_list(ctx, vc, channel)
                await 큐(ctx)
            else:
                queue.insert(now_index,"E:/mp3 폴더/유튭/"+new_filename)
            title_list = []
            url_list = []
            await 큐(ctx)

@bot.command()
async def 실행(ctx):
    print('[실행] 커맨드가 전달되었습니다')
    global link_data, fail_list, new_filename
    if link_data != '':
        await ctx.send('재생목록을 다운로드합니다.\n재생목록의 특성상 모든 컨텐츠(제한:100)를 다운로드하지 못할 수 있습니다.')
        playlist = Playlist(link_data)
        link_data = ''
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        temp_value = 0
        link_msg = await ctx.send(f'Progress... 0 / {len(playlist)}')
        fail_list = []
        for i in playlist:
            temp_value += 1
            try:
                yt = YouTubeItem(select, request_headers={'cookie':cookie})
                vids= yt.streams.all()
                vids[0].download("E:/mp3 폴더/유튭/")

                default_filename = vids[0].default_filename
                new_filename = default_filename.replace(".mp4",".mp3")
                print("E:/mp3 폴더/유튭/"+new_filename)
                if new_filename in os.listdir("E:/mp3 폴더/유튭/"):
                    temp = ''
                else:
                    subprocess.call(['ffmpeg', '-i',                 #cmd 명령어 수행
                        os.path.join("E:/mp3 폴더/유튭/", default_filename),
                        os.path.join("E:/mp3 폴더/유튭/", new_filename)
                    ])
                    await ctx.send(f'[ {new_filename.replace(".mp3","")} ] 항목을 저장했습니다.')
                    print('mp3 변환 완료')
                if new_filename.replace(".mp3",".txt") in os.listdir("E:/mp3 폴더/유튭/"):
                    print('자막 존재')
                else:
                    caption = yt.captions.get_by_language_code('ko')
                    if caption == None:
                        caption = yt.captions.get_by_language_code('en')
                        if caption == None:
                            caption = yt.captions.all()[0]
                    if caption != None:
                        with open("E:/mp3 폴더/유튭/" + new_filename.replace(".mp3",".txt"),'w') as f:
                            f.write(caption.generate_srt_captions())
                    print('자막 저장 완료')
                    await ctx.send('자막 파일을 추가하였습니다.')
                os.remove("E:/mp3 폴더/유튭/"+default_filename)
                shutil.copy("E:/mp3 폴더/유튭/"+new_filename, "E:/mp3 폴더/전체/")
            except Exception as e:
                print(e)
                await ctx.send(f'오류가 발생하였습니다. 오류 발생 번호 : {temp_value}')
                fail_list.append(i)
        if file_list != []:
            await ctx.send('모든 다운로드가 끝났습니다. 실패 목록은 \n\n{} \n\n입니다'.format("\n".join(fail_list)))
        else:
            await ctx.send('모든 다운로드가 끝났습니다. 모든 목록 다운로드에 성공하였습니다!')
    elif fail_list != []:
        await ctx.send('모든 다운로드가 끝났습니다. 실패 목록은 \n\n{} \n\n입니다'.format("\n".join(fail_list)))
        download_list = fail_list.copy()
        fail_list = []
        temp_value = 0
        for i in download_list:
            temp_value += 1
            try:
                yt = YouTubeItem(select, request_headers={'cookie':cookie})
                vids= yt.streams.all()
                vids[0].download("E:/mp3 폴더/유튭/")

                default_filename = vids[0].default_filename
                new_filename = default_filename.replace(".mp4",".mp3")
                print("E:/mp3 폴더/유튭/"+new_filename)
                if new_filename in os.listdir("E:/mp3 폴더/유튭/"):
                    temp = ''
                else:
                    subprocess.call(['ffmpeg', '-i',                 #cmd 명령어 수행
                        os.path.join("E:/mp3 폴더/유튭/", default_filename),
                        os.path.join("E:/mp3 폴더/유튭/", new_filename)
                    ])
                    await ctx.send(f'[ {new_filename.replace(".mp3","")} ] 항목을 저장했습니다.')
                    print('mp3 변환 완료')
                if new_filename.replace(".mp3",".txt") in os.listdir("E:/mp3 폴더/유튭/"):
                    print('자막 존재')
                else:
                    caption = yt.captions.get_by_language_code('ko')
                    if caption == None:
                        caption = yt.captions.get_by_language_code('en')
                        if caption == None:
                            caption = yt.captions.get_by_language_code('jp')
                            if caption == None:
                                caption = yt.captions.all()[0]
                    if caption != None:
                        with open("E:/mp3 폴더/유튭/" + new_filename.replace(".mp3",".txt"),'w') as f:
                            f.write(caption.generate_srt_captions())
                    print('자막 저장 완료')
                    await ctx.send('자막 파일을 추가하였습니다.')
                os.remove("E:/mp3 폴더/유튭/"+default_filename)
                shutil.copy("E:/mp3 폴더/유튭/"+new_filename, "E:/mp3 폴더/전체/")
            except Exception as e:
                print(e)
                await ctx.send(f'오류가 발생하였습니다. 오류 발생 번호 : {temp_value}')
                fail_list.append(i)
        if file_list != []:
            await ctx.send('모든 다운로드가 끝났습니다. 실패 목록은 \n\n{} \n\n입니다'.format("\n".join(fail_list)))
        else:
            await ctx.send('모든 다운로드가 끝났습니다. 모든 목록 다운로드에 성공하였습니다!')
    else:
        ctx.send('전달받은 재생목록 다운로드 명령어가 없습니다.')

@bot.command()
async def 검색종료(ctx):
    print("[검색종료] 커맨드가 전달되었습니다")
    global search_value
    search_value = 0
    await 책(ctx)

@bot.command()
async def 큐(ctx, value=1):
    print('[큐] 커맨드가 전달되었습니다')
    global queue, queue_now_page, now_index, msg_queue
    if queue != []:
        if value == '다음':
            queue_now_page +=1
        else:
            queue_now_page = value
        q_num = ''
        q_title = ''
        queue_total_page = len(queue[now_index-1:-1])//10 + 1
        if queue_now_page > queue_total_page:
            await ctx.send('페이지가 너무...커...')
        elif queue_now_page < 1:
            await ctx.send('...작네...?')
        elif queue_now_page != queue_total_page:
            for i,j in enumerate((queue[now_index-1:-1])[(queue_now_page-1)*10:queue_now_page*10]):
                q_num += str((queue_now_page-1)*10+i+1) + "번\n"
                if len(j.replace(".mp3","").split('/')[-1] + "\n") > 40:
                    q_title += (j.replace(".mp3","").split('/')[-1])[:40] + "...\n"
                else:
                    q_title += (j.replace(".mp3","").split('/')[-1]) + "\n"
        else:
            for i,j in enumerate((queue[now_index-1:-1])[(queue_now_page-1)*10:]):
                q_num += str((queue_now_page-1)*10+i+1) + "번\n"
                if len(j.replace(".mp3","").split('/')[-1] + "\n") > 40:
                    q_title += (j.replace(".mp3","").split('/')[-1])[:40] + "...\n"
                else:
                    q_title += (j.replace(".mp3","").split('/')[-1]) + "\n"
        embed=discord.Embed(title=f"Queue Page[{queue_now_page}/{queue_total_page}]  Total: {len(queue[now_index-1:])-1}", color=0xEF441D)
        embed.add_field(name="번호", value=q_num, inline=True)
        embed.add_field(name="제목", value=q_title, inline=True)
        if not msg_queue is None:
            await msg_queue.delete()
            msg_queue = await ctx.send(embed=embed)
        else:
            msg_queue = await ctx.send(embed=embed)
    else:
        print('There is no songs in queue')

@bot.command()
async def 끼워넣기(ctx, value):
    print('[끼워넣기] 커맨드가 전달되었습니다')
    global now_index, queue, files, one_repeat_value
    if one_repeat_value == 1:
        await ctx.send('현재 상태는 단일 반복입니다. 끼워넣어도 계속 현재 노래가 재생됩니다.')
    select=value.replace(" ","")
    list_=select.split(',')
    for i in list(reversed(list_)):
        if len(i.split(':'))==2:
            for j in range(int(i.split(':')[0]),int(i.split(':')[1])+1):
                queue.insert(now_index, PATH+files[j-1])
        else:
            queue.insert(now_index, PATH+files[int(i)-1])
    await 큐(ctx)

@bot.command()
async def 추가(ctx, value):
    print('[추가 커맨드가 전달되었습니다]')
    global queue, files, one_repeat_value
    if one_repeat_value == 1:
        await ctx.send('현재 상태는 단일 반복입니다. 추가하여도 계속 현재 노래가 재생됩니다.')
    select=value.replace(" ","")
    list_=select.split(',')
    temp = queue.pop(-1)
    for i in list_:
        if len(i.split(':'))==2:
            for j in range(int(i.split(':')[0]),int(i.split(':')[1])+1):
                queue.append(PATH+files[j-1])
        else:
            print(i)
            queue.append(PATH+files[int(i)-1])
    queue.append('Dump')
    await 큐(ctx)

@bot.command()
async def 종료(ctx):
    global driver, msg_book, msg_queue, msg
    print('[종료] 커맨드가 전달되었습니다')
    await msg_queue.delete()
    await msg_book.delete()
    await msg.delete()
    server = ctx.message.guild.voice_client
    if type(server) != None:
        await server.disconnect()
    await ctx.send('봇을 종료합니다')
    await bot.close()
    driver.quit()

@bot.command()
async def 장르(ctx, value):
    print('[장르] 커맨드가 전달되었습니다')
    global PATH, content_value, search_value, page_num
    if search_value == 1:
        await ctx.send('검색 도중 장르변경이 감지되었습니다. 검색을 초기화합니다.')
        await 검색종료(ctx)
    if value == '클래식':
        PATH = 'E:/mp3 폴더/Classic/'
        content_value = '클래식'
    elif value == '덕덕':
        PATH = 'E:/mp3 폴더/덕질용/'
        content_value = '덕덕'
    elif value == '가요':
        PATH = 'E:/mp3 폴더/가요/'
        content_value = '가요'
    elif value == '우타이테':
        PATH = 'E:/mp3 폴더/우타이테/'
        content_value = '우타이테'
    elif value == '전체':
        PATH = 'E:/mp3 폴더/전체/'
        content_value = '전체'
    elif value == '유튭':
        PATH = 'E:/mp3 폴더/유튭/'
        content_value = '유튭'
    elif value == 'NCS':
        PATH = 'E:/mp3 폴더/NCS/'
        content_value = 'NCS'
    elif value == 'AW':
        PATH = 'E:/mp3 폴더/Alan Walker/'
        content_value = 'Alan Walker'
    else:
        await ctx.send('그런 장르는 모르는데...')
    now_page = 1
    print(f'현재 패스는 {PATH}입니다')
    await 책(ctx)

@bot.command(pass_context=True)
async def 참가(ctx):
    print('[참가] 커맨드가 전달되었습니다')
    global vc, ctx_global, Voice_detected_value, Voice_command_value
    ctx_global = ctx
    channel = ctx.message.author.voice.channel
    vc = await channel.connect()
    await 책(ctx)

@bot.command()
async def 반복(ctx):
    print('[반복] 커맨드가 전달되었습니다')
    global queue, now_index, repeat_value, one_repeat_value
    await ctx.send('현재 큐를 반복합니다')
    one_repeat_value = 0
    repeat_value = 1

@bot.command()
async def 단일반복(ctx):
    print('[단일반복] 커맨드가 전달되었습니다')
    global one_repeat_value, repeat_value
    await ctx.send('현재 노래를 반복합니다')
    one_repeat_value = 1
    repeat_value = 0

@bot.command()
async def 반복종료(ctx):
    print('[반복종료] 커맨드가 전달되었습니다')
    global repeat_value, one_repeat_value
    await ctx.send('반복을 종료합니다')
    repeat_value = 0
    one_repeat_value = 0

@bot.command(pass_context=True)
async def 추방(ctx):
    print('[추방] 커맨드가 전달되었습니다')
    print(type(ctx.message))
    server = ctx.message.guild.voice_client
    await server.disconnect()

@bot.command()
async def 재생(ctx, value='랜덤반복'):
    print('[재생] 커맨드가 전달되었습니다')
    global vc, files, list_value, repeat_value, queue, play_value, Play_status_massage
    if play_value == 1:
        await ctx.send('이미 재생중인데요? [//추가] 명령어로 원하는 노래를 대기열에 추가해보세요.')
        return 0
    if list_value == 0:
        await ctx.send('[//책] 명령어를 먼저 사용해주세요')
        pass
    user=ctx.message.author
    voice_channel=user.voice.channel
    channel=None
    repeat_value = 0
    queue=[]
    if voice_channel!= None:
        if value == '랜덤반복':
            queue = files.copy()
            for i in range(len(queue)):
                queue[i] = PATH + queue[i]
            random.shuffle(queue)
            print(queue)
            repeat_value = -1
        elif value == '순서반복':
            queue = files.copy()
            for i in range(len(queue)):
                queue[i] = PATH + queue[i]
            repeat_value = -1
        elif value == '':
            await ctx.send('//재생 명령어 뒤에 공백을 넣은 것 같아요. 다시 시도해주세요')
        else :
            select=value.replace(" ","")
            list_=select.split(',')
            for i in list_:
                if len(i.split(':'))==2:
                    for j in range(int(i.split(':')[0]),int(i.split(':')[1])+1):
                        queue.append(PATH+files[j-1])
                else:
                    print(i)
                    queue.append(PATH+files[int(i)-1])
        queue.append('Dump')
        print(queue)
        channel=voice_channel.name
        await ctx.send('현재 접속 채널: '+ channel)
        Play_status_massage = '재생 중'
        await play_list(ctx, vc, channel)
    else:
        await ctx.send('니부터 채널에 들어가야지')

@bot.command()
async def 일시정지(ctx):
    print('[일시정지] 커맨드가 전달되었습니다')
    global vc, status_value, Play_status_massage
    Play_status_massage = '일시정지'
    status_value = True
    vc.pause()

@bot.command()
async def 계속(ctx):
    print('[계속] 커맨드가 전달되었습니다')
    global vc, status_value, Play_status_massage
    Play_status_massage = '재생 중'
    status_value = False
    vc.resume()

@bot.command()
async def 정지(ctx):
    print('[정지] 커맨드가 전달되었습니다')
    global vc, repeat_value, play_value, repeat_value, Play_status_massage
    Play_status_massage = '정지'
    repeat_value = 0
    play_value = 0
    repeat_value = 0
    try:
        vc.stop()
        server = ctx.message.guild.voice_client
        await server.disconnect()
    except:
        repeat_value = 0
    channel = ctx.message.author.voice.channel
    vc = await channel.connect()

@bot.command()
async def 스킵(ctx):
    print('[스킵] 커맨드가 전달되었습니다')
    global vc, skip_value, one_repeat_value

    if one_repeat_value == 1:
        await ctx.send('현재 상태는 단일 반복입니다. 스킵하여도 계속 현재 노래가 재생됩니다.')

    skip_value = 1

@bot.command()
async def 책(ctx, *args):
    print('[책] 커맨드가 전달되었습니다')
    global files, list_value, value, now_page, PATH, content_value, search_list, search_value, msg_book
    if search_value == 1:
        search_str = "검색 : " + " => ".join(search_list)
        now_page = 1
    else:
        search_str = ''
    if args == ():
        print('no args')
    elif len(args)==1:
        if args[0]=='다음':
            now_page+=1
        elif args[0] == '가수':
            value = '가수'
            now_page = 1
        elif args[0] == '제목':
            value = '제목'
            now_page = 1
        elif args[0].isdigit():
            now_page = int(args[0])
    elif len(args)==2:
        if args[0] == '가수':
            value = '가수'
        elif args[0] == '제목':
            value = '제목'
        else:
            await ctx.send('뭐야... 그거...')
        if args[1].isdigit():
            now_page = int(args[1])
    else :
        await ctx.send('뭐야... 그거...')

    if (PATH == 'E:/mp3 폴더/우타이테/'
    or PATH == 'E:/mp3 폴더/덕질용/'
    or PATH == 'E:/mp3 폴더/가요/'
    or PATH == 'E:/mp3 폴더/NCS/'
    or PATH == 'E:/mp3 폴더/Alan Walker/'):
        list_value = 1
        if search_value == 0:
            files = [x for x in os.listdir(PATH) if not '.txt' in x]
        print(args)

        if value == '가수':
            files.sort(key=lambda x: x.split(' - ')[0])
        elif value == '제목':
            files.sort(key=lambda x: x.split(' - ')[1])
        else :
            await ctx.send('뭐야 그건?')

        total_pages = len(files)//10 + 1
        num, artist, title = '', '', ''
        if now_page > total_pages:
            await ctx.send('페이지가 너무...커')
        elif now_page < 1:
            await ctx.send('...작네...?')
        elif now_page != total_pages:
            for i,j in enumerate(files[(now_page-1)*10:now_page*10]):
                num += str((now_page-1)*10+i+1) + "번\n"
                artist += j.split(' - ')[0] + "\n"
                if len(j.split(' - ')[1].replace(".mp3","")) > 35:
                    title += j.split(' - ')[1].replace(".mp3","")[:35] + "...\n"
                else:
                    title += j.split(' - ')[1].replace(".mp3","") + "\n"
        else:
            for i,j in enumerate(files[(now_page-1)*10:]):
                num += str((now_page-1)*10+i+1) + "번\n"
                artist += j.split(' - ')[0] + "\n"
                if len(j.split(' - ')[1].replace(".mp3","")) > 35:
                    title += j.split(' - ')[1].replace(".mp3","")[:35] + "...\n"
                else:
                    title += j.split(' - ')[1].replace(".mp3","") + "\n"
        if now_page > total_pages or now_page < 1:
            now_page = 1
        if value == '가수':
            embed=discord.Embed(title=f"{content_value} - 노래 목록 Page[{now_page}/{total_pages}]  Total: {len(files)}\n{search_str}", description=f"정렬: {value}", color=0x00ff56)
            embed.add_field(name="번호", value=num, inline=True)
            embed.add_field(name="가수", value=artist, inline=True)
            embed.add_field(name="제목", value=title, inline=True)
        else:
            embed=discord.Embed(title=f"{content_value} - 노래 목록 Page[{now_page}/{total_pages}]  Total: {len(files)}\n{search_str}", description=f"정렬: {value}", color=0x00ff56)
            embed.add_field(name="번호", value=num, inline=True)
            embed.add_field(name="제목", value=title, inline=True)
            embed.add_field(name="가수", value=artist, inline=True)
        if not msg_book is None:
            await msg_book.delete()
            msg_book = await ctx.send(embed=embed)
        else:
            msg_book = await ctx.send(embed=embed)

    else:
        list_value = 1
        if search_value == 0:
            files = os.listdir(PATH)
        num, artist, title = '', '', ''
        total_pages = len(files)//10 + 1 if len(files)%10 !=0 else len(files)//10

        if now_page > total_pages:
            await ctx.send('페이지가 너무...커...')
        elif now_page < 1:
            await ctx.send('...작네...?')
        elif now_page != total_pages:
            for i,j in enumerate(files[(now_page-1)*10:now_page*10]):
                num += str((now_page-1)*10+i+1) + "번\n"
                if len(j.replace(".mp3","")) > 35:
                    title += j.replace(".mp3","")[:35] + "...\n"
                else:
                    title += j.replace(".mp3","") + "\n"
        else:
            for i,j in enumerate(files[(now_page-1)*10:]):
                num += str((now_page-1)*10+i+1) + "번\n"
                if len(j.replace(".mp3","")) > 35:
                    title += j.replace(".mp3","")[:35] + "...\n"
                else:
                    title += j.replace(".mp3","") + "\n"
        embed=discord.Embed(title=f"{content_value} - 노래 목록 Page[{now_page}/{total_pages}]  Total: {len(files)}\n{search_str}", color=0x00ff56)
        embed.add_field(name="번호", value=num, inline=True)
        embed.add_field(name="제목", value=title, inline=True)
        if not msg_book is None:
            await msg_book.delete()
            msg_book = await ctx.send(embed=embed)
        else:
            msg_book = await ctx.send(embed=embed)

@bot.command()
async def 볼륨업(ctx):
    print('[볼륨업] 커맨드가 전달되었습니다')
    global vc, volume_
    if int(vc.source.volume*100) != 100:
        volume_ +=0.05
        await ctx.send(f'현재 볼륨은 {int(vc.source.volume*100)}%입니다')
    else:
        await ctx.send('이미 ㅈㄴ큰데 얼마나 더 키워야해?')

@bot.command()
async def 볼륨다운(ctx):
    print('[볼륨다운] 커맨드가 전달되었습니다')
    global vc, volume_
    if int(vc.source.volume*100) != 0:
        volume_ -= 0.05
        await ctx.send(f'현재 볼륨은 {int(vc.source.volume*100)}%입니다')
    else:
        await ctx.send('이게 들려? 토끼가 따로없네')

@bot.command()
async def 볼륨(ctx, value):
    print('[볼륨] 커맨드가 전달되었습니다')
    global volume_
    volume_ = float(value)/100
    await ctx.send(f'현재 볼륨은 {int(volume_*100)}%입니다')

@bot.command()
async def 마법의소라고둥님(ctx, *, question):
    print('[마법의소라고둥님] 커맨드가 전달되었습니다')
    responses=['그럼', '아니']
    await ctx.send(f'Question: {question} \nAnswer: {random.choice(responses)}')

@bot.command()
async def 싹쓸이(ctx, amount=5):
    print('[싹쓸이] 커맨드가 전달되었습니다')
    await ctx.channel.purge(limit=int(amount))
"""
@bot.event
async def on_error(ctx, error):
    print(error)

@bot.event
async def on_command_error(ctx, error):
    print(error)"""
bot.run(token)
