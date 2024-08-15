import json
import requests

def getSaldoEstoque():
    try:
        url = 'http://127.0.0.1:5000/get-produtos'
        response = requests.get(url)
        return response.json()
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
    except ValueError as e:
        print(e)



def alterarEstoque(atualizacao):
    try:
        url = 'http://127.0.0.1:5000/alterar-estoque'
        json_data = json.dumps(atualizacao)
        data = json.loads(json_data)

        response = requests.post(url, json=data)
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
    except ValueError as e:
        print(e)


def atualizarSaldo(id, att_saldo):
    try:
        payload = {'id':id, 'movimentacao':att_saldo}
        res = requests.patch('http://127.0.0.1:5000/atualizar-saldo', json=payload)
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
    except ValueError as e:
        print(e)


def getHistoricoPeriodo(data_inicio, data_fim):
    try:
        url = f"""http://127.0.0.1:5000/historico-periodo?data_inicio={data_inicio}&data_fim={data_fim}"""
        response = requests.get(url)
        return response.json()
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
    except ValueError as e:
        print(e)








