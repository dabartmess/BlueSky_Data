import importlib.resources
import os
import sys

import atproto
from atproto import models

import session_reuse
from bsky_follows_util import get_followers

sp1_name = "Dingo Dave SP #"
sp1_description = "Automated Starter Pack by THE Dingo Dave\nFollow these folks, they're great!"
handle = 'thedingodave.substack.com'
password = 'i3g7-27cm-oezl-dfsm'

def create_SP_list(followers, handle, password):
    client = session_reuse.init_client(handle, password)
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

        aturi = create_SP(sp_list, sp_num, sp1_name, sp1_description, handle, password)
        print("SP #" + str(sp_num) + " has been created")
        #print("SP URI: ", spuri)
        bsky_post = create_post(aturi, sp_num, handle, password)
        break

        sp_num += 1
        curr += i

    print("Number of items: ", len(sp_items))
    #print(SP_items)

def create_post(aturi, sp_num, handle, password):
    client = session_reuse.init_client(handle, password)
    print("Entering create_post ")

    client = session_reuse.init_client(handle, password)
    # client = Client()
    # profile = client.login(handle, password)
    resolver = atproto.IdResolver()
    did = resolver.handle.resolve('thedingodave.substack.com')

    at_created = client.get_current_time_iso()

    print("Creating Post Record")

#    rkey_array = str(blob_ref).split(':')[3].split('/')[2].split("\'")
    rkey_array = str(aturi).split(':')[3].split('/')[2].split("\'")
    print("RKEY_ARRAY: ", rkey_array)
    rkey = rkey_array[0]
    print("RKEY: ", rkey)

    bsky_post = client.com.atproto.repo.put_record (
        data = {
            "repo": did,
            "rkey":rkey,
            "collection": "com.atproto.repo",
            "record": {
                "repo":      did,
                "collection":"com.atproto.repo",
                "record":    {
                    "createdAt":  at_created,
                    "name":       "Starter Pack by THE Dingo Dave, #" + str(sp_num),
                    "list":       aturi,
                    #           "feeds":      [aturi],
                    "description":"Automated Starter Packs by THE Dingo Dave, #" + str(sp_num),
                    "py_type":    "app.bsky.graph.starterpack"
                }
            }
        }
    )

    print("Bsky_Post: ", bsky_post)
    return bsky_post

def create_SP(sp_list, spnum, name, description, handle, password):
    client = session_reuse.init_client(handle, password)
    # client = Client()
    # profile = client.login(handle, password)
    resolver = atproto.IdResolver()
    did = resolver.handle.resolve('thedingodave.substack.com')

    at_created = client.get_current_time_iso()
    #print("Created: ", at_created)

    aturi = client.app.bsky.graph.list.create(repo=did,
                                              record=models.AppBskyGraphList.Record(
                                                created_at=at_created,
                                                name=name + str(spnum) + "_List",
                                                description=description,
                                                purpose="app.bsky.graph.defs#referencelist"))

    print("Adding people to list for starter pack")
    for follower in sp_list:
        listfoll = follower

        listrecuri = client.app.bsky.graph.listitem.create(
            repo=did,
            record={
                "subject": follower["did"],
                "list": aturi.uri,
                "created_at": at_created,
                "py_type": "app.bsky.graph.listitem"
            }
        )
        #print("List Rec URI: ", listrecuri.uri)

    print("AT-URI: ", aturi)
    rkey_array = str(aturi).split(':')[3].split('/')[2].split("\'")
    print("RKEY_ARRAY: ", rkey_array)
    rkey = rkey_array[0]
    print("RKEY: ", rkey)

    spuri = client.app.bsky.graph.starterpack.create(
        repo=did,
        rkey=rkey,
        record={
            "createdAt":  at_created,
            "name":       "Starter Pack by THE Dingo Dave, #" + str(spnum),
            "list":       aturi.uri,
            "feeds":      [],
            "description":"Automated Starter Packs by THE Dingo Dave, #" + str(spnum),
            "py_type":    "app.bsky.graph.starterpack"
        }
    )

    return spuri.uri

def main():
    bsky_handle = sys.argv[1]
    bsky_password = sys.argv[2]

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
       create_SP_list(all_followers, bsky_handle, bsky_password)


if __name__ == '__main__':
    main()