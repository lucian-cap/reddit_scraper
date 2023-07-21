# Basic Reddit Scraper

This is a basic project to scrape posts & comments from some hardcoded subreddits using the Python Reddit API Wrapper package.

## How to use

Running `scraper.py` will require a local `login_info.json` file containing your login information for Reddit, formatted in the following manner, where `STR` should be replaced with your info:

```JSON
{
    "reddit": {
      "client_id": STR,
      "client_secret": STR,
      "user_agent": STR,
      "username": STR,
      "password": STR
    }
  }
```

Instructions for how to obtain this info can be found at [PRAW](https://praw.readthedocs.io/en/stable/getting_started/quick_start.html).

The script will output the scraped posts & comments to a file called `reddit_data.json`, which follows this format:

```JSON
{
    "subreddit_name": [{
        "author": STR,
        "title": STR,
        "body": STR,
        "comments": [{
            "author": STR,
            "body": STR
        }, ...]
    }, ...],
    ...
}
```

Where the name of a subreddit will appear as the key, whose value is a list of posts. The top level "author", "title", "body" and "comments" refer to attributes of a post in that subreddit, with 100 posts appearing at most per subreddit. The "comments" attribute contains a list of comments for that post, where "author" and "body" at this level refer to the author and content of the comment. 

## Info

The "body" of the post and comment will both appear as markdown content. If the body of a post does not contain any text, e.g. a link or image post, then the body will be `None`. Additionally, if a comment doesn't have a author (likely deleted or banned) then it is skipped and will not appear.
