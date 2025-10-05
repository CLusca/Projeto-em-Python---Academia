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

def carregar_json():
    dados = {
        'alunos': carregarDados('./dados/alunos.json'),
        'cidades': carregarDados('./dados/cidade.json'),
        'professores': carregarDados('./dados/professores.json'),
        'modalidades': carregarDados('./dados/modalidades.json'),
        'matriculas': carregarDados('./dados/matriculas.json')
    }

    indices = {
        'alunos': criarIndice(dados['alunos'], "cod_Aluno"),
        'cidades': criarIndice(dados['cidades'], "cod_Cidade"),
        'professores': criarIndice(dados['professores'], "cod_Professor"),
        'modalidades': criarIndice(dados['modalidades'], "cod_Modalidade"),
        'matriculas': criarIndice(dados['matriculas'], "cod_Matricula")
    }

    arvores = {
        'alunos': construirArvore(indices['alunos']),
        'cidades': construirArvore(indices['cidades']),
        'professores': construirArvore(indices['professores']),
        'modalidades': construirArvore(indices['modalidades']),
        'matriculas': construirArvore(indices['matriculas'])
    }
    return {'dados': dados, 'indices': indices, 'arvores': arvores}

def contar_matriculas(cod_modalidade, lista_de_matriculas):
    contador = 0
    cod_modalidade_int = int(cod_modalidade)
    for matricula in lista_de_matriculas:
        if int(matricula['cod_Modalidade']) == cod_modalidade_int:
            contador += 1
    return contador


def verificar_vagas_modalidade(arvore_modalidades, dados_modalidades, dados_matriculas):
    os.system('cls')
    print("--- Verificar Vagas por Modalidade ---")
    while True:
        cod_mod = input("Digite o código da modalidade para verificar as vagas: ").strip()
        if cod_mod.isdigit():
            break
        else:
            print("Código inválido. Por favor, digite apenas números.")
    indice_modalidade = consultar(arvore_modalidades, cod_mod)
    
    if indice_modalidade is None:
        print("\nModalidade não encontrada.")
        time.sleep(2)
        return
    modalidade = dados_modalidades[indice_modalidade]
    limite_vagas = int(modalidade['limite_Alunos'])
    alunos_matriculados = contar_matriculas(cod_mod, dados_matriculas)
    vagas_disponiveis = limite_vagas - alunos_matriculados
    
    print(f"\n--- Relatório de Vagas para: {modalidade['descricao']} ---")
    print(f"Limite de Vagas na Modalidade: {limite_vagas}")
    print(f"Total de Alunos Já Matriculados: {alunos_matriculados}")
    
    if vagas_disponiveis > 0:
        print(f"Vagas Disponíveis: {vagas_disponiveis}")
    else:
        print("Não há vagas disponíveis para esta modalidade.")
    continuar = input("\nPressione Enter para continuar...")
    match continuar:
        case '':
            return

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

def salvar_dados(caminho_arquivo, dados):
    try:
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"\nERRO CRÍTICO ao salvar o arquivo {caminho_arquivo}: {e}")
        return False

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

    nome = dados[raiz.indice].get('nome') or dados[raiz.indice].get('descricao')
    
    print(f"Descrição: {nome}\nCodigo: {raiz.codigo}\n")
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
            input("\nAperte Enter para continuar...")
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

