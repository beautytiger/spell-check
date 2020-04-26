import requests

# solve es cluster is red caused by shards UNASSIGNED, detailed reason is node left, data lossed forever.
# https://www.elastic.co/guide/en/elasticsearch/reference/6.8/cluster-reroute.html
ELASTICSEARCH_URL = "http://10.20.123.20:30066"
ELASTICSEARCH_USER = "elastic"
ELASTICSEARCH_PASSWORD = "xxx"
ELASTICSERACH_NODE_ID = "BJAmXx8DRdyoA6aEaPoDxw"

esurl = ELASTICSEARCH_URL

route_table_path = "/_cluster/state/routing_table"
reroute_path = "/_cluster/reroute"

basic_auth = (ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD)
es_node_id = ELASTICSERACH_NODE_ID


def main():
    resp = requests.get(esurl + route_table_path, auth=basic_auth)
    table = resp.json()
    indices = table["routing_table"]["indices"]
    for index, content in indices.items():
        shards = content["shards"]
        for shard, info in shards.items():
            for replicas in info:
                if replicas["primary"]:
                    if replicas["state"] == "UNASSIGNED":
                        print(index, shard)
                        data = {
                            "commands": [
                                {
                                    "allocate_empty_primary": {
                                        "index": index,
                                        "shard": shard,
                                        "node": es_node_id,
                                        "accept_data_loss": True,
                                    }
                                }
                            ]
                        }
                        reply = requests.post(
                            esurl + reroute_path, auth=basic_auth, json=data,
                        )
                        print(reply.status_code)
                        print(reply.text)


main()
