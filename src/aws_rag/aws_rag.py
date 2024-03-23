import requests
import json
#delete(url, args)	Sends a DELETE request to the specified url
#get(url, params, args)	Sends a GET request to the specified url
#head(url, args)	Sends a HEAD request to the specified url
#patch(url, data, args)	Sends a PATCH request to the specified url
#post(url, data, json, args)	Sends a POST request to the specified url
#put(url, data, args)	Sends a PUT request to the specified url
#request(method, url, args)	Sends a request of the specified method to the specified url

stage = 'prod'
host = f"https://dsft6rxl8j.execute-api.us-east-1.amazonaws.com/{stage}"

#host = "http://127.0.0.1:3000"
def get_user_name(access_token):
    
    headers = {'Authorization': access_token, "ContentType":"application/json"}
    response = requests.put(f'{host}/content/manage', headers=headers, data=json.dumps({"code":access_token, "func":"username", "source":"next"}))
    
    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        return response
    
    return json.loads(response.text)

def get_collections(access_token):
    
    headers = {'Authorization': access_token, 'ContentType':"application/json"}
    response = requests.put(f'{host}/content/manage', headers=headers, data=json.dumps({"access_token":access_token,"func":"get_collections"}))
    
    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        return response
    return json.loads(response.text)

def get_access_url(file_name, access_token, openai_api_key, model):
    
    headers = {'Authorization': access_token, 'ContentType':"application/json"}
    response = requests.put(f'{host}/content/upload', headers=headers, data=json.dumps({"access_token":access_token,"file_name":file_name, "apitoken":openai_api_key, "model":model}))
    
    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        return response
    
    return json.loads(response.text)

def get_user_files(access_token):
    
    headers = {'Authorization': access_token, 'ContentType':"application/json"}
    response = requests.put(f'{host}/content/manage', headers=headers, data=json.dumps({"code":access_token,"func":"get_files"}))
    
    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        return response
    return json.loads(response.text)

def create_collection(access_token, lombda_key, collection, source, model):
    
    headers = {'Authorization': access_token, 'ContentType':"application/json"}
    response = requests.put(f'{host}/content/merge', headers=headers, data=json.dumps({"code":access_token, "collection":collection,"source":source,"model":model, "attempts":0}))
    
    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        return response
    
    return json.loads(response.text)

def delete_user_files(access_token, db_type, source):
    
    if db_type.lower() not in ["file","collection"]:
        return {"result":"bad db_type parameter"}
    
    func = ""
    if db_type.lower() == "file":
        func = "delete_file"
    elif db_type.lower() == "collection":
        func = "delete_collection"
        
    headers = {'Authorization': access_token, 'ContentType':"application/json"}
    response = requests.put(f'{host}/content/manage', headers=headers, data=json.dumps({"code":access_token, "func":func, "source":source}))
    
    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        return response
    
    return json.loads(response.text)

# Function to upload file using a presigned URL
def upload_file_to_s3(presigned_url, file_path):
    with open(file_path, 'rb') as f:
        response = requests.put(presigned_url, data=f)
        print(response)
        return response

def ask_qa(question, file_name, access_token, lombda_key, openai_api_key, model, db_type, chat_model, num_results: int = 3):
    
    #removed api from gateway for testing
    
    headers = {
        'Authorization': access_token, 
        'ContentType':'application/json', 
        'x-api-key' : lombda_key}
    
    response = requests.put(f'{host}/content/query', 
                            headers=headers, 
                            data=json.dumps({
                                "query":question,
                                "code":access_token,
                                "db":file_name, 
                                "db_type":db_type,
                                "apitoken":openai_api_key, 
                                "model":model, 
                                "num_results":num_results, 
                                "func":"qa",
                                "chat_model":chat_model}))
    
    print(response.status_code)
    print(response.text)
    
    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        return response
    
    return json.loads(response.text)