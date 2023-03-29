from pytube import YouTube
import pytube.request
import sys


pytube.request.default_range_size = 9437184

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = round(bytes_downloaded / total_size * 100, 2)
    sys.stdout.write('\r' + '|' + '#'*int(percentage_of_completion) + '.' * (100 - int(percentage_of_completion)) + '|   ' + percentage_of_completion )
    sys.stdout.flush()

url = "https://www.youtube.com/watch?v=ztHopE5Wnpc"

# Create the YouTube object first
yt_obj = YouTube(url)

# Then register the callback
yt_obj.register_on_progress_callback(on_progress)

# Download the video, getting back the file path the video was downloaded to
file_path = yt_obj.streams.filter(progressive=True).get_highest_resolution().download()
print(f"file_path is {file_path}")