def adicionar_matricula(dados_globais):
    os.system('cls')
    print("--- Adicionar Nova Matrícula ---")
    while True:
        cod_mat_input = input("Digite o código da nova matrícula: ").strip()
        if not cod_mat_input.isdigit():
            print("O código deve ser um número.")
            continue
        if consultar(dados_globais['arvores']['matriculas'], cod_mat_input) is not None:
            print("Este código de matrícula já está em uso.")
            continue
        cod_mat_valido = cod_mat_input
        break
    while True:
        cod_aluno_input = input("Digite o CÓDIGO do aluno a ser matriculado: ").strip()
        indice_aluno = consultar(dados_globais['arvores']['alunos'], cod_aluno_input)
        if indice_aluno is None:
            print("Aluno não encontrado. Tente novamente.")
            continue
        aluno = dados_globais['dados']['alunos'][indice_aluno]
        indice_cidade = consultar(dados_globais['arvores']['cidades'], aluno['cod_Cidade'])
        cidade_nome = dados_globais['dados']['cidades'][indice_cidade]['descricao'] if indice_cidade is not None else "N/A"
        print(f"\nAluno encontrado: {aluno['nome']} (de {cidade_nome})")
        cod_aluno_valido = cod_aluno_input
        break
    modalidade_selecionada = None
    while True:
        cod_mod_input = input("Digite o código da modalidade: ").strip()
        indice_modalidade = consultar(dados_globais['arvores']['modalidades'], cod_mod_input)
        if indice_modalidade is None:
            print("Modalidade não encontrada.")
            continue
        modalidade = dados_globais['dados']['modalidades'][indice_modalidade]
        print(f"\nModalidade encontrada: {modalidade['descricao']}")
        limite_vagas = int(modalidade['limite_Alunos'])
        alunos_matriculados = contar_matriculas(cod_mod_input, dados_globais['dados']['matriculas'])
        if alunos_matriculados >= limite_vagas:
            print(f"TURMA LOTADA! (Limite: {limite_vagas}, Ocupadas: {alunos_matriculados})")
            if input("Deseja tentar outra modalidade? (s/n): ").lower() != 's':
                print("Matrícula cancelada.")
                continuar = input("\nAperte Enter para continuar...")
                match continuar:
                    case '':
                        return False
        else:
            print(f"Vaga disponível! (Limite: {limite_vagas}, Ocupadas: {alunos_matriculados})")
            cod_mod_valido = cod_mod_input
            modalidade_selecionada = modalidade
            break
    while True:
        quant_aulas = input("Digite a quantidade de aulas: ").strip()
        if quant_aulas.isdigit():
            quant_aulas_valida = int(quant_aulas)
            break
        else:
            print("A quantidade de aulas deve ser um número.")
    valor_aula = float(modalidade_selecionada['valor_Aula'])
    valor_total = valor_aula * quant_aulas_valida
    print(f"\nValor a ser pago ({quant_aulas_valida} aulas * R${valor_aula:.2f}): R$ {valor_total:.2f}")
    if input("Confirmar matrícula com este valor? (s/n): ").lower() != 's':
        print("Matrícula cancelada.")
        continuar = input("\nAperte Enter para continuar...")
        match continuar:
            case '':
                return False
        return False
    nova_matricula = {
        "cod_Matricula": cod_mat_valido,
        "cod_Aluno": cod_aluno_valido,
        "cod_Modalidade": cod_mod_valido,
        "quant_Aulas": str(quant_aulas_valida)
    }
    lista_matriculas = dados_globais['dados']['matriculas']
    lista_matriculas.append(nova_matricula)
    if not salvar_dados('./dados/matriculas.json', lista_matriculas):
        print("Falha ao salvar a nova matrícula. Operação cancelada.")
        continuar = input("\nAperte Enter para continuar...")
        match continuar:
            case '':
                return False
    print("Atualizando total de alunos na modalidade...")
    indice_modalidade = consultar(dados_globais['arvores']['modalidades'], cod_mod_valido)
    if indice_modalidade is not None:
        dados_modalidades_atualizados = dados_globais['dados']['modalidades']
        total_atual = int(dados_modalidades_atualizados[indice_modalidade]['total_Alunos'])
        dados_modalidades_atualizados[indice_modalidade]['total_Alunos'] = str(total_atual + 1)
        salvar_dados('./dados/modalidades.json', dados_modalidades_atualizados)
    print("\nMatrícula realizada e total de alunos atualizado com sucesso!")
    continuar = input("\nAperte Enter para continuar...")
    match continuar:
        case '':
            return False
        
def remover_matricula(dados_globais):
    os.system('cls')
    print("--- Remover Matrícula ---")
    while True:
        cod_mat_input = input("Digite o código da matrícula: ").strip()

        if not cod_mat_input.isdigit():
            print("O código deve ser um número.")
            continue

        if consultar(dados_globais['arvores']['matriculas'], cod_mat_input) is not None:
            cod_mat_valido = cod_mat_input
            break
        else: 
            print(f"Matricula {cod_mat_input} não foi encontrada")
            continue


    lista_matriculas    = dados_globais['dados']['matriculas']
    indice_para_remover = None
    matricula_removida  = None

    for i, matricula in enumerate(lista_matriculas):
        if matricula['cod_Matricula'] == cod_mat_valido:
            indice_para_remover = i
            matricula_removida  = matricula
            break

    if indice_para_remover is None:
        print(f"\nMatrícula com código '{cod_mat_valido}' não encontrada.")
        input("Aperte Enter para continuar...")
        return

    print(f"Matrícula '{cod_mat_valido}' encontrada. Removendo...")
    lista_matriculas.pop(indice_para_remover)
    
    if not salvar_dados('./dados/matriculas.json', lista_matriculas):
        print("Falha ao remover a matrícula. Operação cancelada.")
        continuar = input("\nAperte Enter para continuar...")
        match continuar:
            case '':
                return False
            
    print("Atualizando total de alunos na modalidade...")
    cod_mod = matricula_removida['cod_Modalidade']
    
    indice_modalidade = consultar(dados_globais['arvores']['modalidades'], cod_mod)

    if indice_modalidade is not None:
        dados_modalidades = dados_globais['dados']['modalidades']
        total_atual       = int(dados_modalidades[indice_modalidade]['total_Alunos'])
        
        dados_modalidades[indice_modalidade]['total_Alunos'] = str(total_atual - 1)
        
        salvar_dados('./dados/modalidades.json', dados_modalidades)
        print("\nTotal de alunos na modalidade foi atualizado.")
    else:
        print(f"Aviso: A modalidade com código {cod_mod} não foi encontrada para atualizar o total de alunos.")

    print("\nOperação de remoção concluída com sucesso!")
    input("Aperte Enter para continuar...")

