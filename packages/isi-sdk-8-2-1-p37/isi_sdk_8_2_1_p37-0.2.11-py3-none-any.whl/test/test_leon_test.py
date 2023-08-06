import isi_sdk_8_2_1
from isi_sdk_8_2_1.rest import ApiException



configuration = isi_sdk_8_2_1.Configuration()
configuration.username = 'root'
configuration.password = 'RockfordF12'
configuration.host = 'https://192.168.1.21:8080'
configuration.verify_ssl = False

client = isi_sdk_8_2_1.ApiClient(configuration,pool_threads=5)
client.pool

api_instance = isi_sdk_8_2_1.ClusterApi(isi_sdk_8_2_1.ApiClient(configuration))
try:
    api_response = api_instance.get_cluster_nodes(timeout=30)
    print(api_response)
except ApiException as e:
    print("Exception when calling ClusterApi->get_cluster_nodes: %s\n" % e)
