import os
import sys
import time
import re
from urllib.parse import urlparse, parse_qs

# Check for required libraries and install them if necessary
try:
    import requests
    from tqdm import tqdm
    from colorama import Fore, Style
except ImportError:
    print("Required libraries are missing. Installing...")
    try:
        os.system("pip install requests tqdm colorama")
        import requests
        from tqdm import tqdm
        from colorama import Fore, Style
    except Exception as e:
        print(f"Error installing required libraries: {e}")
        sys.exit(1)

def download_single_post(post_url, output_folder):
    # Parse post ID from the URL
    parsed_url = urlparse(post_url)
    post_id = parse_qs(parsed_url.query).get('id')
    if not post_id:
        print(f"{Fore.RED}Invalid post URL.{Style.RESET_ALL}")
        return
    
    # Define API endpoint for single post
    api_url = f"https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&id={post_id[0]}&json=1"
    
    # Send request to API
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise exception for any error status codes
        posts = response.json()  # Parse JSON response
    except requests.RequestException as e:
        print(f"\n{Fore.RED}Error accessing API: {e}{Style.RESET_ALL}")
        return
    
    if not posts:
        print(f"{Fore.RED}No post found with ID: {post_id[0]}{Style.RESET_ALL}")
        return
    
    post = posts[0]
    media_url = post.get("file_url")
    if not media_url:
        print(f"\n{Fore.YELLOW}No media URL found for this post.{Style.RESET_ALL}")
        return
    
    # Determine media type
    media_type = "other"
    if media_url.endswith((".jpg", ".jpeg", ".png")):
        media_type = "images"
    elif media_url.endswith((".mp4", ".avi", ".mkv")):
        media_type = "videos"
    elif media_url.endswith((".gif")):
        media_type = "gifs"
    
    # Create tag folder if it doesn't exist
    tag_folder = os.path.join(output_folder, media_type)
    os.makedirs(tag_folder, exist_ok=True)
    
    # Download media
    media_name = os.path.basename(media_url)
    media_path = os.path.join(tag_folder, media_name)
    try:
        with open(media_path, "wb") as f:
            media_response = requests.get(media_url, stream=True)
            total_size = int(media_response.headers.get("content-length", 0))
            with tqdm(total=total_size, unit="B", unit_scale=True, desc=media_name, leave=False,
                      ascii=True, ncols=80, bar_format="{l_bar}{bar}{r_bar}") as pbar:
                for chunk in media_response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
    except Exception as e:
        print(f"\n{Fore.RED}Error downloading media: {e}{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.GREEN}Post downloaded successfully:{Style.RESET_ALL} {media_name}\n")

def download_media(tags, output_folder, limit):
    # Define API endpoint for posts
    api_url = "https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&json=1"
    
    # Define parameters for the API request
    params = {
        "tags": " ".join(tags),
        "limit": limit if limit != "all" else 1000,  # Hard limit of 1000 posts per request
        "json": 1  # Request JSON formatted response
    }
    
    # Send request to API
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise exception for any error status codes
        posts = response.json()  # Parse JSON response
    except requests.RequestException as e:
        print(f"\n{Fore.RED}Error accessing API: {e}{Style.RESET_ALL}")
        return
    
    num_posts = len(posts)
    print(f"\nFound {num_posts} posts matching the tags.\n")

    # Create tag folder if it doesn't exist
    tag_folder = os.path.join(output_folder, "_".join(tags))
    os.makedirs(tag_folder, exist_ok=True)
    
    print(f"Output folder: {tag_folder}\n")
    
    # Download media from posts
    downloaded = 0
    start_time = time.time()
    for post in tqdm(posts, desc=f"{Fore.GREEN}Downloading{Style.RESET_ALL}", unit="post"):
        try:
            # Access file_url attribute to find the media URL
            media_url = post.get("file_url")
                
            # If no URL found, skip this post
            if not media_url:
                print(f"\n{Fore.YELLOW}No media URL found for this post.{Style.RESET_ALL}")
                continue
            
            # Determine media type
            media_type = "other"
            if media_url.endswith((".jpg", ".jpeg", ".png")):
                media_type = "images"
            elif media_url.endswith((".mp4", ".avi", ".mkv")):
                media_type = "videos"
            elif media_url.endswith((".gif")):
                media_type = "gifs"
            
            # Create media type folder if it doesn't exist
            media_folder = os.path.join(tag_folder, media_type)
            os.makedirs(media_folder, exist_ok=True)
            
            media_name = os.path.basename(media_url)
            media_path = os.path.join(media_folder, media_name)
            
            # Download media
            with open(media_path, "wb") as f:
                media_response = requests.get(media_url, stream=True)
                total_size = int(media_response.headers.get("content-length", 0))
                with tqdm(total=total_size, unit="B", unit_scale=True, desc=media_name, leave=False,
                          ascii=True, ncols=80, bar_format="{l_bar}{bar}{r_bar}") as pbar:
                    for chunk in media_response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
            downloaded += 1
        except Exception as e:
            print(f"\n{Fore.RED}Error downloading media: {e}{Style.RESET_ALL}")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nDownloaded {downloaded} out of {num_posts} posts.")
    print(f"Time taken: {elapsed_time:.2f} seconds.\n")

def main():
    while True:
        option = input("Choose an option (1 - Download by tags, 2 - Download single post, 3 - Close program): ")

        if option == "1":
            tags = input("Enter tags (separated by spaces): ").split()
            limit = input("Enter number of posts to download (or 'all' for maximum): ")
            output_folder = input("Enter output folder path: ")
            download_media(tags, output_folder, limit)
        elif option == "2":
            post_url = input("Enter post URL: ")
            output_folder = input("Enter output folder path: ")
            download_single_post(post_url, output_folder)
        elif option == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please choose either 1, 2, or 3.")

if __name__ == "__main__":
    main()