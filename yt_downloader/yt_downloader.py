from pytube import Playlist as yt_playlist
from pytube import YouTube as yt
import pytube

import unicodedata
import subprocess
import sys
import os

def convert(file_name, path):
	_command = 'ffmpeg -i \"' + path + '/' + file_name + '.mp4\" \"' + path + '/' + file_name + '.mp3\"'
	subprocess.run(_command)
	os.remove(os.path.join(path, file_name + '.mp4'))
	return

def on_download_proggress(stream, chunk, bytes_remaining): 
	_percent = round(( ( float(stream.filesize - bytes_remaining) / float(stream.filesize) ) * float(100)), 2)
	_text = f"\r - downloading: {_percent}%"
	sys.stdout.write(_text)
	sys.stdout.flush()
	return

def on_download_complete(stream, file_handle):
	print(f' {stream.title} [ done ] ')
	return

def main():
	_convert_to_mp3 = True
	_convert_list = []

	print('[yt_downloader]: _playlist_link: ', end = '')
	_playlist_link = input()

	print('[yt_downloader]: _folder_name: ', end = '')
	_folder_name = input()

	_our_playlist_obj = yt_playlist(_playlist_link)
	print('[yt_downloader]: list of videos url in playlist [%s videos]:' % len( _our_playlist_obj.video_urls ))

	for video_url in _our_playlist_obj.video_urls:
		print(' - ' + video_url)

		_video = yt(video_url)
		_video.register_on_progress_callback(on_download_proggress)
		_video.register_on_complete_callback(on_download_complete)
						 
		_video.streams.filter(only_audio=True).first().download(output_path = _folder_name, filename = pytube.helpers.safe_filename(_video.title))
		if (_convert_to_mp3):
			_convert_list.append(_video.title)

	# convert
	if(_convert_to_mp3):
		for video in _convert_list:
			convert(video, _folder_name)

	return

main()

# remake to c++ + gui