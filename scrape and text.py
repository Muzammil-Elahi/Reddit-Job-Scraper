import praw
from twilio.rest import Client

# Reddit API credentials
client_id = 'insert here'
client_secret = 'insert here'
user_agent = ("Reddit Job Scraper by /u/work-life-nomad" "https://github.com/Muzammil-Elahi/Reddit-Job-Scraper/")

# Automate this and send text daily at midnight
from apscheduler.schedulers.background import BackgroundScheduler

# Twilio credentials
twilio_account_sid = 'insert here'
twilio_auth_token = 'insert here'
twilio_phone_number = 'insert here'
my_number = 'insert here'

# Initialize the Reddit API client
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

# Subreddit to scrape
subreddit_name = 'techjobs'
subreddit = reddit.subreddit(subreddit_name)

# Keywords to filter posts by job level
job_levels = ['entry-level', 'junior', 'assoicate','new grad','new graduate']

# Keyword to filter posts with "hiring" in the title
title_filter = 'hiring'

# Twilio client
twilio_client = Client(twilio_account_sid, twilio_auth_token)

def send_filtered_posts():
    # Iterate through the hot posts in the subreddit
    for submission in subreddit.hot(limit=10):  # Adjust the limit as needed
        title = submission.title
        selftext = submission.selftext
        combined_text = title.lower() + " " + selftext.lower()

        if any(level in combined_text for level in job_levels) and title_filter in title.lower():
            message = f'Title: {title}\nURL: {submission.url}'
            print(message)  # Print post details

            # Send the post details to your phone using Twilio
            twilio_client.messages.create(
                body=message,
                from_=twilio_phone_number,
                to=my_number
            )

# Schedule the job to run daily at midnight
scheduler = BackgroundScheduler()
scheduler.add_job(send_filtered_posts, 'interval', days=1, start_date='2023-01-01 00:00:00')
scheduler.start()

# Keep the script running
try:
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
