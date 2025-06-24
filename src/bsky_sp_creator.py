import io
import sys
import os

import atproto
import atproto_client
import importlib.resources
import json

from typing import TypedDict, Any

from atproto_client.models.app.bsky.actor.defs import ProfileView

show = False
did = None
url = "https://bracket.us-west.host.bsky.network/xrpc/"
xurl = "com.atproto.repo.listRecords?repo = {did} & collection = app.bsky.graph.follow & limit = 100"
followers = []
handle = 'thedingodave.substack.com'
password = 'i3g7-27cm-oezl-dfsm'
client = None
follow_data = {}

# noinspection PyTypedDict
class FollowData(TypedDict):
    did: str
    handle: str
    display_name: str
    description: str
    verification: str
    blocked_by: bool
    blocking: bool
    muted: bool

def insert_data(profileview: ProfileView):
    follow_data: FollowData = FollowData()
    return follow_data

def get_followers():
    cursor=None
    client = atproto.Client()
    profile = client.login(handle, password)
    print('Welcome,', profile.display_name)
    resolver = atproto.IdResolver()
    did = resolver.handle.resolve('thedingodave.substack.com')
    print(did)
    followers_response = client.get_followers(actor=did, cursor=cursor, limit=100)
    follow_no = 0
    follower_data=[]

    cursor = followers_response.cursor

    for follower in followers_response.followers:
        follow_no += 1
        foll_data = {
            "did":         follower["did"],
            "handle":      follower["handle"],
            "display_name":follower["display_name"]
            # "verification":follower["verification"]["verifiedStatus"]
        }

        follower_data.append(foll_data)

        if follow_no % 1000 == 0:
            print("Fetched: ", follow_no, ": ", cursor)

    while cursor:
        try:
            followers_response = client.get_followers(actor=did, cursor=cursor, limit=100)
            cursor = followers_response.cursor
            for follower in followers_response.followers:
                follow_no += 1
                # if follower["verification"]:
                #     print("Verified")

                foll_data = {
                    "did":         follower["did"],
                    "handle":      follower["handle"],
                    "display_name":follower["display_name"]
                    # "verification":follower["verification"]["verifiedStatus"]
                }

                follower_data.append(foll_data)

                if follow_no % 1000 == 0:
                    print("Fetched: ", follow_no, ": ", cursor)

        except  atproto_client.exceptions.NetworkError:
            print("End of Stream")
            break

    with open("followers.json", "a+t") as f_out:
        json.dump(follower_data, f_out, indent=2)

    print("Number of Followers: ", follow_no)


def get_following():
    cursor = None
    client = atproto.Client()
    profile = client.login(handle, password)
    print('Welcome,', profile.display_name)
    resolver = atproto.IdResolver()
    did = resolver.handle.resolve('thedingodave.substack.com')
    follows = []

    print(did)

    follows_response = client.get_follows(actor=did, cursor=cursor, limit=100)
    follow_no = 0

    cursor = follows_response.cursor

    for follower in follows_response.follows:
        follows.append({"did":follower["did"], "handle":follower["handle"]})
                        # "verified":follower["verification"]["verifiedStatus"]})
        follow_no += 1

    if follow_no % 1000 == 0:
        print("Fetched: ", follow_no, ": ", cursor)

    while cursor:
        follows_response = client.get_follows(actor=did, cursor=cursor, limit=100)
        cursor = follows_response.cursor
        # print(cursor)
        for follower in follows_response.follows:
            follows.append({"did":follower["did"], "handle":follower["handle"]})
            follow_no += 1

            if follow_no % 1000 == 0:
                print("Fetched: ", follow_no, ": ", cursor)

    with open("follows.json", "a+t") as f_out:
        json.dump(follows, f_out, indent=2)

    print("Number of Follows: ", follow_no)

def comparefollowstofollowers():
    follows = []
    follower_remove = []

    with open('follows.json', "rt") as follows_data:
        follows = json.load(follows_data)

    with open('followers.json') as followers_data:
        followers = json.load(followers_data)

    find_remove = True
    for follows_item in follows:
        #print(followers_item)

        for followers_item in followers:
            if followers_item["did"] == follows_item["did"]:
                find_remove = False

        if find_remove:
            followers_remove.append(follows_item)

    pprint(followers_remove)

def main():
    all_followers = []
    try:
        os.remove("follows.json")
        os.remove("followers.json")
    except FileNotFoundError:
        print("Follow files not found")

    template_res = importlib.resources.files("bsky_sp_creator").joinpath("./bsky.properties")
    with importlib.resources.as_file(template_res) as template_file:
        get_followers()
        get_following()

    comparefollowstofollowers()

if __name__ == '__main__':
    main()