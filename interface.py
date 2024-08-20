from operator import itemgetter
import tabelas
import http_requests as http

from datetime import datetime, timezone
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
from time import time

def getDataAtualMilisegundos():
    milisegundos = int(time() * 1000)
    return str(milisegundos)

def formatarDataMovimentacao(data):
    milisegundos = int(data)
    segundos = milisegundos / 1000
    data_obj = datetime.fromtimestamp(segundos, timezone.utc)
    data_formatada = data_obj.strftime('%d/%m/%Y')
    return data_formatada

def isNullOrEmpty(value):
    if value == "" or value == None:
        return True
    else:
        return False

def inserirTabelaControle():
    #global prod_estoque
    controleEstoque = http.getSaldoEstoque()
    estoque_ordenado = sorted(controleEstoque, key=itemgetter('id'), reverse=True)
    tabelas.tbl_controle.delete(*tabelas.tbl_controle.get_children())
    for produto in estoque_ordenado:
        id = produto['id']
        descricao = produto['nomeProduto']
        saldo = produto['saldoTotal']
        un = produto['unidade']
        if saldo > 300:
            total = 'black'
        else:
            total = 'red'
        data = (id, descricao, saldo, un)
        tabelas.tbl_controle.insert(parent='', index=0, values=data, tags=total)
    tabelas.tbl_controle.tag_configure("red", foreground="red")


def inserirTabelaHistorico(historico):
    for registro in historico:
        produto = registro['descricao']
        tipo_alteracao = registro['tipoMov']
        solicitante = registro['solicitante']
        motivo = registro['motivo']
        saldo = registro['saldo']
        data_hora = formatarDataMovimentacao(registro['dataMov'])
        data = (produto, tipo_alteracao, solicitante, motivo, saldo, data_hora)
        tabelas.tbl_motivo_acabados.insert(parent='', index=0, values=data)


def verDataSelecionada():
    _inicio = dtInicioMotivos.get()
    _fim = dtFimMotivos.get()
    ms_inicio = converterParaMilisegundos(_inicio)
    ms_fim = converterParaMilisegundos(_fim)
    historico = http.getHistoricoPeriodo(ms_inicio, ms_fim)
    tabelas.tbl_motivo_acabados.delete(*tabelas.tbl_motivo_acabados.get_children())
    inserirTabelaHistorico(historico)



def converterParaMilisegundos(data):
    data_obj = datetime.strptime(data, '%d/%m/%Y')
    milissegundos = int(data_obj.timestamp() * 1000)
    return milissegundos


def janelaAttEstoque(_tbl, tp_att):
    dados_prod = tabelas.armazenarInfoProduto(Event, _tbl)
    
    if dados_prod == None:
        messagebox.showinfo('Nenhum produto selecionado', 'Selecione um produto na tabela para alterar seu saldo.')
    else:
        global janela_soma
        janela_soma = Toplevel(root)
        janela_soma.title("Atualização estoque")
        janela_soma.geometry("400x300")
        
        if tp_att == 'adicao':
            _titulo = 'Atualizar estoque'
            titulo_botao = 'Adicionar'
        else:
            _titulo = 'Subtrair do estoque'
            titulo_botao = 'Subtrair'
        
        titulo_janela = Label(janela_soma, text=f"{dados_prod[1]}", font=("Arial", 14))
        titulo_janela.grid(row=0, padx=(40, 0), pady=(0,20))
        
        lbl_add_saldo = Label(janela_soma, text = f'{_titulo}:')
        lbl_add_saldo.grid(row=1, padx=(40, 0))
        att_var = IntVar()
        att_saldo = Entry(janela_soma, textvariable=att_var, bd=4)
        att_saldo.grid(row=2, padx=(40, 0), pady=(0,20))
        
        lbl_motivo_explicacao = Label(janela_soma, text="Por favor, escreva o nome do solicitante:")
        lbl_motivo_explicacao.grid(row=3, padx=(40, 0))
        solicitante_var = StringVar()
        solicitante = Entry(janela_soma, textvariable=solicitante_var, bd=4)
        solicitante.grid(row=4, padx=(40, 0), pady=(0,20))

        lbl_motivo_explicacao = Label(janela_soma, text="Por favor, escreva o motivo da atualização do estoque:")
        lbl_motivo_explicacao.grid(row=5, padx=(40, 0))
        just_var = StringVar()
        motivo = Entry(janela_soma, textvariable=just_var, bd=4)
        motivo.grid(row=6, padx=(40, 0), pady=(0,20))

        getDataAtualMilisegundos()

        obj = {
            "idProduto":dados_prod[0], 
            "descricao": dados_prod[1], 
            "saldo": att_var, 
            "unidade":"UN", 
            "dataMov": getDataAtualMilisegundos(),
            "tipoMov":tp_att,
            "solicitante": solicitante_var,
            "motivo":just_var}

        btn_alterar = Button(janela_soma, text=f"{titulo_botao}", command=lambda: setarDadosDicionario(obj, tp_att))
        btn_alterar.grid(row=7, padx=(40, 0), pady=20)


