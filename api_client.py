import requests

BASE_URL = "http://100.119.203.87:5000"

def get_filmes():
    try:
        res = requests.get(f"{BASE_URL}/filmes")
        return res.json() if res.status_code == 200 else []
    except:
        return []

def post_filme(dados):
    res = requests.post(f"{BASE_URL}/filmes", json=dados)
    return res.status_code == 201

def delete_filme(id_filme):
    res = requests.delete(f"{BASE_URL}/filmes/{id_filme}")
    return res.status_code == 200

def get_clientes():
    try:
        res = requests.get(f"{BASE_URL}/clientes")
        return res.json() if res.status_code == 200 else []
    except:
        return []

def post_cliente(dados):
    res = requests.post(f"{BASE_URL}/clientes", json=dados)
    return res.status_code == 201

def delete_cliente(id_cliente):
    res = requests.delete(f"{BASE_URL}/clientes/{id_cliente}")
    return res.status_code == 200

def get_locacoes():
    try:
        res = requests.get(f"{BASE_URL}/locacoes")
        return res.json() if res.status_code == 200 else []
    except:
        return []

def post_locacao(dados):
    res = requests.post(f"{BASE_URL}/locacoes", json=dados)
    return res.status_code == 201

def put_devolver(id_locacao):
    res = requests.put(f"{BASE_URL}/locacoes/{id_locacao}/devolver")
    return res.status_code == 200