import requests
import random
import time
from tkinter import *
from tkinter import font

HEIGHT = 400
WIDTH = 600
MAX_ROUNDS = 3

choice = None
rounds = 0
score = 0


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


# sets guess based on which button was clicked
def update(username):
    global choice
    choice = username


def endRound(root, user1, user2, answer):
    # evaluate if correct
    global choice
    if choice is answer:
        resultLbl = Label(root, text="Correct!", fg="limegreen", bg="midnightblue",
                          font=("Helvetica", 32, font.BOLD))
        global score
        score += 1
    else:
        resultLbl = Label(root, text="Wrong!", fg="red3", bg="midnightblue",
                          font=("Helvetica", 32, font.BOLD))
    choice = None

    # display whether guess was correct
    resultLbl.pack()
    resultLbl.place(x=WIDTH / 2 - 120, y=HEIGHT / 2 - 50)

    # update number of rounds completed
    global rounds
    rounds += 1

    # determine if game should be over
    resultLbl.destroy()
    if rounds < MAX_ROUNDS:
        playRound(root, user1, user2)
    else:
        endGame(root)


def endGame(root):
    # display player's score
    endLbl = Label(root, text=f"You Scored {score}/{rounds}!", fg="turquoise2", bg="midnightblue",
                   font=("Helvetica", 32, font.BOLD))
    endLbl.pack()
    endLbl.place(x=WIDTH / 2 - 120, y=HEIGHT / 2 - 50)

    # button to terminate program when clicked
    endBtn = Button(root, text="End game", font=("Helvetica", 24, font.BOLD))
    endBtn.configure(command=lambda: sys.exit(0))
    endBtn.pack()
    endBtn.place(x=WIDTH / 2 - 65, y=HEIGHT / 2 + 60)


def selectTweet(user1, user2):
    # randomly picks 1 of 2 twitter accounts
    accountChoice = random.randint(1, 2)
    if accountChoice is 1:
        tweetList = user1
        answer = "elon"
    else:
        tweetList = user2
        answer = "kanye"
    # randomly picks tweet
    tweetIndex = random.randint(0, len(tweetList) - 1)
    tweetText = tweetList[tweetIndex]

    return tweetText, answer


def playRound(root, user1, user2):
    # pick random tweet
    tweetText, answer = selectTweet(user1, user2)

    # display tweet text
    tweetLbl = Label(root, text=tweetText, fg="white", bg="midnightblue", justify=CENTER, wraplength=300,
                     font=("Helvetica", 18))
    tweetLbl.pack()
    tweetLbl.place(x=WIDTH / 2 - 150, y=HEIGHT / 2 - 50)

    # button to pick elon as answer
    elonBtn = Button(root, text="Elon Musk", font=("Helvetica", 18))
    elonBtn.configure(command=lambda: [elonBtn.destroy(), kanyeBtn.destroy(), tweetLbl.destroy(), update("elon"),
                                       endRound(root, user1, user2, answer)])
    elonBtn.pack()
    elonBtn.place(x=WIDTH / 2 - 100, y=HEIGHT - 75)

    # button to pick kanye as answer
    kanyeBtn = Button(root, text="Kanye West", font=("Helvetica", 18))
    kanyeBtn.configure(
        command=lambda: [elonBtn.destroy(), kanyeBtn.destroy(), tweetLbl.destroy(), update("kanye"),
                         endRound(root, user1, user2, answer)])
    kanyeBtn.pack()
    kanyeBtn.place(x=WIDTH / 2 + 20, y=HEIGHT - 75)


def main():
    # create gui window
    root = Tk()
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.title("Who Tweeted That?")
    root.configure(bg="midnightblue")

    # opening text
    welcomeLbl = Label(root, text="Who Tweeted That?", fg="turquoise2", bg="midnightblue",
                       font=("Helvetica", 24, font.BOLD))
    welcomeLbl.pack()
    welcomeLbl.place(x=WIDTH / 2 - 120, y=HEIGHT / 2 - 50)

    # button to start playing game
    startBtn = Button(root, text="Start game", font=("Helvetica", 24, font.BOLD))
    startBtn.configure(command=lambda: [startBtn.destroy(), welcomeLbl.destroy(), playRound(root, elon, kanye)])
    startBtn.pack()
    startBtn.place(x=WIDTH / 2 - 65, y=HEIGHT / 2 + 60)

    # create lists of tweets
    elon = pullTweets("elonmusk")
    kanye = pullTweets("kanyewest")

    # deploy window
    root.resizable(0, 0)
    root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
    root.mainloop()


if __name__ == "__main__":
    main()
