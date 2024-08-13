import json
import math
from pandas import DataFrame
import http_requests as http
# import connection
# import db_ctrl_estoque

#from '../../backend-estoque' import server

class EstoqueService:
    def __init__(self):
        
        self.produtos = None
    
    def formatarAcabados(self):
        self.produtos = http.getSaldoEstoque()
        
        df_controle = DataFrame(self.p_controle)
        df_controle = df_controle.groupby(['pkProduto', 'descricao'])[['saldo']].sum().reset_index()
        controle_json = json.loads(df_controle.to_json(orient='records'))
        
        df_tpa = DataFrame(self.produtos_tpa)
        df_tpa = df_tpa.apply(self.calcularSaldo, controle=controle_json, axis=1)
        _acabadosjson = json.loads(df_tpa.to_json(orient='records'))
        
        self.ctrl_acabados = _acabadosjson
        
    def formatarProdutosControle(self):
        self.formatarAcabados()
    
    
    def calcularSaldo(self, row, controle):
        if math.isnan(row['somaQuantidade']):
            row['somaQuantidade'] = 0
        row['somaQuantidade'] = (row['somaQuantidade'] * 100) * -1
        for prod in controle:
            if int(row['PK_PRODUTO']) == int(prod['pkProduto']):
                row['somaQuantidade'] = prod['saldo'] + row['somaQuantidade']
        return row
    
    def calcularSaldoSA(self, row, controle):
        row['totalProducao'] = row['totalProducao'] * -1
        if 'GR' in row['UN']:
            row['totalProducao'] = row['totalProducao'] / 1000
            row['UN'] = 'KG'
        for prod in controle:
            if int(row['IDX_PRODUTO']) == int(prod['idxProduto']):
                row['totalProducao'] = prod['saldo'] + row['totalProducao']
        return row
    
    def calcularSaldoSemiacabados(self, row):
        total_producao = 0
        for acab in self.produtos_tpa:
            if row['RDX_PRODUTO'] == acab['PK_PRODUTO']:
                total_producao = row['QUANTIDADE'] * acab['somaQuantidade']
        return total_producao
