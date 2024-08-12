import tabelas
import classes.controleEstoqueService as controleEstoqueService
import classes.atualizacao_saldo as atualizacao_saldo
import classes.filtro_controle as filtro_controle
#import classes.historico_acertos as historico_acertos

import pandas as pd
import numpy as np
import json
from datetime import datetime, timezone
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox


def inserirTabelaControle():
    #global prod_estoque
    controleEstoque = controleEstoqueService.EstoqueService()
    controleEstoque.formatarProdutosControle()
    prod_estoque = controleEstoque.ctrl_acabados
    global filtro_acabados
    filtro_acabados = filtro_controle.FiltroControleAcabados( tabelas.tbl_controle, controleEstoque.ctrl_acabados)
    tabelas.tbl_controle.delete(*tabelas.tbl_controle.get_children())
    for produto in controleEstoque.ctrl_acabados:
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
        tabelas.tbl_controle.insert(parent='', index=0, values=data, tags=total)
    tabelas.tbl_controle.tag_configure("red", foreground="red")
    
    # global saprod_estoque
    # saprod_estoque = controleEstoque.ctrl_semiacabados
    global filtro_sa
    filtro_sa = filtro_controle.FiltroControleSA(tabelas.tbl_ctrl_semi, controleEstoque.ctrl_semiacabados)
    tabelas.tbl_ctrl_semi.delete(*tabelas.tbl_ctrl_semi.get_children())
    for sa in controleEstoque.ctrl_semiacabados:
        id = sa['IDX_PRODUTO']
        produto = sa['DESCRICAO']
        saldo = sa['totalProducao']
        un = sa['UN']
        if saldo >= 0:
            total_sa = 'black'
        else:
            total_sa = 'red'
        data_sa = (id, produto, saldo, un)
        tabelas.tbl_ctrl_semi.insert(parent='', index=0, values=data_sa, tags=total_sa)
    tabelas.tbl_ctrl_semi.tag_configure("red", foreground="red")


def janelaAttEstoque(_tbl, tp_controle, tp_att):
    dados_prod = tabelas.armazenarInfoProduto(Event, _tbl)
    
    if dados_prod == None:
        messagebox.showinfo('Nenhum produto selecionado', 'Selecione um produto na tabela para alterar seu saldo.')
    else:
        global janela_soma
        janela_soma = Toplevel(root)
        janela_soma.title("Atualização estoque")
        janela_soma.geometry("400x300")
        
        if tp_att == 'soma':
            _titulo = 'Atualizar estoque'
            titulo_botao = 'Adicionar'
        else:
            _titulo = 'Subtrair do estoque'
            titulo_botao = 'Subtrair'
        
        titulo_janela = Label(janela_soma, text=f"{dados_prod[1]}", font=("Arial", 14))
        titulo_janela.grid(row=0, padx=(40, 0), pady=(0,20))
        
        lbl_add_saldo = Label(janela_soma, text = f'{_titulo}:')
        lbl_add_saldo.grid(row=1, padx=(40, 0))
        att_var = ''
        att_saldo = Entry(janela_soma, textvariable=att_var, bd=4)
        att_saldo.grid(row=2, padx=(40, 0), pady=(0,20))
        
        lbl_motivo_explicacao = Label(janela_soma, text="Por favor, escreva o motivo da atualização do estoque:")
        lbl_motivo_explicacao.grid(row=3, padx=(40, 0))
        just_var = ''
        motivo = Entry(janela_soma, textvariable=just_var, bd=4)
        motivo.grid(row=4, padx=(40, 0), pady=(0,20))
        
        lbl_motivo_explicacao = Label(janela_soma, text="Por favor, escreva o nome do solicitante:")
        lbl_motivo_explicacao.grid(row=5, padx=(40, 0))
        solicitante_var = ''
        solicitante = Entry(janela_soma, textvariable=solicitante_var, bd=4)
        solicitante.grid(row=6, padx=(40, 0), pady=(0,20))
        
        def on_button_click():
            _attSaldo = att_saldo.get()
            _motivo = motivo.get()
            _solicitante = solicitante.get()
            
            obj = atualizacao_saldo.AttTabelaAcabados(dados_prod, _attSaldo, tp_att, _motivo, _solicitante, tabelas.tbl_controle, janela_soma)
            
            obj.criarProduto()
        
        btn_add = Button(janela_soma, text=f"{titulo_botao}", bg='#C0C0C0', font=("Arial", 16), command=on_button_click)
        btn_add.grid(row=7, sticky='nsew', padx=(40, 0), pady=(0,20))

