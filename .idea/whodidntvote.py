
# Who Commented and didn't bother to vote?
# v.1.0 by @slobberchops
# February 2023

from beem import Hive
from beem.vote import ActiveVotes
from datetime import datetime, timedelta
from beem.comment import Comment
from beem.exceptions import ContentDoesNotExistsException
from beem.account import Account
import random
from beem.instance import set_shared_blockchain_instance
import os

# Enables ANSI colors to be used on Wintel platform
os.system("")

hivenodes = ["https://api.hive.blog", "https://api.deathwing.me"]
activenode = random.choice(hivenodes)
hive = Hive(node=activenode)
set_shared_blockchain_instance(hive)

myaccount = "slobberchops"
sAccount = Account(myaccount)

# ---------------------------------------------------------
# StdOut console colour definitions
class bcolors:
     HEADER = '\033[95m'
     BLUE = '\033[94m'
     CYAN = '\033[96m'
     GREEN = '\033[92m'
     YELLOW = '\033[93m'
     VIOLET = '\033[35m'
     RED = '\033[91m'
     END = '\033[0m'
     BOLD = '\033[1m'
     UNDERLINE = '\033[4m'
# ---------------------------------------------------------
# --------------------------------------------------------------------------------------------
# Function getlastpost (account)
# Returns the most recent post of the account in 'myaccount'
# and bpost which determines of there are any valid posts to vote


def getlastpost (account):

    c_list = {}
    mypost = ""
    bpost = False

    try:
        for post in map(Comment, account.history_reverse(stop=stop, only_ops=['comment'], use_block_num=False)):

            if post.permlink in c_list:
                continue
            try:
                post.refresh()
            except ContentDoesNotExistsException:
                continue
            c_list[post.permlink] = 1

            # Skip anything that is NOT a post and is NOT pending rewards
            if not post.is_comment() and post.is_pending():
                if mypost == "":
                    mypost=post
                bpost = True
    except:
        print(bcolors.RED + "HIVE Blockchain timeout error, recalibrating..." + bcolors.END)

    return bpost, mypost
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# Function get_commenters (post_url)
# Returns a list of commenters that commented on the post (post_url)


def get_commenters (post_url):

    hive = Hive()
    post = Comment(post_url, hive_instance=hive)
    commenters = post.get_replies()
    commenter_names = [commenter["author"] for commenter in commenters]
    return commenter_names

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# Function takes the commenters list and cross-references it against
# table data extracted using the ActiveVotes beem.vote method
# displays the data of the 'offending' non-voters for all to see


def get_nonvoters (commenters, post_permlink, title):

    print(bcolors.CYAN + f"   Summary for Post: '{title}'"+ bcolors.END)
    print(bcolors.CYAN + f'   Authored by: @{myaccount}' + bcolors.END)
    print(bcolors.CYAN + f"   -= Who commented and didn't vote? =-" + bcolors.END)
    print('   ------------------------------------------------------------------')
    voters = []
    votes = ActiveVotes(post_permlink, blockchain_instance=hive)

    for votees in votes:
        string = str(votees)
        start_delimiter = "|"
        end_delimiter = ">"
        start_index = string.find(start_delimiter) + len(start_delimiter)
        end_index = string.find(end_delimiter)
        voterdata = string[start_index: end_index].strip()
        voters.append(voterdata)

    for commentee in commenters:
        if commentee in voters:
            print(bcolors.GREEN + f"      @{commentee} did vote" + bcolors.END)
        else:
            print(bcolors.RED + f"      @{commentee} did NOT vote" + bcolors.END)

    return
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# Main ###


stop = datetime.utcnow() - timedelta(days=7)

bpost, post = getlastpost(sAccount)

if bpost:
    print(f'Yes.. a post found = {post.title}')
    commenters = get_commenters(post)
    get_nonvoters(commenters, post, post.title)

else:
    print("No posts found")

os.system('pause')

