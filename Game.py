import requests
import codecs
import warnings

session = requests.Session


def authorize():
    # read authentication information from separate file
    credentialsFile = open("tokens.txt", "r")
    bearer = credentialsFile.readline()
    credentialsFile.close()

    return {"Authorization": bearer}


def pullTweets(username):
    # endpoint
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?" \
          f"screen_name={username}" \
          "&count=200" \
          "&exclude_replies=true" \
          "&include_rts=false"

    userTweets = []  # to hold the text data from tweets

    # cycle through pages of 200 tweets (maximum # tweets possible to retrieve per request)
    newResults = True
    page = 1
    # repeats until all tweets retrieved or reaches api max of approx 3200 tweets
    while newResults:
        tweetFile = requests.get(url + f"&page={page}", headers=authorize()).json()
        if not tweetFile:  # if no tweets returned
            newResults = False
        for tweet in range(len(tweetFile)):
            # filter out tweets with media, links and tags to other twitter users
            if "https://t.co" not in tweetFile[tweet]["text"]:
                userTweets.append(tweetFile[tweet]["text"])
        page += 1

    return userTweets


print(pullTweets("kanyewest"))

# below code to fix unicode will give DepreciationWarning when encountering some escape sequences
# warnings.filterwarnings("ignore", category=DeprecationWarning)
# displays unicode characters properly
# new_str = codecs.unicode_escape_decode(response.text)[0]
# print(new_str)
