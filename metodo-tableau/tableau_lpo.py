import re

REGEX_LITERAL = r"^~?[A-Z][a-zA-Z0-9]*\([a-zA-Z0-9,]+\)$"


def is_literal(formula):
    # Verifica se é um literal proposicional simples (P, ~P)
    if formula.isalpha() and formula.isupper():
        return True
    if formula.startswith('~') and formula[1:].isalpha() and formula[1:].isupper():
        return True
    # Verifica se é um literal de predicado (P(a), ~P(b))
    if re.match(REGEX_LITERAL, formula):
        return True
    return False


def not_literal(literal):
    if literal.startswith('~'):
        return literal[1:]
    else:
        return '~' + literal


def obter_constantes(ramo):
    constantes = set()
    for formula in ramo:
        # Procura conteúdo dentro de parênteses: P(termo)
        match = re.findall(r'\(([a-z0-9]+)\)', formula)
        for m in match:
            constantes.add(m)

    # Se não houver nenhuma constante no ramo, iniciamos com um padrão 'a'
    if not constantes:
        constantes.add('a')
    return constantes


def gerar_nova_constante(constantes_existentes):
    i = 1
    while True:
        cand = f"c{i}"
        if cand not in constantes_existentes:
            return cand
        i += 1


def substituir_variavel(formula, variavel, constante):
    # Remove o quantificador (Ax ou Ex)
    # Assume formato Ax(...) ou Ex(...)
    conteudo = formula[2:]

    # Remove parênteses externos do escopo se houver
    if conteudo.startswith('(') and conteudo.endswith(')'):
        conteudo = conteudo[1:-1]

    padrao = r'\b' + re.escape(variavel) + r'\b'
    nova_formula = re.sub(padrao, constante, conteudo)
    return nova_formula


def ramo_fechado(ramo):
    literais = [f for f in ramo if is_literal(f)]
    for lit in literais:
        negacao_literal = not_literal(lit)
        if negacao_literal in literais:
            return True
    return False


def aplica_regras(formula, constantes_no_ramo):
    # Tira parênteses externos
    if formula.startswith('(') and formula.endswith(')') and '(' not in formula[1:-1]:
        formula = formula.replace('(', '').replace(')', '')

    # --- REGRAS PROPOSICIONAIS ---

    if formula.startswith('~(') and formula.endswith(')'):
        sub_formula = formula[2:-1].strip()

        # Regra: ~(A v B) -> ~A, ~B
        if 'v' in sub_formula:
            print("Regra ~(A v B) aplicada")
            A, B = sub_formula.split('v', 1)
            return [['~' + A.strip(), '~' + B.strip()]]

        # Regra: ~(A > B) -> A, ~B
        elif '>' in sub_formula:
            print("Regra ~(A > B) aplicada")
            A, B = sub_formula.split('>', 1)
            return [[A.strip(), '~' + B.strip()]]

        # Regra: ~(A ^ B) -> ~A | ~B
        elif '^' in sub_formula:
            print("Regra ~(A ^ B) aplicada")
            A, B = sub_formula.split('^', 1)
            return [['~' + A.strip()], ['~' + B.strip()]]

        # Regra: ~Ax(P(x)) -> Ex(~P(x)) (Negação do Universal)
        elif sub_formula.startswith('A'):
            # ~Ax P(x) equivale a Ex ~P(x)
            print("Regra ~Ax aplicada")
            variavel = sub_formula[1]  # Pega 'x' de 'Ax'
            resto = sub_formula[2:]
            nova = f"E{variavel}(~{resto})"
            return [[nova]]

        # Regra: ~Ex(P(x)) -> Ax(~P(x)) (Negação do Existencial)
        elif sub_formula.startswith('E'):
            print("Regra ~Ex aplicada")
            variavel = sub_formula[1]
            resto = sub_formula[2:]
            nova = f"A{variavel}(~{resto})"
            return [[nova]]

    # Regra: A > B
    elif '>' in formula and not formula.startswith('A') and not formula.startswith('E'):
        print("Regra A > B aplicada")
        A, B = formula.split('>', 1)
        return [['~' + A.strip()], [B.strip()]]

    # Regra: A ^ B
    elif '^' in formula:
        print("Regra A ^ B aplicada")
        A, B = formula.split('^', 1)
        return [[A.strip(), B.strip()]]

    # Regra: A v B
    elif 'v' in formula:
        print("Regra A v B aplicada")
        A, B = formula.split('v', 1)
        return [[A.strip()], [B.strip()]]

    # Regra: ~~A
    elif formula.startswith('~~'):
        print("Regra ~~A aplicada")
        return [[formula[2:]]]

    # --- REGRAS DE PRIMEIRA ORDEM (QUANTIFICADORES) ---

    # Regra Existencial: Ex(P(x)) -> P(c_nova)
    # Substitui a variável por uma nova constante que não existe no ramo
    elif formula.startswith('E'):
        variavel = formula[1]
        nova_constante = gerar_nova_constante(constantes_no_ramo)
        print(f"Regra Existencial aplicada: Substituindo '{variavel}' por nova constante '{nova_constante}'")

        resultado = substituir_variavel(formula, variavel, nova_constante)
        return [[resultado]]

    # Regra Universal: Ax(P(x)) -> P(a), P(b), P(c)...
    # Substitui a variável por todas as constantes existentes no ramo
    elif formula.startswith('A'):
        variavel = formula[1]
        print(f"Regra Universal aplicada: Substituindo '{variavel}' pelas constantes {constantes_no_ramo}")

        instancias = []
        for constante in constantes_no_ramo:
            instancias.append(substituir_variavel(formula, variavel, constante))

        return [instancias]

    return []


