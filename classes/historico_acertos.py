from abc import abstractmethod
from datetime import datetime, timezone
import db_ctrl_estoque


class HistoricoAcertos():
    def __init__(self, data_inicio, data_final, tabela):
        self.data_inicio = data_inicio
        self.data_final = data_final
        self.tabela = tabela
        #Bourrienne’s memoirs
    
    @abstractmethod
    def inserirProdutos(self):
        pass
    
    @abstractmethod
    def retornarAcertos(self):
        pass
    
    def formatarDataCadastro(self, data):
        milliseconds_since_epoch = int(data)
        seconds_since_epoch = milliseconds_since_epoch / 1000
        date_object = datetime.fromtimestamp(seconds_since_epoch, timezone.utc)
        formatted_date = date_object.strftime('%d/%m/%Y')
        return formatted_date
    
class HistoricoAcertosAcabados(HistoricoAcertos):
    def retornarAcertos(self):
        acertos = db_ctrl_estoque.buscarProdutosPorData(self.data_inicio, self.data_final)
        return acertos
        
    def inserirProdutos(self):
        self.tabela.delete(*self.tabela.get_children())
        self.tabela.delete(*self.tabela.get_children())
        
        prod_periodo = self.retornarAcertos()
                
        # Inserir motivos acabados
        for x in prod_periodo:
            id = x['pkProduto']
            descricao = x['descricao']
            motivo = x['motivo']
            quemSolicitou = x['solicitante']
            subtracao = x['saldo']
            data_formatada = self.formatarDataCadastro(x['dataMov'])
            data = (id, descricao, motivo, quemSolicitou, subtracao, data_formatada)
            self.tabela.insert(parent='', index=0, values=data)

class HistoricoAcertosSA(HistoricoAcertos):
    def retornarAcertos(self):
        acertos = db_ctrl_estoque.buscarSAPorData(self.data_inicio, self.data_final)
        return acertos
        
    def inserirProdutos(self):
        prod_periodo = self.retornarAcertos()
    
        self.tabela.delete(*self.tabela.get_children())
        self.tabela.delete(*self.tabela.get_children())
        
        for y in prod_periodo:
            id = y['idxProduto']
            descricao = y['descricao']
            motivo = y['motivo']
            quemSolicitou = y['solicitante']
            subtracao = y['saldo']
            data_formatada = self.formatarDataCadastro(y['dataMov'])
            data = (id, descricao, motivo, quemSolicitou, subtracao, data_formatada)
            self.tabela.insert(parent='', index=0, values=data)