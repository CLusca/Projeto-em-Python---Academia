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
        if item[cod_Tipo] is not None:
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

def consultar(raiz, valorBuscado):
    if raiz is None or raiz.valor == valorBuscado:
        return raiz
    elif valorBuscado < raiz.valor:
        return consultar(raiz.esquerda, valorBuscado)
    return consultar(raiz.direita, valorBuscado)

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
    
def listarTudo(listaDeDados):
    resultados = []

    for registro in listaDeDados:

        if registro is None:
            continue
        
        resultados.append(registro)

    if resultados == []:
        return 0
    else: 
        return resultados

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

def alunos():
    while True:
        os.system('cls')
        
        entrada_bruta = input("Insira o Nome do Aluno(ou 0 para Sair): ")

        if entrada_bruta == "0":
            return

        entrada_tratado = re.sub(padrao_str, '', entrada_bruta)
        json_aluno         = buscaExaustiva(dadosAlunos, "nome", entrada_tratado)
        
        if json_aluno == 0:
            print("Nenhum Aluno Encontrado!")
            time.sleep(2)
            continue

        nome_aluno         = json_aluno['nome']
        codigo_cidade      = json_aluno['cod_cidade']
        imc_aluno          = round(json_aluno['peso'] / (json_aluno['altura'] * json_aluno['altura']), 2)

        classif_imc = "Baixo Peso"

        if imc_aluno >= 18.6 and imc_aluno <= 24.9 :
            classif_imc = "Peso Normal"
        elif imc_aluno >= 25 and imc_aluno <= 29.9:
            classif_imc = "Sobrepeso"
        elif(imc_aluno >= 30):
            classif_imc = "Obeso"

        if codigo_cidade == 0:
            print("Não Encontrei, Desculpa")
        else: 
            json_cidade = buscaExaustiva(dadosCidades, 'cod_cidade', codigo_cidade)
            print(f"Aluno: " + nome_aluno)
            print(f"IMC: " + str(imc_aluno))
            print(f"Classificacao IMC: " + str(classif_imc))
            print("Cidade: " + json_cidade['descricao'] + " - Estado: " + json_cidade['estado'])

            contador_5_segundos()
            continue
            
def professor():
    while True:
        os.system('cls')
        
        entrada_bruta    = input("Insira o Nome do Professor: ")
        entrada_tratada  = re.sub(padrao_str, '', entrada_bruta)
        json_professor   = buscaExaustiva(dadosProfessores, "nome", entrada_tratada)

        if json_professor == 0:
            print("Nenhum Professor Encontrado!")
            time.sleep(2)
            continue

        nome_professor   = json_professor['nome']
        codigo_cidade    = json_professor['cod_cidade']

        if codigo_cidade == 0:
            print("Não Encontrei, Desculpa")
        else: 
            json_cidade = buscaExaustiva(dadosCidades, 'cod_cidade', codigo_cidade)
            print(f"Aluno: " + nome_professor)
            print("Cidade: " + json_cidade['descricao'] + " - Estado: " + json_cidade['estado'])

            contador_5_segundos()
            continue

def modalidades():
    while True:
        os.system('cls')
        print(listarTudo(dadosModalidades))
        # print("*--- Escolha uma das Opções Abaixo ---*")
        # print("1 - Somenta Academia")
        # print("2 - Academia e Jiu Jitsu")
        # print("0 - Sair")

        entrada_bruta    = input("Opcao: ")
        entrada_tratada  = re.sub(padrao_str, '', entrada_bruta)                

        json_modalidade  = buscaExaustiva(dadosProfessores, "nome", entrada_tratada)

        if json_modalidade == 0:
            print("Nenhuma Modalidade Encontrada!")
            time.sleep(2)
            continue

        nome_professor   = json_modalidade['nome']
        codigo_cidade    = json_modalidade['cod_cidade']

        if codigo_cidade == 0:
            print("Não Encontrei, Desculpa")
        else: 
            json_cidade = buscaExaustiva(dadosCidades, 'cod_cidade', codigo_cidade)
            print(f"Aluno: " + nome_professor)
            print("Cidade: " + json_cidade['descricao'] + " - Estado: " + json_cidade['estado'])

            contador_5_segundos()
            continue

dadosAlunos      = carregarDados('./dados/alunos.json')
dadosCidades     = carregarDados('./dados/cidade.json')
dadosProfessores = carregarDados('./dados/professores.json')
dadosModalidades = carregarDados('./dados/modalidades.json')
dadosMatriculas  = carregarDados('./dados/matriculas.json')



while True:   
    print("*--- Escolha uma das Opções Abaixo ---*")
    print("1 - Aluno")
    print("2 - Professor")
    print("3 - Modalidades")
    print("0 - Sair")

    opcao_bruta = input("Opcao: ")

    opcao_tratada = re.sub(padrao_num, '', opcao_bruta)

    match opcao_tratada:
        case '1':
            alunos()
        case '2':
            professor()
        case '3':
            modalidades()
        case '0':
            print('Saindo do Sistema')
            break
        case _:
            print('ESCOLHA CERTO VIADO')









# print("--- Buscando aluno com nome 'Camila' ---")
# alunosEncontrados = buscaExaustiva(dadosAlunos, "nome", "camila")
# if alunosEncontrados:
#     print(f"Encontrado(s) {len(alunosEncontrados)} aluno(s): {alunosEncontrados}")
# else:
#     print("Nenhum aluno encontrado.")

# print("\n--- Buscando professor com nome 'Weverton' ---")
# professoresEncontrados = buscaExaustiva(dadosProfessores, "nome", "weverton")
# if professoresEncontrados:
#     print(f"Encontrado(s) {len(professoresEncontrados)} professor(es): {professoresEncontrados}")
# else:
#     print("Nenhum professor encontrado.")

# print("\n--- Buscando cidades do estado 'SP' ---")
# cidadesEncontradas = buscaExaustiva(dadosCidades, "estado", "sp")
# if cidadesEncontradas:
#     print(f"Encontrada(s) {len(cidadesEncontradas)} cidade(s): {cidadesEncontradas}")
# else:
#     print("Nenhuma cidade encontrada.")
    
# print("\n--- Buscando modalidade com descrição 'Somente Academia' ---")
# modalidadesEncontradas = buscaExaustiva(dadosModalidades, "descricao", "somente academia")
# if modalidadesEncontradas:
#     print(f"Encontrada(s) {len(modalidadesEncontradas)} modalidade(s): {modalidadesEncontradas}")
# else:
#     print("Nenhuma modalidade encontrada.")

# print("\n--- Buscando matrículas do aluno com código 1 ---")
# matriculasEncontradas = buscaExaustiva(dadosMatriculas, "cod_Aluno", 1)
# if matriculasEncontradas:
#     print(f"Encontrada(s) {len(matriculasEncontradas)} matrícula(s): {matriculasEncontradas}")
# else:
#     print("Nenhuma matrícula encontrada.")





