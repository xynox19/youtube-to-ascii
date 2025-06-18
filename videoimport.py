from pytube import YouTube

yt = YouTube("https://www.youtube.com/watch?v=9lNZ_Rnr7Jc") #add whichever video you would desire
stream = yt.streams.filter(res="360p", file_extension='mp4').first()
stream.download(filename="bad_apple.mp4") #change filename as needed
