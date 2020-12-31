import subprocess

# combining / muxing visual and audio
cmd = './ffmpeg -y -i audio.webm  -r 30 -i vid.webm  -filter:a aresample=async=1 -c:a flac -c:v copy again.mkv'
subprocess.call(cmd, shell=True)                                     # "Muxing Done
print('Muxing Done')
