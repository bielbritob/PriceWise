import requests

cookies = {
    'vtex-search-anonymous': '3a3ee8bbef864fa182366d6c16b2de60',
    'checkout.vtex.com': '__ofid=96e47bc532ab48f9b278980f5ec7bbd5',
    'VtexWorkspace': 'master%3A-',
    'vtex-search-session': 'b16e127bb4f84c2491653ff537277e0c',
    'vtex_binding_address': 'mercantilnovaera.myvtex.com/',
    'vtex_session': 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjhkMDg0ZmViLTg2MDQtNDUwOS1iYjE4LTZlYzNlY2M0ZDM5ZSIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50LmlkIjpbXSwiaWQiOiJlNzRhNDNlOC1jNjcwLTQ2MTctYWM3Ni0wMmIwOGMyZmZkNjMiLCJ2ZXJzaW9uIjo1LCJzdWIiOiJzZXNzaW9uIiwiYWNjb3VudCI6InNlc3Npb24iLCJleHAiOjE3MzgzNzI1MjIsImlhdCI6MTczNzY4MTMyMiwianRpIjoiZjE0OWJmZjctODQwOC00ZTEzLTkzOTItYjAwZjhjYmRmNDE3IiwiaXNzIjoic2Vzc2lvbi9kYXRhLXNpZ25lciJ9.KTFBQweytaRo_wwfRwzDn1TcEbHnZy1bNvi_da8rhD-SF3Zzp1xkJgGr56o2XGjPuQjhsZNLvE4OXb45Zd69ZQ',
    'vtex_segment': 'eyJjYW1wYWlnbnMiOm51bGwsImNoYW5uZWwiOiIxIiwicHJpY2VUYWJsZXMiOm51bGwsInJlZ2lvbklkIjoiVTFjamJXVnlZMkZ1ZEdsc2JtOTJZV1Z5WVd4dmFtRXlPQT09IiwidXRtX2NhbXBhaWduIjpudWxsLCJ1dG1fc291cmNlIjpudWxsLCJ1dG1pX2NhbXBhaWduIjpudWxsLCJjdXJyZW5jeUNvZGUiOiJCUkwiLCJjdXJyZW5jeVN5bWJvbCI6IlIkIiwiY291bnRyeUNvZGUiOiJCUkEiLCJjdWx0dXJlSW5mbyI6InB0LUJSIiwiY2hhbm5lbFByaXZhY3kiOiJwdWJsaWMifQ',
    'CheckoutOrderFormOwnership': 'fRyVUn2+V+yAHuoVCI9oneYQ0ZInsiOZ3hMlPwr82wWXp8tc9tg9LmAtfcGjm+Ry1Me7iPdnezPhMnFKUxBZ7TcWEna28vaEVj0Dc8pVLmJvN+buRsbErjbtp7nXte8XjnjT+mhhACYYNxXu0RyR3ssioU5+KraRJd88fJOG4gt8eRK3uHonp/O7O5PW6PL7lKcRg8ZFRQUq3GyF7CgZa2Ad2SBpqcuwhcLfNpgqlR6LpyadLJBERTqAbNIRrPaCLq0ingSm/ew6w+MSg4qXeUOMdP7jLcAqv1ifko9aObE=',
    'biggy-search-history': 'leite%20uht%2CAbacaxi%20P%C3%A9rola%2Ccaf%C3%A9%20500g',
    'janus_sid': '01294fb0-89ec-4559-a7d3-bc2bc10fd8cc',
}

