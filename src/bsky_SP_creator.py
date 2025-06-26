import importlib.resources
import json
import os
import pprint
import sys
from datetime import datetime
import atproto
from atproto import Client, models
import atproto_client
from atproto_client.models.app.bsky.actor.defs import ProfileView
from awscli.botocore.docs.utils import py_type_name

from bsky_follows_util import get_followers

sp1_name = "THE Dingo Dave"
sp1_description = ""
handle = 'thedingodave.substack.com'
password = 'i3g7-27cm-oezl-dfsm'


def create_SP_list(followers):
    sp_items = []
    max_sp = 150
    curr = 0
    i = 0
    sp_num = 1

    while curr < len(followers):
        sp_list = []

        for i in range(0, max_sp, 1):
            #print("Curr: ", curr, "i: ", i)
            if curr+i < len(followers):
                sp_list.append(followers[curr+i])
                sp_items.append(followers[curr+i])
                print("follower DID: ", followers[curr+i])

        print("SPNAME: ", sp1_name)
        create_SP(sp_list, sp_num, handle, password)
        break

        sp_num += 1
        curr += i

    print("Number of items: ", len(sp_items))
    #print(SP_items)

def create_SP(sp_list, spnum, listname, description):
    client = Client()
    profile = client.login(handle, password)
    print('Welcome,', profile.display_name)
    resolver = atproto.IdResolver()
    did = resolver.handle.resolve('thedingodave.substack.com')

    print("Entering create_SP")

    at_created = client.get_current_time_iso()
    print("Created: ", at_created)

    aturi = client.app.bsky.graph.list.create(repo=did,
                                              record=models.AppBskyGraphList.Record(
                                                created_at=at_created,
                                                name=listname + str(spnum) + "_List",
                                                description=description,
                                                purpose="app.bsky.graph.defs#referencelist"))

    print("Adding people to list for starter pack")
    for follower in sp_list:
        listfoll = follower

        listrecuri = client.app.bsky.graph.listitem.create(
            repo=did,
            record=models.AppBskyGraphListitem.Record(
                subject=follower["did"],
                list=aturi.uri,
                created_at=at_created,
                py_type="app.bsky.graph.listitem"
            )
        )
        print("List Rec URI: ", listrecuri.uri)

    print("AT-URI: ", aturi.uri)

    client.com.atproto.repo.create_record(
        data = {
            "collection": "app.bsky.graph.starterpack",
            "repo": did,
            "record": {
                "description": sp1_description,
                "name": sp1_name + str(spnum),
                "list": aturi.uri,
                "createdAt": at_created
            }
        }
    )

def main():
    sp1_name = sys.argv[1]
    sp1_description = sys.argv[2]
    bsky_handle = sys.argv[3]
    bsky_password = sys.argv[4]

    print(sp1_name, sp1_description)
    print(bsky_handle, bsky_password)

    all_followers = []
    try:
        os.remove("followers.json")
    except FileNotFoundError:
        print("Follower file not found")

    template_res = importlib.resources.files("bsky_SP_creator").joinpath("./bsky.properties")
    with importlib.resources.as_file(template_res) as template_file:
       all_followers = get_followers()
       # with open('followers.json') as followers_data:
       #     all_followers = json.load(followers_data)
       create_SP_list(all_followers)


if __name__ == '__main__':
    main()