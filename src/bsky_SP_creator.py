import importlib.resources
import os
import sys
import atproto
from atproto import Client, models, client_utils

from bsky_follows_util import get_followers

sp1_name = "Test SP"
sp1_description = "Testing automated creation of lists"
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
                #print("follower DID: ", followers[curr+i])

        #print("SPNAME: ", sp1_name)
        spuri = create_SP(sp_list, sp_num, handle, password)
        #print("SP URI: ", spuri)
        create_post(spuri, sp_num)
        break

        sp_num += 1
        curr += i

    print("Number of items: ", len(sp_items))
    #print(SP_items)

def create_post(spuri, sp_num):
    print("SP uri: ", spuri)

    client = Client()
    profile = client.login(handle, password)
    print('Welcome,', profile.display_name)
    resolver = atproto.IdResolver()
    did = resolver.handle.resolve('thedingodave.substack.com')

    at_created = client.get_current_time_iso()

    post = client_utils.TextBuilder()
    post.text("Another comprehensive Starter Pack from my Follower List")
    post.link("Service Pack " + str(sp_num), spuri)
    post.build_facets()

    print("SP uri: ", spuri)
    spuri2 = spuri

    client.com.atproto.repo.create_record(
        data={
            "collection": "client.app.bsky.feed.post",
            "repo":      did,
            "record":    {
                "description":"Another in the list of automated Starter Packs, #" + str(sp_num),
                "list":       spuri2,
                "createdAt":  at_created
            }
        }
    )


def create_SP(sp_list, spnum, listname, description):
    client = Client()
    profile = client.login(handle, password)
    print('Welcome,', profile.display_name)
    resolver = atproto.IdResolver()
    did = resolver.handle.resolve('thedingodave.substack.com')

    at_created = client.get_current_time_iso()
    #print("Created: ", at_created)

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
            record={
                "subject": follower["did"],
                "list": aturi.uri,
                "created_at": at_created,
                "py_type": "app.bsky.graph.listitem"
            }
        )
        #print("List Rec URI: ", listrecuri.uri)

    #print("AT-URI: ", aturi.uri)

    spuri = client.app.bsky.graph.starterpack.create(
#        collection="app.bsky.graph.starterpack",
        repo=did,
        record={
            "description": sp1_description,
            "name": sp1_name + str(spnum),
            "list": aturi.uri,
            "createdAt": at_created,
            "py_type": "app.bsky.graph.starterpack"
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
       create_SP_list(all_followers)


if __name__ == '__main__':
    main()