def buscarAluno(arvoreAluno, arvoreCidade, dadosAlunos, dadosCidades):
    os.system('cls')
    print("*--- Escolha uma das Opções Abaixo ---*")
    print(" ---* Buscar Aluno *---")
    print("\n1 - Listar Nomes")
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

def faturamento(arvoreModalidades, arvoreProfessores, arvoreCidades, dadosModalidade, dadosProfessores, dadosCidades, dadosMatriculas):
    os.system('cls')
    print('*--- Faturamento por Modalidades ---*')
    listarTudo(arvoreModalidades, dadosModalidade)
    cod_escolhido = input("\nCodigo: ")

    cod_tratado       = re.sub(padrao_num, '', cod_escolhido)
    indice_modalidade = consultar(arvoreModalidades, cod_tratado)

    if indice_modalidade is None:
        print("Nenhuma modalidade foi encontrada!")
        return

    modalidade = dadosModalidade[indice_modalidade]

    indice_professor = consultar(arvoreProfessores, modalidade['cod_Professor'])

    if indice_professor is None:
        print("Nenhum Professor foi encontrado!")
        return

    professor = dadosProfessores[indice_professor]

    indice_cidade = consultar(arvoreCidades, professor['cod_Cidade'])

    if indice_cidade is None:
        print("Nenhuma Cidade foi encontrada!")
        return
    
    cidade = dadosCidades[indice_cidade]
    
    print(f"Modalidade: {modalidade['descricao']}")
    print(f"Professor: {professor['nome']}")
    print(f"Cidade: {cidade['descricao']}")

    quantAulas = 0

    for matricula in dadosMatriculas:
        if matricula['cod_Modalidade'] == modalidade['cod_Modalidade']:
            quantAulas += int(matricula['quant_Aulas'])

    valor_faturado = int(modalidade['total_Alunos']) * (float(modalidade['valor_Aula']) * quantAulas)

    print(f"\n Valor Faturado: R$ {valor_faturado}")

    input("\nAperte Enter para continuar...")

def main ():
    os.system('cls')
    while True:
        dadosAlunos        = carregarDados('./dados/alunos.json')
        dadosCidades       = carregarDados('./dados/cidade.json')
        dadosProfessores   = carregarDados('./dados/professores.json')
        dadosModalidades   = carregarDados('./dados/modalidades.json')
        dadosMatriculas    = carregarDados('./dados/matriculas.json')

        indice_alunos      = criarIndice(dadosAlunos, "cod_Aluno")
        indice_cidades     = criarIndice(dadosCidades, "cod_Cidade")
        indice_professores = criarIndice(dadosProfessores, "cod_Professor")
        indice_modalidades = criarIndice(dadosModalidades, "cod_Modalidade")
        indice_matriculas  = criarIndice(dadosMatriculas, "cod_Matricula")

        arvore_alunos      = construirArvore(indice_alunos)
        arvore_cidades     = construirArvore(indice_cidades)
        arvore_professores = construirArvore(indice_professores)
        arvore_modalidades = construirArvore(indice_modalidades)
        arvore_matriculas  = construirArvore(indice_matriculas) 

        dados_gerais = carregar_json() 

        os.system('cls')
        print("*--- Escolha uma das Opções Abaixo ---*")
        print("1 - Listar Todos os Alunos")
        print("2 - Listar Todos os Professores")
        print("3 - Adicionar Novo Aluno")
        print("4 - Adicionar Novo Professor")
        print("5 - Adicionar Novo Cidade")
        print("6 - Adicionar Novo Modalidade")
        print("7 - Adicionar Nova Matricula")
        print("8 - Remover Matricula")
        print("9 - Faturamento por Modalidade")
        print("0 - Sair")

        opcao_bruta = input("\nOpcao: ")

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
                adicionar_matricula(dados_gerais)
            case '8':
                remover_matricula(dados_gerais)
            case '9':
                faturamento(arvore_modalidades, arvore_professores, arvore_cidades, dadosModalidades, dadosProfessores, dadosCidades, dadosMatriculas)
            case '0':
                print('Saindo do Sistema')
                break
            case _:
                print('Escolha uma opcao valida')

main()