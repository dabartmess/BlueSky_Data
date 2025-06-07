import atproto
import importlib.resources
import requests

did = None
url = "https://bracket.us-west.host.bsky.network/xrpc/"
xurl = "com.atproto.repo.listRecords?repo = {did} & collection = app.bsky.graph.follow & limit = 100"
followers = []
handle = 'thedingodave.substack.com'
password = 'i3g7-27cm-oezl-dfsm'

def get_all_followers(did):
    """Retrieves all followers for a given user using the Bluesky API.

    Args:
        user_did: The DID (Decentralized Identifier) of the user.

    Returns:
        A list of follower objects.
    """

    cursor = None
    base_url = "app.bsky.graph.getFollowers"  # Public API URL

    while True:
        params = {
            "actor": did,
            "limit": 100,  # Or another limit
            "cursor":cursor
        }
        headers = {
            "Authorization":f"Bearer {password}"
        }

        # print(url+base_url)
        response = requests.get("https://public.api.bsky.app/xrpc/app.bsky.graph.getFollowers", params=params,
                                headers=headers)
        data = response.json()

#        print(data)
        followers.append(data["followers"])
        # print(len(followers), followers)
        cursor = data.get("cursor")

        if not cursor:
            break

    return followers


def main():
    all_followers = []

    template_res = importlib.resources.files("bsky_sp_creator").joinpath("./bsky.properties")
    with importlib.resources.as_file(template_res) as template_file:
        client = atproto.Client()
        profile = client.login(handle, password)
        print('Welcome,', profile.display_name)
        resolver = atproto.IdResolver()
        did = resolver.handle.resolve('thedingodave.substack.com')
        print(did)
        followers_response = client.get_followers(actor=did, limit=100)









































































































        cursor = followers_response.cursor
        all_followers.append(followers_response.followers)
        while cursor:
            for f in followers_response.followers:
                print(f.handle)
            followers_response = client.get_followers(actor=did, limit=100, cursor=cursor)
            all_followers.append(followers_response.followers)
        # all_followers = get_all_followers(did)
        print(len(all_followers))

if __name__ == '__main__':
    main()