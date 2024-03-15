# Youtube Downloader
# Download Videos Youtube And Playlists
# By - Abdelrahman Ghareeb (GLITCH)


try:
    import requests
    from pytube import Playlist, YouTube
    from tqdm import tqdm
    import pyfiglet
    from colorama import Fore, Style
    import os
except ImportError:
    print("Some required packages are missing. Installing them now...")
    try:
        import subprocess
        subprocess.call(["pip", "install", "pytube", "tqdm", "pyfiglet", "requests", "colorama"])
        from pytube import Playlist, YouTube
        from tqdm import tqdm
        import pyfiglet
        import os
        print("Packages installed successfully!")
    except Exception as e:
        print(f"Error installing required packages: {e}")
        exit(1)
        
######################################################################

def check_internet_connection():
    try:
        response = requests.get("http://www.google.com", timeout=3)
        response.raise_for_status()
        print(Fore.GREEN + "Internet connection established.")
        return True
    except requests.RequestException:
        print(Fore.RED + "No internet connection. Please check your network connection.")
        return False
    finally:
        print(Style.RESET_ALL)

######################################################################

try:
    global_variable = None
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
                video_streams = video.streams.filter(res=quality).first()
                if not video_streams:
                    print(f"No matching stream found for {video.title} with quality {quality}. Skipping...")
                    return
                video_stream = video_streams
                global global_variable
                global_variable = video_streams.filesize 
                with tqdm(total=global_variable, unit='B', unit_scale=True) as progress_bar:
                    progress_bar.update()
                    video_stream.download(output_directory)
                    progress_bar.close()
                print(f"Downloading video: {video.title}")
        except Exception as e:
            print(f"Error downloading {video.title}: {e}")

##################################################3

    def display_available_qualities(video):
        print("Available qualities:")
        for stream in video.streams.filter(type='video'):
            print(stream.resolution)

##################################################3

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
                print(f"Downloading Video Please wait... ({video.title})")
                download_single_video(video_url, output_directory, quality, audio_only)

            elif download_option == 'P':
                playlist_url = input("Enter the YouTube playlist URL: ")
                playlist = Playlist(playlist_url)
                print(f"Downloading playlist: {playlist.title}")
                video_url = playlist.video_urls[0]
                video = YouTube(video_url)
                display_available_qualities(video)
                quality = input("Enter the desired video quality: ").lower()
                for video_url in tqdm(playlist.video_urls, desc='Downloading Videos', unit='B', unit_scale=True):
                    download_single_video(video_url, output_directory, quality, audio_only)
                print("\nDownload complete.")
                print(f"Media files are saved in: {output_directory}")
            else:
                print("Invalid option. Please enter 'S' for a single video or 'P' for a playlist.")
        except KeyboardInterrupt:
            print("\nDownload interrupted. Goodbye!")
except:
    print("\nGoodbye!")

def main():
    if not check_internet_connection():
        return

    banner = pyfiglet.figlet_format("Xloder")
    print(banner)
    print("BY - GLITCH\nFree Palestine 🤍")
    print("-" * 50)

    while True:
        download_option = input("Do you want to download a single video (enter 'S') or a playlist (enter 'P')? ").strip().lower()
        if download_option in ['s', 'single']:
            download_option = 'S'
            break
        elif download_option in ['p', 'playlist']:
            download_option = 'P'
            break
        else:
            print("Invalid option. Please enter 'S' for a single video or 'P' for a playlist.")
    
    playlist_url = ""

    while True:
        audio_only_option = input("Do you want to download audio only? (y/n): ").strip().lower()
        if audio_only_option in ['y', 'n']:
            audio_only_option = audio_only_option == 'y'
            break
        else:
            print("Invalid option. Please enter 'y' for yes or 'n' for no.")

    download_playlist_with_quality(playlist_url, download_option, audio_only_option)

if __name__ == "__main__":
    main()

