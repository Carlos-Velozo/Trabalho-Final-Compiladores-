class AnalisadorSintatico:
    def __init__(self, tokens):
        # Adicionamos um token de Fim de Arquivo ($) para indicar o término
        self.tokens = tokens + [('EOF', '$', tokens[-1][2] if tokens else 1)]
        self.posicao = 0
        self.token_atual = self.tokens[self.posicao]
        
        # A Pilha inicia com o Fim de Arquivo e o Não-Terminal inicial
        self.pilha = ['$', 'Programa']
        
        # Tabela Preditiva LL(1) (Mapeamento das Regras)
        # Formato: tabela[Nao_Terminal][Token_Lido] = [Regras a empilhar]
        self.tabela = {
            'Programa': {
                'AUTOMACAO': ['AUTOMACAO', 'STRING', 'BlocoQuando', 'BlocoSe', 'BlocoEntao']
            },
            'BlocoQuando': {
                'QUANDO': ['QUANDO', 'RegraGatilho']
            },
            'RegraGatilho': {
                'TIPO_GATILHO': ['TIPO_GATILHO', 'TEMPO_EXATO'],
                'ID_ENTIDADE': ['ID_ENTIDADE', 'OPERADOR', 'ESTADO']
            },
            'BlocoSe': {
                'SE': ['SE', 'RegraCondicao'],
                'ENTAO': [] # Transição Epsilon (ε): Se ler ENTAO, o BlocoSe acaba vazio
            },
            'RegraCondicao': {
                'ID_ENTIDADE': ['ID_ENTIDADE', 'OPERADOR', 'ESTADO', 'MaisCondicoes']
            },
            'MaisCondicoes': {
                'OP_LOGICO': ['OP_LOGICO', 'RegraCondicao'],
                'ENTAO': [] # Epsilon
            },
            'BlocoEntao': {
                'ENTAO': ['ENTAO', 'Comando', 'MaisComandos']
            },
            'Comando': {
                'VERBO_ACAO': ['VERBO_ACAO', 'Complemento']
            },
            'Complemento': {
                'ID_ENTIDADE': ['ID_ENTIDADE'],
                'STRING': ['STRING']
            },
            'MaisComandos': {
                'OP_LOGICO': ['OP_LOGICO', 'Comando', 'MaisComandos'],
                'EOF': [] # Epsilon no final do arquivo
            }
        }

    def avancar_token(self):
        self.posicao += 1
        if self.posicao < len(self.tokens):
            self.token_atual = self.tokens[self.posicao]

    def modo_panico(self, tokens_sincronizacao):
        """
        Recuperação de Erros (Requisito C): 
        Descarta tokens até encontrar um ponto seguro para continuar a análise.
        """
        print(f"[ERRO SINTÁTICO] Modo Pânico ativado na linha {self.token_atual[2]}.")
        print(f"Descartando tokens até encontrar: {tokens_sincronizacao}")
        
        while self.token_atual[0] not in tokens_sincronizacao and self.token_atual[0] != 'EOF':
            print(f"  -> Descartando token ignorado: {self.token_atual[1]}")
            self.avancar_token()

    def analisar(self):
        print("--- INICIANDO ANÁLISE SINTÁTICA ---")
        
        while len(self.pilha) > 0:
            topo = self.pilha.pop()
            tipo_token_lido = self.token_atual[0]
            lexema_lido = self.token_atual[1]
            linha = self.token_atual[2]

            if topo == '$':
                if tipo_token_lido == 'EOF':
                    print("Análise Sintática concluída com SUCESSO!")
                    return True
                else:
                    print(f"[ERRO] Esperado fim de arquivo, mas encontrou '{lexema_lido}' na linha {linha}.")
                    return False

            # Se o topo for um Terminal
            elif topo.isupper() or topo == 'STRING': 
                if topo == tipo_token_lido:
                    print(f"  [Match Terminal] {topo} consumiu '{lexema_lido}'")
                    self.avancar_token()
                else:
                    print(f"[ERRO SINTÁTICO] Esperado '{topo}', mas encontrou '{lexema_lido}' na linha {linha}.")
                    # Ativa Modo Pânico: Tenta pular para o próximo bloco lógico seguro
                    self.modo_panico(['QUANDO', 'SE', 'ENTAO', 'EOF'])
            
            # Se o topo for um Não-Terminal (consulta a Tabela LL1)
            else:
                if tipo_token_lido in self.tabela.get(topo, {}):
                    producao = self.tabela[topo][tipo_token_lido]
                    print(f"[Derivação] {topo} -> {producao}")
                    
                    # Empilha a produção de trás para frente (LIFO)
                    for simbolo in reversed(producao):
                        self.pilha.append(simbolo)
                else:
                    print(f"[ERRO SINTÁTICO] Falha ao derivar '{topo}' com token '{lexema_lido}' na linha {linha}.")
                    self.modo_panico(['QUANDO', 'SE', 'ENTAO', 'EOF'])

        return True