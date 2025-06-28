import importlib.resources
import os
import sys
import atproto
import atproto_client.models.blob_ref
from atproto import Client, models, client_utils
from atproto_client.models.blob_ref import BlobRef
import atproto_core
from bsky_follows_util import get_followers

sp1_name = "Dingo Dave SP #"
sp1_description = "Automated Starter Pack by THE Dingo Dave\nFollow these folks, they're great!"
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
        bsky_post = create_post(spuri, sp_num)
        break

        sp_num += 1
        curr += i

    print("Number of items: ", len(sp_items))
    #print(SP_items)

def create_post(spuri, sp_num):
    print("Entering create_post ")

    client = Client()
    profile = client.login(handle, password)
    resolver = atproto.IdResolver()
    did = resolver.handle.resolve('thedingodave.substack.com')
    img_bytes = None
    img_path = "/home/dabartmess/Dropbox/Protest/BlueSkyLiberty.jpg"

    at_created = client.get_current_time_iso()

    # ref2 = client.send_image(text="BlueSky Liberty", image=img_data, image_alt="BlueSky Liberty Logo")
    # print("Ref: ", ref2)
    print("Creating embeds")

    with open(img_path, "rb") as f:
        img_data = f.read()
    blob_ref = atproto_client.models.blob_ref.BlobRef(
        alt="BlueSky Liberty Wave",
        mime_type="image/jpeg",
        ref=spuri,
        maxSize=1000000,
        size=190055,
        py_type="blob"
    )

    print("Blob: ", blob_ref)
    embed =  [
        atproto_client.models.AppBskyGraphStarterpack.FeedItem(
            py_type = "app.bsky.graph.starterpack#feedItem",
            uri = spuri
        ),
        atproto_client.models.AppBskyEmbedImages.Image(
            alt="THEDingoDave.substack.com BlueSky Liberty",
            image=blob_ref,
            py_type="app.bsky.embed.images#image"
        )
    ]
    print("Creating Post Record")

    rkey_array = str(blob_ref).split(':')[3].split('/')[2].split("\'")
    print("RKEY_ARRAY: ", rkey_array)
    rkey = rkey_array[0]
    print("RKEY: ", rkey)

    bsky_post = client.app.bsky.feed.post.create(
        repo = did,
        rkey = rkey,
        record = {
            "text":       "Starter Pack by THE Dingo Dave, #" + str(sp_num),
            "description":"Automated Starter Packs by THE Dingo Dave, #" + str(sp_num),
            "createdAt":  at_created,
            "embed":      embed,
            "py_type":    "app.bsky.feed.post"
        }
    )
    print("Bsky_Post: ", bsky_post)
    return bsky_post

def create_SP(sp_list, spnum, listname, description):
    client = Client()
    profile = client.login(handle, password)
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