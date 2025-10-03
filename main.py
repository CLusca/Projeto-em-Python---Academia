from tkinter import *
import time
import json
import re
import os

padrao_str = r'[^a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ\s]'
padrao_num = r'\D'

def criarIndice(arquivo,cod_Tipo):
    indice = {}
    for i, item in enumerate(arquivo):
        if item[cod_Tipo] is not None and item[cod_Tipo].isdigit() == False:
            indice[item[cod_Tipo].strip().lower()] = i
        else:
            indice[item[cod_Tipo]] = i
    return indice

class No:
    def __init__(raiz, valor, codigo):
        raiz.valor    = valor
        raiz.esquerda = None
        raiz.direita  = None
        raiz.indice   = codigo

def construirArvore(indice):
    raiz = None
    for codigo, indice_valor in indice.items():
        raiz = inserir(raiz, codigo, indice_valor)
    return raiz

def inserir(raiz, valor, codigo):
    if raiz is None:
        return No(valor, codigo)
    if valor < raiz.valor:
        raiz.esquerda = inserir(raiz.esquerda, valor, codigo)
    elif valor > raiz.valor:
        raiz.direita = inserir(raiz.direita, valor, codigo)
    return raiz

def consultar(raiz, valor_buscado, forma_busca):
     if forma_busca == True:
        if valor_buscado.isdigit() == False:
                valor_buscado = valor_buscado.strip().lower()
        if raiz is None:
            print("Valor nao encontrado")
            return raiz
        if raiz.valor == valor_buscado:
            print(f"{raiz.indice}, {raiz.valor}")
            return raiz.valor
        elif valor_buscado < raiz.valor:
            return consultar(raiz.esquerda, valor_buscado)
        return consultar(raiz.direita, valor_buscado)
     else:
        if valor_buscado.isdigit() == False:
            print("Valor invalido para busca de indice")
            return
        if raiz is None:
            print("Valor nao encontrado")
            return raiz
        if raiz.indice == valor_buscado:
            print(f"{raiz.indice}, {raiz.valor}")
            return raiz.valor
        elif valor_buscado < raiz.indice:
            return consultar(raiz.esquerda, valor_buscado)
        return consultar(raiz.direita, valor_buscado)

def exclusão (raiz, valor):
    if raiz is None:
        return raiz
    if valor < raiz.valor < raiz.indice:
        raiz.esquerda = exclusão(raiz.esquerda, valor)
    elif valor > raiz.valor > raiz.indice:
        raiz.direita = exclusão(raiz.direita, valor)
    else:
        raiz.valor = None
        raiz.indice = None
    return raiz

def carregarDados(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Arquivo '{caminho_arquivo}' não foi encontrado.")
        return []

def buscaExaustiva(listaDeDados, campoBusca, valorBuscado):
    resultados = []
    
    buscarPorTexto = isinstance(valorBuscado, str)
    valorBuscadoFormatado = valorBuscado.strip().lower()

    for registro in listaDeDados:
        valorDoRegistro = registro.get(campoBusca)

        if valorDoRegistro is None:
            continue
        
        if buscarPorTexto and isinstance(valorDoRegistro, str):
            if valorDoRegistro.lower() == valorBuscadoFormatado:
                resultados.append(registro)
        elif valorDoRegistro == valorBuscadoFormatado:
            resultados.append(registro)
    if resultados == []:
        return 0
    else: 
        infos = resultados[0]
        return infos
    
def listarTudo(raiz):
    if raiz is None:
        print ("Nada encontrado")
        return
    elif raiz.esquerda is not None:
        listarTudo(raiz.esquerda)
    print(f"{raiz.indice}, {raiz.valor.title()}")
    if raiz.direita is not None:
        listarTudo(raiz.direita)

def buscarAluno(arvoreAluno, arvoreCidade):
    os.system('cls')
    print("*--- Escolha uma das Opções Abaixo ---*")
    print("\n ---* Buscar Aluno *---")
    print("1 - Listar Indices e Nomes")
    print("2 - Buscar por Nome")
    print("3 - Buscar por indice")
    print("0 - Retornar")
    opcao_bruta = input("Opcao: ")

    opcao_tratada = re.sub(padrao_num, '', opcao_bruta)

    
    match opcao_tratada:
        case '1':
            os.system('cls')
            listarTudo (arvoreAluno)
            continuar = input("Aperte Enter para continuar...")
            match continuar:
                case '':
                    return
        case '2':
            os.system('cls')
            input_nome = input("Qual o Nome do Aluno: ").strip().lower()
            consultar (arvoreAluno, input_nome, True)
            
        case '3':
            os.system('cls')
            input_indice= input("Qual o Indice do Aluno: ").strip()
            consultar (arvoreAluno, input_indice, False)
            
        case '0':
            return


def contador_5_segundos():
    print("\n ---* Limpando a tela Em *---")
    print("5 Segundos")
    time.sleep(1)
    print("4 Segundos")
    time.sleep(1)
    print("3 Segundos")
    time.sleep(1)
    print("2 Segundos")
    time.sleep(1)
    print("1 Segundo")
    time.sleep(1)

while True:
    dadosAlunos      = carregarDados('./dados/alunos.json')
    dadosCidades     = carregarDados('./dados/cidade.json')
    dadosProfessores = carregarDados('./dados/professores.json')
    dadosModalidades = carregarDados('./dados/modalidades.json')
    dadosMatriculas  = carregarDados('./dados/matriculas.json')

    indice_alunos = criarIndice(dadosAlunos,"nome".strip().lower())
    indice_cidades =  criarIndice(dadosCidades,"descricao".strip().lower())
    indice_professores = criarIndice(dadosProfessores,"nome".strip().lower())
    indice_modalidades = criarIndice(dadosModalidades,"descricao".strip().lower())
    indice_matriculas =criarIndice(dadosMatriculas,"cod_Matricula")

    arvore_alunos = construirArvore(indice_alunos)
    arvore_cidades = construirArvore(indice_cidades)
    arvore_professores = construirArvore(indice_professores)
    arvore_modalidades = construirArvore(indice_modalidades)
    arvore_matriculas = construirArvore(indice_matriculas)   

    print("*--- Escolha uma das Opções Abaixo ---*")
    print("1 - Listar Todos os Alunos")
    print("2 - Listar Todos os Cidades")
    print("0 - Sair")

    opcao_bruta = input("Opcao: ")

    opcao_tratada = re.sub(padrao_num, '', opcao_bruta)

    match opcao_tratada:
        case '1':
            buscarAluno(arvore_alunos, arvore_cidades)
        case '0':
            print('Saindo do Sistema')
            break
        case _:
            print('Escolha uma opcao valida')