headers = {
    'accept': '*/*',
    'accept-language': 'pt-BR,pt;q=0.8',
    'content-type': 'application/json',
    # 'cookie': 'vtex-search-anonymous=3a3ee8bbef864fa182366d6c16b2de60; checkout.vtex.com=__ofid=96e47bc532ab48f9b278980f5ec7bbd5; VtexWorkspace=master%3A-; vtex-search-session=b16e127bb4f84c2491653ff537277e0c; vtex_binding_address=mercantilnovaera.myvtex.com/; vtex_session=eyJhbGciOiJFUzI1NiIsImtpZCI6IjhkMDg0ZmViLTg2MDQtNDUwOS1iYjE4LTZlYzNlY2M0ZDM5ZSIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50LmlkIjpbXSwiaWQiOiJlNzRhNDNlOC1jNjcwLTQ2MTctYWM3Ni0wMmIwOGMyZmZkNjMiLCJ2ZXJzaW9uIjo1LCJzdWIiOiJzZXNzaW9uIiwiYWNjb3VudCI6InNlc3Npb24iLCJleHAiOjE3MzgzNzI1MjIsImlhdCI6MTczNzY4MTMyMiwianRpIjoiZjE0OWJmZjctODQwOC00ZTEzLTkzOTItYjAwZjhjYmRmNDE3IiwiaXNzIjoic2Vzc2lvbi9kYXRhLXNpZ25lciJ9.KTFBQweytaRo_wwfRwzDn1TcEbHnZy1bNvi_da8rhD-SF3Zzp1xkJgGr56o2XGjPuQjhsZNLvE4OXb45Zd69ZQ; vtex_segment=eyJjYW1wYWlnbnMiOm51bGwsImNoYW5uZWwiOiIxIiwicHJpY2VUYWJsZXMiOm51bGwsInJlZ2lvbklkIjoiVTFjamJXVnlZMkZ1ZEdsc2JtOTJZV1Z5WVd4dmFtRXlPQT09IiwidXRtX2NhbXBhaWduIjpudWxsLCJ1dG1fc291cmNlIjpudWxsLCJ1dG1pX2NhbXBhaWduIjpudWxsLCJjdXJyZW5jeUNvZGUiOiJCUkwiLCJjdXJyZW5jeVN5bWJvbCI6IlIkIiwiY291bnRyeUNvZGUiOiJCUkEiLCJjdWx0dXJlSW5mbyI6InB0LUJSIiwiY2hhbm5lbFByaXZhY3kiOiJwdWJsaWMifQ; CheckoutOrderFormOwnership=fRyVUn2+V+yAHuoVCI9oneYQ0ZInsiOZ3hMlPwr82wWXp8tc9tg9LmAtfcGjm+Ry1Me7iPdnezPhMnFKUxBZ7TcWEna28vaEVj0Dc8pVLmJvN+buRsbErjbtp7nXte8XjnjT+mhhACYYNxXu0RyR3ssioU5+KraRJd88fJOG4gt8eRK3uHonp/O7O5PW6PL7lKcRg8ZFRQUq3GyF7CgZa2Ad2SBpqcuwhcLfNpgqlR6LpyadLJBERTqAbNIRrPaCLq0ingSm/ew6w+MSg4qXeUOMdP7jLcAqv1ifko9aObE=; biggy-search-history=leite%20uht%2CAbacaxi%20P%C3%A9rola%2Ccaf%C3%A9%20500g; janus_sid=01294fb0-89ec-4559-a7d3-bc2bc10fd8cc',
    'priority': 'u=1, i',
    'referer': 'https://www.supernovaera.com.br/leite%20uht?_q=leite%20uht&map=ft',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
}

params = {
    'workspace': 'master',
    'maxAge': 'medium',
    'appsEtag': 'remove',
    'domain': 'store',
    'locale': 'pt-BR',
    '__bindingId': '8b389c2d-2c18-4726-b45e-b6b134af62da',
    'operationName': 'productSuggestions',
    'variables': '{}',
    'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"0ef2c56d9518b51f912c2305ac4b07851c265b645dcbece6843c568bb91d39ff","sender":"vtex.store-resources@0.x","provider":"vtex.search-graphql@0.x"},"variables":"eyJwcm9kdWN0T3JpZ2luVnRleCI6ZmFsc2UsInNpbXVsYXRpb25CZWhhdmlvciI6ImRlZmF1bHQiLCJoaWRlVW5hdmFpbGFibGVJdGVtcyI6dHJ1ZSwiYWR2ZXJ0aXNlbWVudE9wdGlvbnMiOnsic2hvd1Nwb25zb3JlZCI6dHJ1ZSwic3BvbnNvcmVkQ291bnQiOjIsInJlcGVhdFNwb25zb3JlZFByb2R1Y3RzIjpmYWxzZSwiYWR2ZXJ0aXNlbWVudFBsYWNlbWVudCI6ImF1dG9jb21wbGV0ZSJ9LCJvcmRlckJ5IjoiT3JkZXJCeVNjb3JlREVTQyIsImZ1bGxUZXh0IjoibGVpdGUgdWh0IiwiY291bnQiOjQsInNoaXBwaW5nT3B0aW9ucyI6W10sInZhcmlhbnQiOm51bGx9"}',
}

response = requests.get('https://www.supernovaera.com.br/_v/segment/graphql/v1', params=params, cookies=cookies, headers=headers)