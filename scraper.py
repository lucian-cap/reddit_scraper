import praw
import pickle
import json

def scrape():
    '''Scrape Reddit for posts & comments from 20 subreddits'''

    #load our login info from a json file
    try:
        with open('login_info.json', 'r') as f:
            login_info = json.load(f)['reddit']
    except:
        print('Error opening login information file!')
        exit(1)

    #define the subreddits to scrape from land the number of posts to retrieve
    SUBREDDITS = ['gaming', 'pcmasterrace', 'DnD', 'EldenRing', 'pcgaming', 'books', 'horrorlit', 'kindle', 'Lovecraft', 'horrorwriters', \
                'movies', 'StarWars', 'lotr', 'dune', 'freefolk', 'ChatGPT', 'OpenAI', 'StableDiffusion', 'aiArt', 'aiwars']

    NUM_POSTS = 100

    #log into Reddit
    reddit = praw.Reddit(client_id = login_info['client_id'],
                        client_secret = login_info['client_secret'],
                        user_agent = login_info['user_agent'],
                        username = login_info['username'],
                        password = login_info['password'])

    posts = {}

    #for each subreddit in the list, get the top 100 posts over the last year
    for sub in SUBREDDITS:
        print(f'Scraping posts from {sub}...')
        
        posts[sub] = []
        for submission in reddit.subreddit(sub).top(time_filter = 'year', limit = NUM_POSTS):

            #if we can't get a author for the post just skip it
            if submission.author is None:
                continue
            
            content = {'author': submission.author.name ,
                       'title': submission.title,
                       'body': submission.selftext if len(submission.selftext) > 0 else None,
                       'comments': [{'author': c.author.name,
                                     'body': c.body} for c in submission.comments if isinstance(c, praw.models.Comment) 
                                                                                     and c.author is not None]}


            #for each post in the top 100, save it and a page of its comments
            posts[sub].append(content)

    #create a local copy to store outside of mattermost so there's a version to share if needed
    with open('./reddit_data.json', 'wb') as f:
        pickle.dump(posts, f)

if __name__ == '__main__':
    scrape()