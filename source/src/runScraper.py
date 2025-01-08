import os
from datetime import datetime
import instaloader
import sys
import logging
logging.getLogger("instaloader").setLevel(logging.CRITICAL) #<-- Still experimenting on the logging
curr_dir = os.path.dirname(__file__)
since_str = sys.argv[1]
until_str = sys.argv[2]
src_str = sys.argv[3]
SINCE = datetime.strptime(since_str, "%Y-%m-%d") # Convert to datetime format
UNTIL = datetime.strptime(until_str, "%Y-%m-%d")
L = instaloader.Instaloader() # Initiate Instaloader
# Filtering the scraping info, only the caption is needed
L.download_pictures = False
L.download_videos = False
L.download_video_thumbnails = False
L.save_metadata = False
L.save_metadata_json = False
# Still experimenting this error handler too lol
try:
    profile = instaloader.Profile.from_username(L.context, src_str)
except instaloader.exceptions.ProfileNotExistsException:
    print(f"Oops, an error occured. Make sure the Instagram ID is valid", file=sys.stderr)
    sys.exit(1)
except instaloader.exceptions.ConnectionException:
    print(f"Oops, an error occured. Please check your network connection", file=sys.stderr)
    sys.exit(1)
except instaloader.exceptions.LoginRequiredException:
    print(f"Oops, an error occured. Make sure the Instagram ID is not a private account", file=sys.stderr)
    sys.exit(1)
except instaloader.exceptions.PrivateProfileNotFollowedException:
    print(f"Oops, an error occured. Make sure the Instagram ID is not a private account", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Oops, an unexpected error occured. Sorry for the inconvenience (˶ᵕ︵ᵕ˶)", file=sys.stderr)
    sys.exit(1)
posts = profile.get_posts()
directory = os.path.join(curr_dir, "../scrape-results")
os.makedirs(directory, exist_ok=True)
# Using it's date and time of the posts for the filename because it's simpler to process :v
def save_caption(post):
    filename = os.path.join(directory, post.date_utc.strftime("%Y-%m-%d_%H-%M-%S_UTC.txt"))
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(post.caption if post.caption else "")
# Bug Workaround, Threshold for the scraper to get data older than the requested date
max_old_posts = 50
old_post_count = 0
# Filter the scraped posts that are in accordance with the requested date
for post in posts:
    if SINCE <= post.date_utc <= UNTIL:
        save_caption(post)
        old_post_count = 0  # Reset the older date counter if the post is in the requested date 
    elif post.date_utc < SINCE:
        old_post_count += 1
        if old_post_count >= max_old_posts:
            break
    else:
        old_post_count = 0 # Reset the older date counter for another use if all of the posts are filtered
