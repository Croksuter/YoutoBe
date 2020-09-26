import pytube

yt = pytube.YouTube('https://www.youtube.com/watch?v=_9s4bAJMRn0')
print(yt.captions.all()[0].generate_srt_captions())