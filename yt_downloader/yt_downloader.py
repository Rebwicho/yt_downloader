from pytube import Playlist as yt_playlist
import sys

def on_download_proggress(stream, chunk, bytes_remaining): 
	_percent = round(( ( float(stream.filesize - bytes_remaining) / float(stream.filesize) ) * float(100)), 2)
	_text = f"\r - downloading: {stream.title} / {_percent}%"
	sys.stdout.write(_text)
	sys.stdout.flush()
	return

def on_download_complete(stream, file_handle):
	print(' [ done ] ')
	return

print('[yt_downloader]: _playlist_link: ', end = '')
_playlist_link = input()

print('[yt_downloader]: _folder_name: ', end = '')
_folder_name = input()

_our_playlist_obj = yt_playlist(_playlist_link)
print('[yt_downloader]: list of videos url in playlist:')
for video_url in _our_playlist_obj.video_urls:
	print(' - ' + video_url)

print('[yt_downloader]: found %s videos:' % len( _our_playlist_obj.video_urls ) )

for video in _our_playlist_obj.videos:
	video.register_on_progress_callback(on_download_proggress)
	video.register_on_complete_callback(on_download_complete)

	_video_stream = video.streams.filter(only_audio=True).first()

	_video_stream.download(output_path = _folder_name)