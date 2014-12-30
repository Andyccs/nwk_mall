import requests

response = requests.post(
    'http://localhost:8000/o/token/',
    data={
        'grant_type': 'password',
        'username': 'admin',
        'password': 'admin',
        'client_id': '=4BNZQ5P03rnEWsHpxSBzyIf-Wt4-Hu!BOGF=cG!',
        'client_secret': 'dQbuPBIcoap0RG?zu38juA:xFw-8q4A-7wcq?n?ZPz9Lwp-RIdf3kRpw3?rwBDcb8rfRsEc01x?9igI3!Zx4r7l-H2nkOQGrDnNn-?DVgA?J=SLodW94Qdpx7xunCk9n'
    }
)

print(response.text)
