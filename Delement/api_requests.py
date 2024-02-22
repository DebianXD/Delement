import requests

BASE_URL = 'https://elemsocial.com/System/API/'

def login(email, password):
    url = BASE_URL + 'Authorization.php?F=LOGIN'
    headers = {'User-Agent': 'Delement'}
    data = {'Email': email, 'Password': password}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        session_key = response.json()['Content']
        return session_key
    else:
        return None

def add_post(session_key, text, file=None, clear_metadata_img=False, censoring_img=False):
    url = BASE_URL + 'AddPost.php'
    headers = {'User-Agent': 'Delement', 'S-KEY': session_key['session_key']}
    data = {'Text': text, 'File': file, 'ClearMetadataIMG': clear_metadata_img, 'CensoringIMG': censoring_img}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()['Content']
    else:
        return None
