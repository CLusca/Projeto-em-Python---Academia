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
            indice[item[cod_Tipo].strip()] = i
        else:
            indice[item[cod_Tipo].strip()] = i
    return indice

class No:
    def __init__(raiz, codigo, indice):
        raiz.codigo    = codigo
        raiz.esquerda = None
        raiz.direita  = None
        raiz.indice   = indice

def construirArvore(indice):
    raiz = None
    for codigo, indice_json in indice.items():
        raiz = inserir(raiz,codigo, indice_json)
    return raiz

def inserir(raiz, codigo, indice):
    if raiz is None:
        return No(codigo, indice)
    if codigo < raiz.codigo:
        raiz.esquerda = inserir(raiz.esquerda, codigo, indice)
    elif codigo > raiz.codigo:
        raiz.direita = inserir(raiz.direita, codigo, indice)
    return raiz

def consultar(raiz, valor_buscado):
    if raiz is None:
        return None
    if raiz.codigo is None:
        print("Valor nao encontrado")
        return raiz
    if raiz.codigo == valor_buscado:
        return raiz.indice
    elif valor_buscado < raiz.codigo:
        return consultar(raiz.esquerda, valor_buscado)
    return consultar(raiz.direita, valor_buscado)

def exclusão (raiz, valor):
    if raiz is None:
        return raiz
    if valor < raiz.codigo < raiz.indice:
        raiz.esquerda = exclusão(raiz.esquerda, valor)
    elif valor > raiz.codigo > raiz.indice:
        raiz.direita = exclusão(raiz.direita, valor)
    else:
        raiz.codigo = None
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
    
def listarTudo(raiz, dados):
    if raiz is None:
        print ("Nada encontrado")
        return
    elif raiz.esquerda is not None:
        listarTudo(raiz.esquerda, dados)
    print(f"Indice: {raiz.indice}\nDescrição: {dados[raiz.indice]['nome' or 'descricao']}\nCodigo: {raiz.codigo}\n")
    if raiz.direita is not None:
        listarTudo(raiz.direita, dados)

def adicionar_aluno(caminho_arquivo, raiz):
    os.system('cls')
    print("--- Adicionar Novo Aluno ---")
    
    while True:
        os.system('cls')
        cod_aluno = input("Digite o CÓDIGO do novo aluno: ").strip()
        consulta_codigo = consultar(raiz, cod_aluno)
        if cod_aluno.isdigit() == False:
            print("Código inválido, deve ser um número")
            continuar = input("\nAperte Enter para continuar...")
            match continuar:
                case '':
                    continue
        if consulta_codigo is not None:
            os.system('cls')
            print("Código já existe, tente outro")
            continuar = input("\nAperte Enter para continuar...")
            match continuar:
                case '':
                    continue
        else:
            cod_aluno_livre = cod_aluno
            break

    nome_aluno = input("Digite o nome do novo aluno: ").strip().title()
    data_nasc = input("Digite a data de nacimento (dd-mm-aaaa): ").strip()
    while True:
        try:
            peso_aluno = float(input("Digite o peso (ex: 75.5): ").strip())
            altura_aluno = float(input("Digite a altura (ex: 1.80): ").strip())
            break
        except ValueError:
            print("Peso e altura devem ser números. Tente novamente.")

    cod_cidade = input(f"Digite o código da cidade: ").strip()
    novo_aluno = {
        "cod_Aluno": cod_aluno_livre,
        "nome": nome_aluno,
        "cod_Cidade": cod_cidade,
        "data_Nascimento": data_nasc,
        "peso": peso_aluno,
        "altura": altura_aluno
    }
    lista_de_alunos = carregarDados(caminho_arquivo)
    lista_de_alunos.append(novo_aluno)
    try:
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(lista_de_alunos, f, indent=4, ensure_ascii=False)
        
        print("\nAluno adicionado")
    except IOError as e:
        print(f"\nErro ao salvar o arquivo")

