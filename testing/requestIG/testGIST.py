import requests

cookies = {
    '_octo': 'GH1.1.633066599.1723576092',
    'logged_in': 'yes',
    'dotcom_user': 'bielbritob',
    'color_mode': '%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D',
    'cpu_bucket': 'md',
    'preferred_color_mode': 'dark',
    'tz': 'America%2FCuiaba',
    'gist_user_session': 'A0Iiktaf6lRi3LJMfaqUkBj-5W6nN6msQdHnBW4_lQFDdUML',
    '__Host-gist_user_session_same_site': 'A0Iiktaf6lRi3LJMfaqUkBj-5W6nN6msQdHnBW4_lQFDdUML',
    '_gh_sess': '8t1fyeZubUDoT9rZWqJO6acvbpuMyM7dh52gDcoZ8iHrujXaaAPF03uLw05H65liZt08wVq9wkQlzqs9OrZ9XgM7Nl%2FgW6UQ9DtJInsSB7qaq5FTR4YDZZ9elF9jn4%2BFf07eIJwLyX28n46eyvztDjIDRr9mznLJRymm5tCEa73s1yAWoOEItPb%2B1zSPtzneIAiZXPL%2BqOD4uVsUv6huPI6k0hAxccmCzUO%2FQGFLyYInxeIUW8S8UmntQ4RW9J0WIyrSIeEbujScniR%2BlJEUUjNSpUMTCCDLps26GEawOCIKYq3A47fhExgX3W4ZGXhD3fj9C7N5wNlHW9wuSvgfUx3nwQAWrBlrv2knWTsdI0ratfGu9HQ5Aeeg9RU%2BtIOpI%2FsIxjsnIBWIvs6l3TBlxMnG7g%2BBo%2F%2F7aEXjAqP2PdgvLX1ahU7ylDit710phIePEmrz1KuMGGCKGbDsedTIm51nDvPzIqjjlMoQr%2BgSj4staDgtyG5vd0cCaKrzWoAvKlUrfrB3etQUAfh99bCutObn6khmlDko9D8HYm5l5hcTqzGixUcAtyLlszgS%2FHbykwmOrr4rRtycl%2BVaNx4hXnLgftWH04rbPyC%2FUeCx7SdTyqO3HtJ%2B4cs0%2BP9lxdJt%2BiahAKIvws7nVhkJG8xxKkug2UlphV38BuZWRvfKI1zxrK0iZOb7wjCFje%2BY0BsFz3e0zIiSG%2B5csxBkPNE9EnXcCU4VhA6nB1qrg5VGS2W04fwMJ0zBGDi0C61dLKhrmcd9F5SM4Dkay39LB0iKiYocpKQpcMJu--9ITTu3nFIujWScxw--U67JN7VyXxKiPOp9uKj00Q%3D%3D',
}

headers = {
    'accept': 'text/html, application/xhtml+xml, application/json',
    'accept-language': 'pt-BR,pt;q=0.6',
    # 'cookie': '_octo=GH1.1.633066599.1723576092; logged_in=yes; dotcom_user=bielbritob; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; cpu_bucket=md; preferred_color_mode=dark; tz=America%2FCuiaba; gist_user_session=A0Iiktaf6lRi3LJMfaqUkBj-5W6nN6msQdHnBW4_lQFDdUML; __Host-gist_user_session_same_site=A0Iiktaf6lRi3LJMfaqUkBj-5W6nN6msQdHnBW4_lQFDdUML; _gh_sess=8t1fyeZubUDoT9rZWqJO6acvbpuMyM7dh52gDcoZ8iHrujXaaAPF03uLw05H65liZt08wVq9wkQlzqs9OrZ9XgM7Nl%2FgW6UQ9DtJInsSB7qaq5FTR4YDZZ9elF9jn4%2BFf07eIJwLyX28n46eyvztDjIDRr9mznLJRymm5tCEa73s1yAWoOEItPb%2B1zSPtzneIAiZXPL%2BqOD4uVsUv6huPI6k0hAxccmCzUO%2FQGFLyYInxeIUW8S8UmntQ4RW9J0WIyrSIeEbujScniR%2BlJEUUjNSpUMTCCDLps26GEawOCIKYq3A47fhExgX3W4ZGXhD3fj9C7N5wNlHW9wuSvgfUx3nwQAWrBlrv2knWTsdI0ratfGu9HQ5Aeeg9RU%2BtIOpI%2FsIxjsnIBWIvs6l3TBlxMnG7g%2BBo%2F%2F7aEXjAqP2PdgvLX1ahU7ylDit710phIePEmrz1KuMGGCKGbDsedTIm51nDvPzIqjjlMoQr%2BgSj4staDgtyG5vd0cCaKrzWoAvKlUrfrB3etQUAfh99bCutObn6khmlDko9D8HYm5l5hcTqzGixUcAtyLlszgS%2FHbykwmOrr4rRtycl%2BVaNx4hXnLgftWH04rbPyC%2FUeCx7SdTyqO3HtJ%2B4cs0%2BP9lxdJt%2BiahAKIvws7nVhkJG8xxKkug2UlphV38BuZWRvfKI1zxrK0iZOb7wjCFje%2BY0BsFz3e0zIiSG%2B5csxBkPNE9EnXcCU4VhA6nB1qrg5VGS2W04fwMJ0zBGDi0C61dLKhrmcd9F5SM4Dkay39LB0iKiYocpKQpcMJu--9ITTu3nFIujWScxw--U67JN7VyXxKiPOp9uKj00Q%3D%3D',
    'if-none-match': 'W/"c8dd728246c22a206b8d7d4a61dbff1d"',
    'priority': 'u=1, i',
    'referer': 'https://gist.github.com/bielbritob',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'turbo-visit': 'true',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
    'x-react-app-name': 'rails',
}

response = requests.get('https://gist.github.com/bielbritob/c4ed12178cbdaf33c4f8377e5d75025f', cookies=cookies, headers=headers)
