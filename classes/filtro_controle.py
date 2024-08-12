from abc import abstractmethod
from datetime import datetime, timezone


class Filtro():
    def __init__(self, tabela, lista_produtos):
        self.tabela = tabela
        self.lista_produtos = lista_produtos
    
    @abstractmethod
    def filtrar(self, input):
        pass
    
    def execFiltro(self, input):
        text = input
        prod_filtrado = list(filter(lambda produto:text.lower() in produto['DESCRICAO'].lower(), self.lista_produtos))
        self.tabela.delete(*self.tabela.get_children())
        return prod_filtrado
    
    def execFiltroMotivos(self, input):
        text = input
        motivos_filtrados = list(filter(lambda motivo: text.lower() in motivo['descricao'].lower(), self.lista_produtos))
        self.tabela.delete(*self.tabela.get_children())
        return motivos_filtrados
    
    def formatarDataCadastro(self, data):
        milliseconds_since_epoch = int(data)
        seconds_since_epoch = milliseconds_since_epoch / 1000
        date_object = datetime.fromtimestamp(seconds_since_epoch, timezone.utc)
        formatted_date = date_object.strftime('%d/%m/%Y')
        return formatted_date

class FiltroControleAcabados(Filtro):
    def filtrar(self, input):
        self.execFiltro(input)
        produtos = self.execFiltro(input)
        for produto in produtos:
            id = produto['PK_PRODUTO']
            descricao = produto['DESCRICAO']
            un = produto['UN']
            cod_produto = produto['CODPRODUTO']
            saldo = produto['somaQuantidade']
            if saldo >= 0:
                total = 'black'
            else:
                total = 'red'
            data = (id, descricao, un, cod_produto, saldo)
            self.tabela.insert(parent='', index=0, values=data, tags=total)
        self.tabela.tag_configure("red", foreground="red")

class FiltroControleSA(Filtro):
    def filtrar(self, input):
        produtos = self.execFiltro(input)
        for semiacabado in produtos:
            id = semiacabado['IDX_PRODUTO']
            produto = semiacabado['DESCRICAO']
            saldo = semiacabado['totalProducao']
            un = semiacabado['UN']
            data_sa = (id, produto, saldo, un)
            if saldo >= 0:
                total_sa = 'black'
            else:
                total_sa = 'red'
            self.tabela.insert(parent='', index=0, values=data_sa, tags=total_sa)
        self.tabela.tag_configure("red", foreground="red")

class FiltroMotivo(Filtro):
    def filtrar(self, input):
        produtos = self.execFiltroMotivos(input)
        for motivoA in produtos:
            id = motivoA['pkProduto']
            descricao = motivoA['descricao']
            motivo = motivoA['motivo']
            quemSolicitou = motivoA['solicitante']
            subtracao = motivoA['saldo']
            dataMov = self.formatarDataCadastro(motivoA['dataMov'])
            data = (id, descricao, motivo, quemSolicitou, subtracao, dataMov)
            self.tabela.insert(parent='', index=0, values=data)

class FiltroMotivoSA(Filtro):
    def filtrar(self, input):
        produtos = self.execFiltroMotivos(input)
        for motivoSA in produtos:
            id = motivoSA['idxProduto']
            descricao = motivoSA['descricao']
            motivo = motivoSA['motivo']
            quemSolicitou = motivoSA['solicitante']
            subtracao = motivoSA['saldo']
            dataMov = self.formatarDataCadastro(motivoSA['dataMov'])
            data = (id, descricao, motivo, quemSolicitou, subtracao, dataMov)
            self.tabela.insert(parent='', index=0, values=data)