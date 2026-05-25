import re

# 1. Definição das Expressões Regulares para cada Token
# A ordem aqui importa! Coloque as mais específicas primeiro.
# Atualizado com unidades de tempo, operadores lógicos completos e afins
TOKEN_REGEX = [
    ('AUTOMACAO', r'\bAUTOMACAO\b'),
    ('QUANDO',    r'\bQUANDO\b'),
    ('SE',        r'\bSE\b'),
    ('ENTAO',     r'\bENTAO\b'),
    ('OP_LOGICO', r'\b(E|OU|NAO)\b'),                      # operadores lógicos
    ('VERBO_ACAO',r'\b(ligar|desligar|alternar|notificar)\b'),
    ('ESTADO',    r'\b(ligado|desligado|aberto|fechado|movimento|ocioso)\b'),
    ('OPERADOR',  r'\b(for|estiver)\b'),
    ('TIPO_GATILHO', r'\b(horario|tempo)\b'),
    ('TEMPO_EXATO',r'\b\d{2}:\d{2}\b'),                    # Ex: 05:00
    ('TEMPO_UNIT', r'\b\d+(s|m|min|h|hs)\b'),              # Ex: 10s, 5min, 2h
    ('ID_ENTIDADE',r'\b[a-z_]+\.[a-z0-9_]+\b'),            # Ex: sensor.temperature_living_room
    ('STRING',    r'".*?"'),                               # Ex: "Texto"
    ('ESPACO',    r'[ \t]+'),                              # Espaços (ignorados)
    ('NOVA_LINHA',r'\n'),                                  # Quebras de linha (contagem)
    ('COMENTARIO',r'#.*'),                                 # Comentários (ignorados)
    ('ERRO',      r'.')                                    # Pega qualquer caractere inválido que sobrou
]

def analisador_lexico(codigo_fonte):
    tokens_encontrados = []
    linha_atual = 1

    regex_combinada = '|'.join(f'(?P<{nome}>{padrao})' for nome, padrao in TOKEN_REGEX)
    
    for match in re.finditer(regex_combinada, codigo_fonte):
        tipo_token = match.lastgroup
        valor_token = match.group(tipo_token)

        if tipo_token == 'NOVA_LINHA':
            linha_atual += 1
        elif tipo_token == 'ESPACO' or tipo_token == 'COMENTARIO':
            continue
        elif tipo_token == 'ERRO': # TRATAMENTO DE ERRO LÉXICO
            print(f"[ERRO LÉXICO] Caractere ou palavra inválida '{valor_token}' na linha {linha_atual}")
            # Você pode escolher parar o compilador aqui com um 'return None' ou apenas avisar e continuar 
        else:
            tokens_encontrados.append((tipo_token, valor_token, linha_atual))
            
    return tokens_encontrados

# --- TESTANDO AS NOVAS REGRAS ---
codigo_teste = """
# Automação complexa
AUTOMACAO "Alarme Temperatura"
QUANDO sensor.temperature_living_room for 30
E tempo for 5min
ENTAO notificar "Atenção"
"""

tokens = analisador_lexico(codigo_teste)
for token in tokens:
    print(f"Token: {token[0]:<15} | Valor: {token[1]:<35} | Linha: {token[2]}")