from tkinter import *
from tkinter import ttk

#As funçãos nesse arquivo servem somente para criar as tabelas
#na nossa interface.

#Seleciona a linha de uma tabela
def armazenarIdProduto(event, tabela, _tptabela):
    global tabela_atual
    indice = tabela.selection()
    if indice:
        #tabela_atual = tabela.item(indice)['values'][0]
        tabela_atual = {
            'id_produto':tabela.item(indice)['values'][0],
            'tipo_tabela':_tptabela    
        }
        # print(tabela_atual)


def tabelaControleEstoque(frame):
    global tbl_controle
    tbl_controle = ttk.Treeview(frame, columns = ('ID', 'Produto', 'Saldo', 'UN'), show='headings')
    tbl_controle.heading('ID', text='ID')
    tbl_controle.heading('Produto', text='Produto')
    tbl_controle.heading('Saldo', text='Saldo')
    tbl_controle.heading('UN', text='UN')
    tbl_controle.grid(row=4, columnspan=2, padx=(80, 0), pady=10, sticky="nsew")
    
    tbl_controle.column('ID', width=100, anchor=CENTER)
    tbl_controle.column('Produto', width=300, anchor=CENTER)
    tbl_controle.column('Saldo', width=100, anchor=CENTER)
    tbl_controle.column('UN', width=100, anchor=CENTER)
    tbl_controle.bind('<ButtonRelease>', lambda event: armazenarInfoProduto(event, tbl_controle))


def tabelaMotivo(frame):
    global tbl_motivo_acabados
    
    tbl_motivo_acabados = ttk.Treeview(frame, columns = ('Produto', 'Tipo alteração', 'Solicitante', 'Motivo', 'Saldo', 'Data e hora'), show='headings')
    tbl_motivo_acabados.heading('Produto', text='Produto')
    tbl_motivo_acabados.heading('Tipo alteração', text='Tipo alteração')
    tbl_motivo_acabados.heading('Solicitante', text='Solicitante')
    tbl_motivo_acabados.heading('Motivo', text='Motivo')
    tbl_motivo_acabados.heading('Saldo', text='Subtração')
    tbl_motivo_acabados.heading('Data e hora', text='Data e hora')
    tbl_motivo_acabados.grid(row=5, columnspan=2, padx=(80, 0), pady=10, sticky="nsew")
    
    tbl_motivo_acabados.column('Produto', width=250, anchor=CENTER)
    tbl_motivo_acabados.column('Tipo alteração', width=150, anchor=CENTER)
    tbl_motivo_acabados.column('Solicitante', width=150, anchor=CENTER)
    tbl_motivo_acabados.column('Motivo', width=200, anchor=CENTER)
    tbl_motivo_acabados.column('Saldo', width=100, anchor=CENTER)
    tbl_motivo_acabados.column('Data e hora', width=150, anchor=CENTER)
    
    tbl_motivo_acabados.bind('<ButtonRelease>', lambda event: armazenarInfoProduto(event, tbl_motivo_acabados))



def armazenarInfoProduto(event, _tblControle):
    #global dados_produto
    indice = _tblControle.selection()
    if indice:
        p = _tblControle.item(indice)['values']
        return p

