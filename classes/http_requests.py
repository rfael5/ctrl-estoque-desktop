import requests

def getSaldoEstoque():
    url = 'http://127.0.0.1:5000/get-produtos'
    response = requests.get(url)
    print(response.json())


def atualizarEstoque(atualizacao):
    url = 'http://127.0.0.1:5000/alterar-estoque'

    data = {
        "idProduto":atualizacao.idProduto,
        "descricao": atualizacao.descricao,
        "saldo": atualizacao.saldo,
        "unidade": atualizacao.unidade,
        "dataMov": atualizacao.dataMov,
        "tipoMov": atualizacao.tipoMov,
        "solicitante": atualizacao.solicitante,
        "motivo": atualizacao.motivo
    }

    response = requests.post(url, json=data)
    print(response.json())


def getHistoricoPeriodo(data_inicio, data_fim):
    url = f"""
        http://127.0.0.1:5000/historico-periodo?data_inicio=${data_inicio}&data_fim=${data_fim}
    """
    response = requests.get(url)
    print(response)


getHistoricoPeriodo(1722525660000, 1723409574000)