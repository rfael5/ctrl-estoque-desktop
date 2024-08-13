from abc import abstractmethod
from datetime import datetime
from tkinter import messagebox
import classes.controleEstoqueService as controleEstoqueService


class AtualizacaoSaldo:
    
    def __init__(self, produto, att_saldo, tp_att, motivo, solicitante, tabela, janela):
        self.produto = produto
        self.att_saldo = att_saldo
        self.tp_att = tp_att
        self.motivo = motivo
        self.solicitante = solicitante
        self.tabela = tabela
        self.janela = janela
    
    @abstractmethod
    def criarProduto(self):
        pass
    
    @abstractmethod
    def atualizar(self):
        pass
    
    @abstractmethod
    def atualizarTabela(self):
        pass
    
    @abstractmethod
    def inserirProdutos(self):
        pass
    
    @abstractmethod
    def filtrarListaControle(self):
        pass
    
    def atualizarTabela(self):
        controleEstoque = controleEstoqueService.EstoqueService()
        self.tabela.delete(*self.tabela.get_children())
        return controleEstoque
    
    def validarAdicaoEstoque(self, objeto):
        if self.tp_att == 'soma':
            objeto['saldo'] = abs(float(objeto['saldo']))
            return objeto
        else:
            if not self.motivo or not self.solicitante:
                messagebox.showinfo(
                    'Nenhum motivo ou solicitante', 'Por favor, verifique se os campos motivos e solicitante estão preenchidos corretamente.'
                    )
                return
            else:
                objeto['saldo'] = -abs(float(objeto['saldo']))
                return objeto
    
    def recuperarHoraAtual(self):
        data_hora_atual = datetime.now()
        formato = "%Y-%m-%d_%H-%M-%S"
        data_hora_formatada = data_hora_atual.strftime(formato)
        return data_hora_formatada
    
    def converterParaMilisegundos(self):
        data_hora_atual = datetime.now()
        milissegundos = int(data_hora_atual.timestamp() * 1000)
        return milissegundos

class AttTabelaAcabados(AtualizacaoSaldo):

    def criarProduto(self):
        novo_produto = {
            "pkProduto": self.produto[0],
            "descricao": self.produto[1],
            "saldo": self.att_saldo,
            "unidade": self.produto[2],
            "dataMov": self.converterParaMilisegundos(),
            "tipoMov": self.tp_att,
            "motivo": self.motivo,
            "solicitante": self.solicitante
        }
        self.atualizar(novo_produto)
        self.janela.destroy()
    
    def atualizar(self, objeto):
        try:
            obj_validado = self.validarAdicaoEstoque(objeto)
            db_ctrl_estoque.adicionarEstoque(obj_validado)
            db_ctrl_estoque.getEstoqueCompleto()
            self.inserirProdutos()
            
        except Exception as e:
            messagebox.showerror(
                'Erro', f'Ocorreu um erro ao tentar inserir, verifique se os valores estão corretos. {str(e)}'  
            )
            return
    
    def inserirProdutos(self):
        controle_estoque = self.atualizarTabela()
        controle_estoque.formatarAcabados()
        lista_produtos = controle_estoque.ctrl_acabados
        for produto in lista_produtos:
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
            


class AttSemiAcabados(AtualizacaoSaldo):
    def criarProduto(self):
        adicao_saldo = {
            "idxProduto":self.produto[0],
            "descricao":self.produto[1],
            "saldo":self.att_saldo,
            "unidade": self.produto[3],
            "dataMov": self.converterParaMilisegundos(),
            "tipoMov": self.tp_att,
            "motivo": self.motivo,
            "solicitante": self.solicitante
        }
        self.atualizar(adicao_saldo)
        self.janela.destroy()
        
    def atualizar(self, objeto):
        try:
            obj_validado = self.validarAdicaoEstoque(objeto)
            db_ctrl_estoque.addEstoqueSA(obj_validado)
            db_ctrl_estoque.getEstoqueSA
            self.inserirProdutos()
            
        except Exception as e:
            messagebox.showerror(
                'Erro', f'Ocorreu um erro ao tentar inserir, verifique se os valores estão corretos. {str(e)}'
            )
            
    
    def inserirProdutos(self):
        controle_estoque = self.atualizarTabela()
        controle_estoque.formatarSemiAcabados()
        lista_sa = controle_estoque.ctrl_semiacabados
        for sa in lista_sa:
            id = sa['IDX_PRODUTO']
            produto = sa['DESCRICAO']
            saldo = sa['totalProducao']
            un = sa['UN']
            if saldo >= 0:
                total_sa = 'black'
            else:
                total_sa = 'red'
            data_sa = (id, produto, saldo, un)
            self.tabela.insert(parent='', index=0, values=data_sa, tags=total_sa)
        self.tabela.tag_configure("red", foreground="red")