def tableau_semantico_lpo(bd_formulas, query):
    formulas = bd_formulas.copy()

    # Formata a negação da pergunta corretamente
    if is_literal(query):
        formulas.append('~' + query)
    else:
        formulas.append('~(' + query + ')')

    ramos_abertos = [formulas]
    qtd_ramos_explorados = 0

    print(f"Iniciando Tableau LPO para: {ramos_abertos[0]}")

    # Limite de segurança para evitar loops infinitos
    MAX_ITERACOES = 150

    while ramos_abertos and qtd_ramos_explorados < MAX_ITERACOES:
        ramo_atual = ramos_abertos.pop(0)
        qtd_ramos_explorados += 1

        print(f"\n--- Iteração {qtd_ramos_explorados} ---")
        print(f"Ramo Atual: {ramo_atual}")

        if ramo_fechado(ramo_atual):
            print("RAMO FECHADO (Contradição Encontrada)")
            continue

        # Priorizar regras que não ramificam e Existenciais antes de Universais
        formulas_para_decompor = None

        # Proposicional e Existencial
        for formula in ramo_atual:
            if not is_literal(formula) and not formula.startswith('A'):
                formulas_para_decompor = formula
                break

        # Universais (Ax)
        if formulas_para_decompor is None:
            for formula in ramo_atual:
                if not is_literal(formula):
                    formulas_para_decompor = formula
                    break

        if formulas_para_decompor is None:
            print("RAMO ABERTO")
            return False

        constantes_no_ramo = obter_constantes(ramo_atual)

        ramo_atual.remove(formulas_para_decompor)

        sub_ramos = aplica_regras(formulas_para_decompor, constantes_no_ramo)

        if not sub_ramos:
            pass

        for sub_lista in sub_ramos:
            novo_ramo = ramo_atual + sub_lista
            ramos_abertos.append(novo_ramo)
            print(f"  -> Ramo atualizado: {novo_ramo}")

    if qtd_ramos_explorados >= MAX_ITERACOES:
        print("\nLIMITE DE ITERAÇÕES ATINGIDO!")
        return False

    print("\nTODOS OS RAMOS FECHARAM.")
    return True


# --- TESTES ---
print("*----------------------- TABLEAU LPO -----------------------*")
print("Sintaxe:")
print("  Ax(P(x)) -> Para todo x, P(x)")
print("  Ex(P(x)) -> Existe x tal que P(x)")
print("  P(a) -> Predicado com constante")
print("  A > B, A ^ B, A v B, ~A")

print("\n------ Teste: Silogismo de Sócrates ------")
# Ax(H(x)>M(x), H(socrates) |= M(socrates)
db1 = ['Ax(H(x)>M(x))', 'H(socrates)']
q1 = 'M(socrates)'
tableau_semantico_lpo(db1, q1)

print("\n------ Teste: Existencial ------")
# Ex(P(x)), Ax(P(x)>Q(x)) |= Ex(Q(x))
db2 = ['Ex(P(x))', 'Ax(P(x)>Q(x))']
q2 = 'Ex(Q(x))'
tableau_semantico_lpo(db2, q2)
