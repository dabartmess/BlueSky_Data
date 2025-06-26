import importlib.resources
import json
import os
import pprint
import sys
from typing import TypedDict

import atproto
import atproto_client
from atproto_client.models.app.bsky.actor.defs import ProfileView
from awscli.botocore.docs.utils import py_type_name

from bsky_follows_util import get_followers

sp_name = ""
sp_description = ""
bsky_handle = ""
bsky_password = ""

def create_SP_list(followers):
    sp_items = []
    max_sp = 150
    curr = 0
    i = 0
    sp_num = 1

    while curr < len(followers):
        sp_list = []

        for i in range(0, max_sp, 1):
            print("Curr: ", curr, "i: ", i)
            if curr+i < len(followers):
                sp_list.append(followers[curr+i])
                sp_items.append(followers[curr+i])

        create_SP(sp_list, sp_num, bsky_handle, bsky_password)
        sp_num += 1
        curr += i

    print("Number of items: ", len(sp_items))
    #print(SP_items)

def create_SP(sp_list, num, author, pwd):
    print(author, pwd)
    client = atproto.Client()
    profile = client.login(author, pwd)
    print('Welcome,', profile.display_name)
    resolver = atproto.IdResolver()
    did = resolver.handle.resolve('thedingodave.substack.com')

    print("Entering create_SP")
    client.com.atproto.repo.create_record(
        description = atproto.models.AppBskyGraphStarterpack.Record.description(so_description),
        name = atproto.models.AppBskyGraphStarterpack.Record.name(so_name + str(num)),
        list = atproto.models.AppBskyGraphStarterpack.Record.list(sp_list),
        py_type = 'app.bsky.graph.starterpack'
    )

def main():
    sp_name = sys.argv[1]
    sp_description = sys.argv[2]
    bsky_handle = sys.argv[3]
    bsky_password = sys.argv[4]
    print(sp_name, sp_description)
    print(bsky_handle, bsky_password)

    all_followers = []
    try:
        os.remove("followers.json")
    except FileNotFoundError:
        print("Follower file not found")

    template_res = importlib.resources.files("bsky_SP_creator").joinpath("./bsky.properties")
    with importlib.resources.as_file(template_res) as template_file:
        all_followers = get_followers()
        create_SP_list(all_followers)


if __name__ == '__main__':
    main()