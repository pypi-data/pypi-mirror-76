import requests
import json


class Logpoint:
    def __init__(self, ip, username, secret_key):
        self.ip = ip
        self.username = username
        self.secret_key = secret_key

    def get_logpoint_data(self, data):
        api_path = "https://"+self.ip+"/getalloweddata"
        req_data = {'username': self.username,
                  'secret_key': self.secret_key,
                  "type": data }
        response = requests.post(api_path,data=req_data,verify=False)
        return response.json()

    def get_search_log(self, data):
        api_path = "https://"+self.ip+"/getsearchlogs"
        req_data = {'username': self.username,
                  'secret_key': self.secret_key,
                  "requestData": json.dumps(data) }
        response = requests.post(api_path, data=req_data, verify=False)
        return response

    def get_logs(self, search_id):
        queryData = {"search_id": search_id}
        all_results = []
        while(True):
            try:
                result = self.get_search_log(queryData)
                all_results.extend(result.json()['rows'])
                if(result.json()["final"]):
                    break
            except Exception as e:
                print(e)
                break
        return all_results

    def create_search_query(self, query, repo=[], time_range="Last 30 days"):
        queryData = {"timeout": 90,
                     "client_name": "gui",
                     "repos": repo,
                     "starts": {},
                     "limit": 50000,
                     "time_range": time_range,
                     "query": query }
        return queryData


if __name__ == "__main__":
    logpoint = Logpoint("10.45.9.141","admin","d2845bfc94d9f2f92bb6f92a9edb31ee")
    queryData = logpoint.create_search_query("| chart count() by device_ip")
    search = logpoint.get_search_log(queryData)
    search_id = search.json()["search_id"]
    print(logpoint.get_logs(search_id))
