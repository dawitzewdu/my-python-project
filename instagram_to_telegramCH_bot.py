import instaloader
import time
from telegram import Bot
import asyncio

# Instagram credentials
USERNAME = "username"
PASSWORD = "password"

# Telegram bot token and chat ID
TELEGRAM_TOKEN = 'token'
TELEGRAM_CHAT_ID = 'channelusername'  # Use @ followed by your channel's username

# Initialize Instaloader
L = instaloader.Instaloader()
L.login(USERNAME, PASSWORD)

# Initialize Telegram Bot
bot = Bot(token=TELEGRAM_TOKEN)

def get_latest_post(profile_name):
    profile = instaloader.Profile.from_username(L.context, profile_name)
    posts = profile.get_posts()
    latest_post = next(posts)
    return latest_post

async def send_post_to_telegram(post):
    caption = post.caption if post.caption else "No caption"
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=caption)
    await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=post.url)

async def main():
    profiles_to_check = ['mordless', 'ladymidulce']  # Add the profiles you want to check
    last_checked_posts = {profile: None for profile in profiles_to_check}

    while True:
        for profile in profiles_to_check:
            latest_post = get_latest_post(profile)
            if last_checked_posts[profile] is None or latest_post != last_checked_posts[profile]:
                await send_post_to_telegram(latest_post)
                last_checked_posts[profile] = latest_post
        await asyncio.sleep(3600)  # Check every hour

if __name__ == "__main__":
    asyncio.run(main())