def adicionar_professor(caminho_arquivo, raiz):
    os.system('cls')
    print("--- Adicionar Novo Professor ---")
    
    while True:
        os.system('cls')
        cod_prof = input("Digite o código do novo professor: ").strip()
        consulta_codigo = consultar(raiz, cod_prof)
        if cod_prof.isdigit() == False:
            print("Código inválido, deve ser um número")
            continuar = input("\nAperte Enter para continuar...")
            match continuar:
                case '':
                    continue
        if consulta_codigo is not None:
            os.system('cls')
            print("Código já existe, tente outro")
            continuar = input("\nAperte Enter para continuar...")
            match continuar:
                case '':
                    continue
        else:
            cod_prof_livre = cod_prof
            break

    nome_prof = input("Digite o nome do novo professor: ").strip().title()
    rua = input("Digite a rua do novo professor: ").strip().title()
    bairro = input("Digite o bairro do novo professor: ").strip().title()
    numero = input("Digite o número da casa do novo professor: ").strip()
    telefone = input("Digite o telefone do novo professor: ").strip()
    cod_cidade = input(f"Digite o código da cidade: ").strip()
    novo_prof = {
        "cod_Professor": cod_prof_livre,
        "nome": nome_prof,
        "rua": rua,
        "bairro": bairro,
        "numero": numero,
        "telefone": telefone,
        "cod_Cidade": cod_cidade
    }
    lista_de_professores = carregarDados(caminho_arquivo)
    lista_de_professores.append(novo_prof)
    try:
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(lista_de_professores, f, indent=4, ensure_ascii=False)
        
        print("\nProfessor adicionado")
    except IOError as e:
        print(f"\nErro ao salvar o arquivo")

def adicionar_cidade(caminho_arquivo, raiz):
    os.system('cls')
    print("--- Adicionar Nova Cidade ---")
    
    while True:
        os.system('cls')
        cod_cid = input("Digite o código da nova cidade: ").strip()
        consulta_codigo = consultar(raiz, cod_cid)
        if cod_cid.isdigit() == False:
            print("Código inválido, deve ser um número")
            continuar = input("\nAperte Enter para continuar...")
            match continuar:
                case '':
                    continue
        if consulta_codigo is not None:
            os.system('cls')
            print("Código já existe, tente outro")
            continuar = input("\nAperte Enter para continuar...")
            match continuar:
                case '':
                    continue
        else:
            cod_cid_livre = cod_cid
            break

    nome_cid = input("Digite o nome da nova cidade: ").strip().title()
    estado = input("Digite a UF seguindo este modelo - (SP): ").strip().upper()
    nova_cid = {
        "cod_Cidade": cod_cid_livre,
        "descricao": nome_cid,
        "estado": estado,
    }
    lista_de_cidades = carregarDados(caminho_arquivo)
    lista_de_cidades.append(nova_cid)
    try:
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(lista_de_cidades, f, indent=4, ensure_ascii=False)
        
        print("\nCidade adicionada")
    except IOError as e:
        print(f"\nErro ao salvar o arquivo")

def adicionar_modalidade(caminho_arquivo, raiz):
    os.system('cls')
    print("--- Adicionar Nova Modalidade ---")
    
    while True:
        os.system('cls')
        cod_mod = input("Digite o código da nova modalidade: ").strip()
        consulta_codigo = consultar(raiz, cod_mod)
        if cod_mod.isdigit() == False:
            print("Código inválido, deve ser um número")
            continuar = input("\nAperte Enter para continuar...")
            match continuar:
                case '':
                    continue
        if consulta_codigo is not None:
            os.system('cls')
            print("Código já existe, tente outro")
            continuar = input("\nAperte Enter para continuar...")
            match continuar:
                case '':
                    continue
        else:
            cod_mod_livre = cod_mod
            break

    desc = input("Digite a descrição da modalidade: ").strip().upper()
    cod_prof = input("Digite o código do professor responsável: ").strip()
    valor_aula = input("Digite o valor da aula (ex: 95.00): ").strip()
    limite_alunos = input("Digite o limite de alunos (ex: 100): ").strip()
    total_alunos = input("Digite o total de alunos matriculados: ").strip()
    nova_mod = {
        "cod_Modalidade": cod_mod_livre,
        "descricao": desc,
        "cod_Professor": cod_prof,
        "valor_Aula": valor_aula,
        "limite_Alunos": limite_alunos,
        "total_Alunos": total_alunos,
    }
    lista_de_modalidades = carregarDados(caminho_arquivo)
    lista_de_modalidades.append(nova_mod)
    try:
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(lista_de_modalidades, f, indent=4, ensure_ascii=False)
        
        print("\nModalidade adicionada")
    except IOError as e:
        print(f"\nErro ao salvar o arquivo")

