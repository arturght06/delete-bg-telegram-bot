import requests

cookies = {
    'consent': 'eyJpcCI6IjE1NS4xMzMuNjguOTgiLCJvcmlnaW4iOiJyZW1vdmUuYmciLCJjb3VudHJ5IjoiUEwiLCJ0aW1lc3RhbXAiOjE2Nzg4MTA4OTA5ODQsIm9wdGlvbnMiOlsibWFuYWdlZCIsImZ1bmN0aW9uYWwiLCJwZXJmb3JtYW5jZSIsInRhcmdldGluZyJdLCJjb25zZW50Ijp7Im1hbmFnZWQiOmZhbHNlLCJmdW5jdGlvbmFsIjpmYWxzZSwicGVyZm9ybWFuY2UiOmZhbHNlLCJ0YXJnZXRpbmciOmZhbHNlfSwiY29va2llUG9saWN5VmVyc2lvbiI6IjIwMjItMDYtMDgifQ==',
    '_remove_bg_session': 'MJKTo6E273p2hoWsma8G%2B7n2yWhghqmaBVlRXVP6t86G3Zlmp7cC0xQxqg78vHAdNgwCOECCVaHjiwWh8dbk%2FVYyUcMd9hntj%2BET8LMLN4fXceNHkks9Dwcyt4zu2ZK4N6Lxa3dlU6KgCpu%2BMfGGDANMnoiSy1SJWtw39TYPiQBXrzEN8k%2BMiuHXOVDDHpauYWyiIQ1NXAOSot2Oc8bYIxOwxVwsq%2Bg%2BBXa9zgl3F%2BaDGJVQKf2sikqOLnN%2Fg6vKl0Z28cmaulpdUfOWLQgYXrx1bVB7BuNyJe2U%2BwPfgxJLSmXL3N5dgcZ7IbB7TC3a0lE53i7s0b5XzTaRuP%2FvaGsmkNTAWOgk5yoCr6ZG%2B9N0f%2Bc1OzCTofGPiXbRPij9g6X%2Fd9tb%2BHDIn3GAntNvz2jKQWPvIDxRIZ1wY%2BRed4U%2Fr6dBh48hCh3onle7FoeQSQvG0tKpH1mGYWCtdEam%2BlpEfpvRzgL5ddl2P%2BVbDpNTzO0E417ZpjiGI%2FLw%2B6iAIVdwxMg6qL4UxeUcMu907Ig%2BtTA6nBEJ5y3jnwWJOHHRGfqb9cJqok9AAjSVafEJUnN9FsE37wOh7uCuJlEGB1DlDPKsAUsAgNoS7h5HtvDC45aTpanXGMqfjovGRKGgTqP8zksKed6hp%2FeqyAKysuzh%2FeZigIi6leuvuWXFqBRJ8UJmsAGy6E%2FsD5R5VjIkFcA%3D%3D--WRCUsKiKHS5xS3za--Ct1bO%2FVqi3pbi1RSW1oPIg%3D%3D',
}

headers = {
    'authority': 'www.remove.bg',
    'accept': '*/*',
    'accept-language': 'ru',
    # 'content-length': '0',
    # 'cookie': 'consent=eyJpcCI6IjE1NS4xMzMuNjguOTgiLCJvcmlnaW4iOiJyZW1vdmUuYmciLCJjb3VudHJ5IjoiUEwiLCJ0aW1lc3RhbXAiOjE2Nzg4MTA4OTA5ODQsIm9wdGlvbnMiOlsibWFuYWdlZCIsImZ1bmN0aW9uYWwiLCJwZXJmb3JtYW5jZSIsInRhcmdldGluZyJdLCJjb25zZW50Ijp7Im1hbmFnZWQiOmZhbHNlLCJmdW5jdGlvbmFsIjpmYWxzZSwicGVyZm9ybWFuY2UiOmZhbHNlLCJ0YXJnZXRpbmciOmZhbHNlfSwiY29va2llUG9saWN5VmVyc2lvbiI6IjIwMjItMDYtMDgifQ==; _remove_bg_session=MJKTo6E273p2hoWsma8G%2BpWi7n2yWhghqmaBVlRXVP6t86G3Zlmp7cC0xQxqg78vHAdNgwCOECCVaHjiwWh8dbk%2FVYyUcMd9hntj%2BET8LMLN4fXceNHkks9Dwcyt4zu2ZK4N6Lxa3dlU6KgCpu%2BMfGGDANMnoiSy1SJWtw39TYPiQBXrzEN8k%2BMiuHXOVDDHpauYWyiIQ1NXAOSot2Oc8bYIxOwxVwsq%2Bg%2BBXa9zgl3F%2BaDGJVQKf2sikqOLnN%2Fg6vKl0Z28cmaulpdUfOWLQgYXrx1bVB7BuNyJe2U%2BwPfgxJLSmXL3N5dgcZ7IbB7TC3a0lE53i7s0b5XzTaRuP%2FvaGsmkNTAWOgk5yoCr6ZG%2B9N0f%2Bc1OzCTofGPiXbRPij9g6X%2Fd9tb%2BHDIn3GAntNvz2jKQWPvIDxRIZ1wY%2BRed4U%2Fr6dBh48hCh3onle7FoeQSQvG0tKpH1mGYWCtdEam%2BlpEfpvRzgL5ddl2P%2BVbDpNTzO0E417ZpjiGI%2FLw%2B6iAIVdwxMg6qL4UxeUcMu907Ig%2BtTA6nBEJ5y3jnwWJOHHRGfqb9cJqok9AAjSVafEJUnN9FsE37wOh7uCuJlEGB1DlDPKsAUsAgNoS7h5HtvDC45aTpanXGMqfjovGRKGgTqP8zksKed6hp%2FeqyAKysuzh%2FeZigIi6leuvuWXFqBRJ8UJmsAGy6E%2FsD5R5VjIkFcA%3D%3D--WRCUsKiKHS5xS3za--Ct1bO%2FVqi3pbi1RSW1oPIg%3D%3D',
    'origin': 'https://www.remove.bg',
    'referer': 'https://www.remove.bg/ru/upload',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'x-csrf-token': "SitHlXakrDbWBiN+VO7Nb/czGlJg5pFylPrEHeW+CARjqW969lFAKyRScwuoGfnNJX5076cGQjopsiSD8QidJQ==",
    'x-requested-with': 'XMLHttpRequest',
}

response = requests.post('https://www.remove.bg/ru/trust_tokens', cookies=cookies, headers=headers)
print(response.content)