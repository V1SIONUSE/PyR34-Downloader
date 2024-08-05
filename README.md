![image](https://pbs.twimg.com/media/Fr5aQs9aEAASSLv.png)

# Bulk Media Downloader for Rule34

Welcome to the Media Downloader for Rule34! This Python script allows you to download media from the Rule34 API either by searching for posts with specific tags or by downloading a single post directly using its URL.

## Features

- **Download Media by Tags**: Fetches and downloads media based on specified tags and a limit.
- **Download Single Post**: Downloads a single media file using its post URL.
- **Organize Downloads**: Saves media into categorized folders based on media type (images, videos, gifs).
- **Progress Feedback**: Displays download progress and provides error handling.

## Requirements

Ensure you have Python installed on your system. The script requires the following libraries:

- `requests`: For making HTTP requests.
- `tqdm`: For displaying download progress.
- `colorama`: For colored terminal output.

If these libraries are not installed, the script will attempt to install them automatically.

## Installation

To use this script, you need to have Python and the required libraries installed. 

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. **Install Dependencies**:
    Run the script to install required libraries:
    ```bash
    python media_downloader.py
    ```

## Usage

Run the script using Python:

```bash
python media_downloader.py
```

You will be prompted with the following options:

1. **Download by Tags**:
   - Enter the tags for the media you want to download (separated by spaces).
   - Enter the number of posts to download or `all` for a maximum of 1000 posts.
   - Provide the output folder path where the media will be saved.

2. **Download Single Post**:
   - Provide the URL of the post you want to download.
   - Specify the output folder path where the media will be saved.

3. **Close Program**:
   - Exit the script.

## Example

### Download by Tags

```plaintext
Choose an option (1 - Download by tags, 2 - Download single post, 3 - Close program): 1
Enter tags (separated by spaces): cat cute
Enter number of posts to download (or 'all' for maximum): 10
Enter output folder path: ./downloads
```

### Download Single Post

```plaintext
Choose an option (1 - Download by tags, 2 - Download single post, 3 - Close program): 2
Enter post URL: https://rule34.xxx/index.php?page=dapi&s=post&q=index&id=123456&json=1
Enter output folder path: ./downloads
```

## Directory Structure

- Media files are organized into folders based on media type:
  - `images/` for `.jpg`, `.jpeg`, `.png`
  - `videos/` for `.mp4`, `.avi`, `.mkv`
  - `gifs/` for `.gif`

## Troubleshooting

- **Library Installation Issues**: Ensure you have internet access for library installation. If installation fails, manually install the missing libraries using `pip`.
- **API Errors**: Ensure the Rule34 API is available and accessible. Check the API documentation or community forums if you encounter issues.

## Contributing

Feel free to fork this repository and submit pull requests. For major changes or feature requests, please open an issue to discuss.
