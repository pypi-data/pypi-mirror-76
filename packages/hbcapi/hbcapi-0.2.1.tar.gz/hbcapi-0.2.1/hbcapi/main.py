import requests
import json
class access:
    def __init__(self, auth):
        ''' Constructor for this class. '''
        # Create some member animals
        self.auth = auth
        
 
 
    def poststats(self, guild, shard):
        headers = { "Authorization": str(self.auth), "Content-Type": "application/json" }
        r = requests.post("https://hydrogenbots.club/api/v1/servercount", headers=headers, data=json.dumps({ "shard": shard, "guild": guild }))
        return r.content

    def voters(self):
        headersforvoter = { "Authorization": str(self.auth) }
        r = requests.get("https://hydrogenbots.club/api/v1/voters", headers=headersforvoter)
        return r.content