#O código abaixo cria a interface que usamos para testar nosso script.

#Tkinter
root = Tk()
root.title("| Gerar pedidos de suprimento |")

root.geometry("1150x800")

notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=True)

page1 = Frame(notebook)
notebook.add(page1, text='| Relatório pedidos de suprimento |')

mainFrame = Frame(page1)
mainFrame.pack(fill=BOTH, expand=1)

canvas = Canvas(mainFrame)
canvas.pack(side=LEFT, fill=BOTH, expand=1)
#canvas.grid(row=0, column=0, sticky=EW)

scrollbar = ttk.Scrollbar(mainFrame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
#scrollbar.grid(row=0, rowspan=10, column=1, sticky="ns")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e:canvas.configure(scrollregion=canvas.bbox("all")))

secondFrame = Frame(canvas)
canvas.create_window((0, 0), window=secondFrame, anchor="nw")



####################################################
#PÁGINA 2
####################################################

page2 = Frame(notebook)
notebook.add(page2,text='| Controle estoque acabados |')

saldo_var = ''
label_pesquisa_sa = Label(page2, text="Pesquise o produto acabado:", font=('Arial', 12, 'bold'))
label_pesquisa_sa.grid(row=1, column=0, columnspan=2, padx=(80, 0), pady=(10, 0), sticky='nsew')

input_saldo = Entry(page2, textvariable=saldo_var, bd=4)
input_saldo.grid(row=2, column=0, columnspan=2, padx=(80, 0), pady=(10, 30), sticky='nsew')
#input_saldo.bind("<KeyRelease>", lambda event: filtrarListasControle(event, filtro_acabados, input_saldo))

#Row 4 - Tabela controle estoque

btn_somar_estoque = Button(page2, text="Adicionar estoque", bg='#C0C0C0', font=("Arial", 16), command=lambda: janelaAttEstoque(tabelas.tbl_controle, 'acabados', 'soma'))
btn_somar_estoque.grid(row=6, column=0, columnspan=2, padx=(80, 0), pady=(10, 30), sticky='nsew')

btn_atualisar = Button(page2, text="Atualizar saldo", bg='#C0C0C0', font=("Arial", 16), command=inserirTabelaControle)
btn_atualisar.grid(row=7, column=0, columnspan=2, padx=(80, 0), pady=(10, 30), sticky='nsew')

btn_acerto_estoque = Button(page2, text="Aplicar acerto de estoque", bg='#C0C0C0', font=("Arial", 16), command=lambda: janelaAttEstoque(tabelas.tbl_controle, 'acabados', 'subtracao'))
btn_acerto_estoque.grid(row=8, column=0, columnspan=2, padx=(80, 0), pady=(10, 30), sticky='nsew')

####################################################
# PÁGINA 4
####################################################
def verDataSelecionada():
    _inicio = dtInicioMotivos.get()
    _fim = dtFimMotivos.get()
    ms_inicio = converterParaMilisegundos(_inicio)
    ms_fim = converterParaMilisegundos(_fim)
    acertos_acabados = historico_acertos.HistoricoAcertosAcabados(ms_inicio, ms_fim, tabelas.tbl_motivo_acabados)
    acertos_sa = historico_acertos.HistoricoAcertosSA(ms_inicio, ms_fim, tabelas.tbl_motivo_semi_acabados)
    acertos_acabados.inserirProdutos()
    acertos_sa.inserirProdutos()
    
    _acertos = acertos_acabados.retornarAcertos()
    global lista_acertos_acabados
    lista_acertos_acabados = filtro_controle.FiltroMotivo(tabelas.tbl_motivo_acabados, _acertos)
    
    _acertossa = acertos_sa.retornarAcertos()
    global lista_acertos_sa
    lista_acertos_sa = filtro_controle.FiltroMotivoSA(tabelas.tbl_motivo_semi_acabados, _acertossa)

def filtrarListasControle(event, filtro, entrada):
    text = entrada.get()
    filtro.filtrar(text)

def converterParaMilisegundos(data):
    data_obj = datetime.strptime(data, '%d/%m/%Y')
    milissegundos = int(data_obj.timestamp() * 1000)
    return milissegundos
    
page4 = Frame(notebook)
notebook.add(page4, text='| Motivos de estoque |')

lbl_dtInicioMotivos = Label(page4, text="De:", font=("Arial", 14))
lbl_dtInicioMotivos.grid(row=1, padx=(0, 190), column=0, sticky="e")

dtInicioMotivos = DateEntry(page4, font=('Arial', 12), width=22, height=20, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
dtInicioMotivos.grid(row=2, column=0, padx=(150, 0), pady=5, sticky="e")

lbl_dtFimMotivos = Label(page4, text="Até:", font=("Arial", 14))
lbl_dtFimMotivos.grid(row=1, column=1, padx=(50, 0), pady=5, sticky="w")

dtFimMotivos = DateEntry(page4, font=('Arial', 12), width=22, height=20, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
dtFimMotivos.grid(row=2, column=1, padx=(50, 0), pady=5, sticky="w")

btn_buscar_acertos = Button(page4, text="Ver acertos no estoque", bg='#C0C0C0', font=("Arial", 16), command=verDataSelecionada)
btn_buscar_acertos.grid(row=3, column=0, columnspan=2, padx=(80, 0), pady=(10, 30), sticky='nsew')

# Campo input_motivo com placeholder
#placeholder_motivo = "Pesquisar produto"
input_motivo = Entry(page4, textvariable=saldo_var, bd=4)
input_motivo.insert(0, 'Pesquisar produto...')
input_motivo.grid(row=10, column=0, columnspan=2, padx=(80, 0), pady=(10, 10), sticky='nsew')
#put_placeholder(input_motivo, placeholder_motivo)
input_motivo.bind("<FocusIn>", lambda event: input_motivo.delete('0', 'end'))
#input_motivo.bind("<FocusOut>", lambda event: restore_placeholder(event, placeholder_motivo))
input_motivo.bind("<KeyRelease>", lambda event: filtrarListasControle(event, lista_acertos_acabados, input_motivo))

# Campo input_motivoSA com placeholder
#placeholder_motivoSA = "Pesquisar produto"
saldo_var_sa = StringVar()
input_motivoSA = Entry(page4, textvariable=saldo_var_sa, bd=4)
input_motivoSA.insert(0, 'Pesquisar produto...')
input_motivoSA.grid(row=15, column=0, columnspan=2, padx=(80, 0), pady=(10, 10), sticky='nsew')
#put_placeholder(input_motivoSA, placeholder_motivoSA)
input_motivoSA.bind("<FocusIn>", lambda event: input_motivoSA.delete('0', 'end'))
# input_motivoSA.bind("<FocusOut>", lambda event: restore_placeholder(event, placeholder_motivoSA))
input_motivoSA.bind("<KeyRelease>", lambda event: filtrarListasControle(event, lista_acertos_sa, input_motivoSA))

tabelas.tabelaControleEstoque(page2)  # Adiciona tabela de controle de estoque na página 2 
tabelas.tabelaMotivo(page4)  # Adiciona tabela de motivo na página 4
tabelas.tabelaMotivoSA(page4)  # Adiciona tabela de motivo SA na página 4
inserirTabelaControle() 
#inserirTabelaMotivos()
root.mainloop()  