def setarDadosDicionario(obj, tp_att):
    data = {
        "idProduto":obj["idProduto"],
        "descricao":obj["descricao"],
        "saldo":obj["saldo"].get(),
        "unidade":"UN",
        "dataMov":obj["dataMov"],
        "tipoMov":tp_att,
        "solicitante":obj["solicitante"].get(),
        "motivo":obj["motivo"].get()
    }

    if data['tipoMov'] == "remocao":
        if int(data["saldo"]) >= 0:
            data["saldo"] = int(data["saldo"]) * -1
    
    atualizarSaldo(data)


def atualizarSaldo(obj):
    if isNullOrEmpty(obj['motivo']) or isNullOrEmpty(obj['solicitante']):
        messagebox.showinfo("Erro", "Os campos 'motivo' e 'solicitante' são obrigatórios'")
    else:
        http.atualizarSaldo(obj["idProduto"], obj["saldo"])
        http.alterarEstoque(obj)
        inserirTabelaControle()
        janela_soma.destroy()



#Tkinter
root = Tk()
root.title("| Controle de estoque |")

root.geometry("1150x800")

notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=True)

page1 = Frame(notebook)
notebook.add(page1, text='| Cadastro e remoção de produtos |')

mainFrame = Frame(page1)
mainFrame.pack(fill=BOTH, expand=1)

canvas = Canvas(mainFrame)
canvas.pack(side=LEFT, fill=BOTH, expand=1)

scrollbar = ttk.Scrollbar(mainFrame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e:canvas.configure(scrollregion=canvas.bbox("all")))

secondFrame = Frame(canvas)
canvas.create_window((0, 0), window=secondFrame, anchor="nw")

#Row 4 - Tabela controle estoque

titulo_pagina = Label(secondFrame, text="Produtos no estoque", font=('Arial', 14), width=22)
titulo_pagina.grid(row=0, column=0, columnspan=2, pady=5, sticky="nsew")

btn_somar_estoque = Button(secondFrame, text="Adicionar produtos", bg='#C0C0C0', font=("Arial", 16), command=lambda: janelaAttEstoque(tabelas.tbl_controle, 'adicao'))
btn_somar_estoque.grid(row=6, column=0, columnspan=2, padx=(80, 0), pady=(10, 30), sticky='nsew')

btn_acerto_estoque = Button(secondFrame, text="Remover produtos", bg='#C0C0C0', font=("Arial", 16), command=lambda: janelaAttEstoque(tabelas.tbl_controle, 'remocao'))
btn_acerto_estoque.grid(row=7, column=0, columnspan=2, padx=(80, 0), pady=(10, 30), sticky='nsew')

btn_atualisar = Button(secondFrame, text="Atualizar saldo", bg='#C0C0C0', font=("Arial", 16), command=inserirTabelaControle)
btn_atualisar.grid(row=8, column=0, columnspan=2, padx=(80, 0), pady=(10, 30), sticky='nsew')


####################################################
# PÁGINA 2
####################################################

page2 = Frame(notebook)
notebook.add(page2, text='| Histórico de movimentações |')

lbl_dtInicioMotivos = Label(page2, text="De:", font=("Arial", 14))
lbl_dtInicioMotivos.grid(row=1, padx=(0, 190), column=0, sticky="e")

dtInicioMotivos = DateEntry(page2, font=('Arial', 12), width=22, height=20, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
dtInicioMotivos.grid(row=2, column=0, padx=(150, 0), pady=5, sticky="e")

lbl_dtFimMotivos = Label(page2, text="Até:", font=("Arial", 14))
lbl_dtFimMotivos.grid(row=1, column=1, padx=(50, 0), pady=5, sticky="w")

dtFimMotivos = DateEntry(page2, font=('Arial', 12), width=22, height=20, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
dtFimMotivos.grid(row=2, column=1, padx=(50, 0), pady=5, sticky="w")

btn_buscar_acertos = Button(page2, text="Ver movimentações no periodo", bg='#C0C0C0', font=("Arial", 16), command=verDataSelecionada)
btn_buscar_acertos.grid(row=3, column=0, columnspan=2, padx=(80, 0), pady=(10, 30), sticky='nsew')

tabelas.tabelaControleEstoque(secondFrame)
tabelas.tabelaMotivo(page2) 
inserirTabelaControle()
root.mainloop() 