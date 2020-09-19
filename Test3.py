import pytube

yt = pytube.YouTube('https://www.youtube.com/watch?v=G2e7oMEMTkk')
print(yt.captions.all())