def adicionar_matricula(caminho_arquivo, raiz):
    os.system('cls')
    print("--- Adicionar Nova Matricula ---")
    
    while True:
        os.system('cls')
        cod_mat = input("Digite o código da nova matricula: ").strip()
        consulta_codigo = consultar(raiz, cod_mat)
        if cod_mat.isdigit() == False:
            print("Código inválido, deve ser um número")
            continuar = input("\nAperte Enter para continuar...")
            match continuar:
                case '':
                    continue
        if consulta_codigo is not None:
            os.system('cls')
            print("Código já existe, tente outro")
            continuar = input("\nAperte Enter para continuar...")
            match continuar:
                case '':
                    continue
        else:
            cod_mat_livre = cod_mat
            break

    cod_aluno = input("Digite o codigo do aluno: ").strip()
    cod_mod = input("Digite o codigo da modalidade: ").strip()
    quant_aulas = input("Digite a quantidade de aulas: ").strip()
    nova_mat = {
        "cod_Matricula": cod_mat_livre,
        "cod_Aluno": cod_aluno,
        "cod_Modalidade": cod_mod,
        "quant_Aulas": quant_aulas,
    }
    lista_de_matriculas = carregarDados(caminho_arquivo)
    lista_de_matriculas.append(nova_mat)
    try:
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(lista_de_matriculas, f, indent=4, ensure_ascii=False)
        
        print("\nMatricula adicionada")
    except IOError as e:
        print(f"\nErro ao salvar o arquivo")

def buscarAluno(arvoreAluno, arvoreCidade, dadosAlunos, dadosCidades):
    os.system('cls')
    print("*--- Escolha uma das Opções Abaixo ---*")
    print(" ---* Buscar Aluno *---")
    print("\n1 - Listar Indices e Nomes")
    print("2 - Buscar por Codigo")
    print("0 - Retornar")
    opcao_bruta = input("Opcao: ")

    opcao_tratada = re.sub(padrao_num, '', opcao_bruta)

    
    match opcao_tratada:
        case '1':
            os.system('cls')
            listarTudo (arvoreAluno, dadosAlunos)
            continuar = input("\nAperte Enter para continuar...")
            match continuar:
                case '':
                    return
                
        case '2':
            os.system('cls')
            input_nome = input("Codigo do Aluno: ").strip()
            if input_nome.isdigit() == False:
                print("Codigo invalido")
                return
            indice_consulta = consultar (arvoreAluno, input_nome)
            aluno = dadosAlunos[indice_consulta]
            if indice_consulta is not None:
                        os.system('cls')
                        print("\n--- Dados do Aluno ---")
                        print(f"Codigo do Aluno: {aluno['cod_Aluno']}")
                        print(f"Nome do Aluno: {aluno['nome']}")
                        print(f"Data de Nascimento: {aluno['data_Nascimento']}")
                        indice_cidade = consultar(arvoreCidade,aluno['cod_Cidade'])
                        if indice_cidade is not None:
                            cidade = dadosCidades[indice_cidade]
                            print(f"Cidade: {cidade['descricao']}")
                            print(f"Estado: {cidade['estado']}")
                        print (f"Peso: {aluno['peso']} Kg")
                        print (f"Altura: {aluno['altura']} m")
                        imc = round(aluno['peso'] / (aluno['altura'] * aluno['altura']),2)
                        print (f"IMC: {imc}")
                        if imc < 18.5:
                            print("Classificação do IMC: Abaixo do peso")
                        elif 18.5 <= imc <= 24.9:
                            print("Classificação do IMC: Peso normal")
                        elif 25 <= imc <= 29.9:
                            print("Classificação do IMC: Sobrepeso")
                        else:
                            print("Classificação do IMC: Obesidade")

                        continuar = input("\nAperte Enter para continuar...")
                        match continuar:
                            case '':
                                return
            
        case '0':
            return

