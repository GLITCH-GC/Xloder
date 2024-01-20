# Youtube Downloader
# By - Abdelrahman Ghareeb (GLITCH)
# Download Videos Youtube And Playlists

from pytube import Playlist, YouTube
from tqdm import tqdm
import pyfiglet
import os

def download_single_video(video_url, output_directory, quality, audio_only=False):
    try:
        video = YouTube(video_url)
        
        if audio_only:
            audio_stream = video.streams.filter(only_audio=True).first()
            if audio_stream:
                audio_stream.download(output_directory)
                print(f"Downloaded audio: {video.title}")
            else:
                print(f"No audio stream found for {video.title}. Skipping...")
        else:
            video_streams = video.streams.filter(res=quality)
            
            if not video_streams:
                print(f"No matching stream found for {video.title} with quality {quality}. Skipping...")
                return
            
            video_stream = video_streams[0]
            
            video_stream.download(output_directory)
            print(f"Downloaded video: {video.title}")
    except Exception as e:
        print(f"Error downloading {video.title}: {e}")

def display_available_qualities(video):
    print("Available qualities:")
    for stream in video.streams.filter(type='video'):
        print(stream.resolution)

def download_playlist_with_quality(playlist_url, download_option, audio_only=False):
    try:
        user_name = input("Enter Folder Name (press Enter for default name - 'Youtube-Downloaded'): ")
        if not user_name:
            user_name = "Youtube-Downloaded"

        output_directory = os.path.join(os.path.expanduser("~"), "Downloads", user_name)
        os.makedirs(output_directory, exist_ok=True)

        if download_option == 'S':
            video_url = input("Enter the YouTube video URL: ")
            video = YouTube(video_url)

            display_available_qualities(video)
            quality = input("Enter the desired video quality: ").lower()

            download_single_video(video_url, output_directory, quality, audio_only)

        elif download_option == 'P':
            playlist_url = input("Enter the YouTube playlist URL: ")
            playlist = Playlist(playlist_url)
            print(f"Downloading playlist: {playlist.title}")

            video_url = playlist.video_urls[0]
            video = YouTube(video_url)

            display_available_qualities(video)
            quality = input("Enter the desired video quality: ").lower()

            for video_url in tqdm(playlist.video_urls, desc='Downloading Videos', unit='video'):
                download_single_video(video_url, output_directory, quality, audio_only)

            print("\nDownload complete.")
            print(f"Media files are saved in: {output_directory}")

        else:
            print("Invalid option. Please enter 'S' for a single video or 'P' for a playlist.")

    except KeyboardInterrupt:
        print("\nDownload interrupted. Goodbye!")

if __name__ == "__main__":
    banner = pyfiglet.figlet_format("GLITCH")
    print(banner)
    print("BY - GLITCH\nFree Palestine 🤍")
    print("-" * 50)

    download_option = input("Do you want to download a single video (enter 'S') or a playlist (enter 'P')? ").upper()
    playlist_url = ""
    
    audio_only_option = input("Do you want to download audio only? (y/n): ").lower() == 'y'

    download_playlist_with_quality(playlist_url, download_option, audio_only_option)
