
import praw
r = praw.Reddit('bot1')
for submission in r.subreddit('cats').new(limit=None):
    href = submission.url
    print(href)