def buscarProfessor(arvoreProfessor, arvoreCidade, dadosProfessor, dadosCidades):
    os.system('cls')
    print("*--- Escolha uma das Opções Abaixo ---*")
    print(" ---* Buscar Professor *---")
    print("\n1 - Listar Indices e Nomes")
    print("2 - Buscar por Codigo")
    print("0 - Retornar")
    opcao_bruta = input("Opcao: ")

    opcao_tratada = re.sub(padrao_num, '', opcao_bruta)

    
    match opcao_tratada:
        case '1':
            os.system('cls')
            listarTudo (arvoreProfessor, dadosProfessor)
            continuar = input("\nAperte Enter para continuar...")
            match continuar:
                case '':
                    return
                
        case '2':
            os.system('cls')
            input_nome = input("Codigo do Professor: ").strip()
            if input_nome.isdigit() == False:
                print("Codigo invalido")
                return
            indice_consulta = consultar (arvoreProfessor, input_nome)
            professor = dadosProfessor[indice_consulta]
            if indice_consulta is not None:
                        os.system('cls')
                        print("\n--- Dados do Professor ---")
                        print(f"Codigo do Professor: {professor['cod_Professor']}")
                        print(f"Nome do Professor: {professor['nome']}")
                        print(f"Rua: {professor['rua']}, Nº {professor['numero']}")
                        print(f"Bairro: {professor['bairro']}")
                        indice_cidade = consultar(arvoreCidade,professor['cod_Cidade'])
                        if indice_cidade is not None:
                            cidade = dadosCidades[indice_cidade]
                            print(f"Cidade: {cidade['descricao']}")
                            print(f"Estado: {cidade['estado']}")
                        print (f"Telefone: {professor['telefone']}")

                        continuar = input("\nAperte Enter para continuar...")
                        match continuar:
                            case '':
                                return
            
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

def main ():
    os.system('cls')
    while True:
        dadosAlunos      = carregarDados('./dados/alunos.json')
        dadosCidades     = carregarDados('./dados/cidade.json')
        dadosProfessores = carregarDados('./dados/professores.json')
        dadosModalidades = carregarDados('./dados/modalidades.json')
        dadosMatriculas  = carregarDados('./dados/matriculas.json')

        indice_alunos = criarIndice(dadosAlunos, "cod_Aluno")
        indice_cidades = criarIndice(dadosCidades, "cod_Cidade")
        indice_professores = criarIndice(dadosProfessores, "cod_Professor")
        indice_modalidades = criarIndice(dadosModalidades, "cod_Modalidade")
        indice_matriculas =criarIndice(dadosMatriculas, "cod_Matricula")

        arvore_alunos = construirArvore(indice_alunos)
        arvore_cidades = construirArvore(indice_cidades)
        arvore_professores = construirArvore(indice_professores)
        arvore_modalidades = construirArvore(indice_modalidades)
        arvore_matriculas = construirArvore(indice_matriculas)   

        os.system('cls')
        print("*--- Escolha uma das Opções Abaixo ---*")
        print(indice_alunos)
        print("1 - Listar Todos os Alunos")
        print("2 - Listar Todos os Professores")
        print("3 - Adicionar Novo Aluno")
        print("4 - Adicionar Novo Professor")
        print("5 - Adicionar Novo Cidade")
        print("6 - Adicionar Novo Modalidade")
        print("7 - Adicionar Nova Matricula")
        print("0 - Sair")

        opcao_bruta = input("Opcao: ")

        opcao_tratada = re.sub(padrao_num, '', opcao_bruta)

        match opcao_tratada:
            case '1':
                buscarAluno(arvore_alunos, arvore_cidades, dadosAlunos, dadosCidades)
            case '2':
                buscarProfessor(arvore_professores, arvore_cidades, dadosProfessores, dadosCidades)  
            case '3':
                adicionar_aluno('./dados/alunos.json', arvore_alunos)
            case '4':
                adicionar_professor('./dados/professores.json', arvore_professores)
            case '5':
                adicionar_cidade('./dados/cidade.json', arvore_cidades)
            case '6':
                adicionar_modalidade('./dados/modalidades.json', arvore_modalidades)
            case '7':
                adicionar_matricula('./dados/matriculas.json', arvore_matriculas)  
            case '0':
                print('Saindo do Sistema')
                break
            case _:
                print('Escolha uma opcao valida')

main()