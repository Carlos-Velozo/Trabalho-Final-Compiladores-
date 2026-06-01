class AnalisadorSemantico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.erros = []
        
        # 1. Tabela de Símbolos (Mock de entidades da "casa")
        # Num compilador real, isto poderia vir de uma API do Home Assistant.
        self.tabela_simbolos = {
            'light.sala_estar': 'light',
            'switch.ilha_interruptor_1': 'switch',
            'sensor.porta_entrada': 'binary_sensor',
            'sensor.temperatura_sala': 'sensor_num'
        }
        
        # 2. Regras de Consistência (Verificação de Tipos / Ações)
        # O que cada domínio pode FAZER (Verbos)
        self.acoes_permitidas = {
            'light': ['ligar', 'desligar', 'alternar'],
            'switch': ['ligar', 'desligar', 'alternar'],
            'binary_sensor': [], # Não podemos "ligar" uma porta
            'sensor_num': []
        }
        
        # O que cada domínio pode SENTIR (Estados)
        self.estados_permitidos = {
            'light': ['ligado', 'desligado'],
            'switch': ['ligado', 'desligado'],
            'binary_sensor': ['aberto', 'fechado', 'movimento', 'ocioso']
        }

    def reportar_erro(self, mensagem, linha):
        erro = f"[ERRO SEMÂNTICO] Linha {linha}: {mensagem}"
        print(erro)
        self.erros.append(erro)

    def analisar(self):
        print("--- INICIANDO ANÁLISE SEMÂNTICA ---")
        
        entidade_contexto = None # Guarda a última entidade lida para validar o seu estado depois

        for i, token in enumerate(self.tokens):
            tipo = token[0]
            valor = token[1]
            linha = token[2]

            # Regra 1: A Entidade existe na Tabela de Símbolos?
            if tipo == 'ID_ENTIDADE':
                entidade_contexto = valor
                if valor not in self.tabela_simbolos:
                    self.reportar_erro(f"Entidade '{valor}' não declarada na Tabela de Símbolos.", linha)
                    continue

            # Regra 2: Validação de Ações (Verbos)
            elif tipo == 'VERBO_ACAO' and valor != 'notificar':
                # Olha para o próximo token para ver quem vai sofrer a ação
                if i + 1 < len(self.tokens) and self.tokens[i+1][0] == 'ID_ENTIDADE':
                    alvo = self.tokens[i+1][1]
                    if alvo in self.tabela_simbolos:
                        dominio = self.tabela_simbolos[alvo]
                        if valor not in self.acoes_permitidas.get(dominio, []):
                            self.reportar_erro(f"Incompatibilidade de Tipo: Não é possível '{valor}' a entidade '{alvo}' (Domínio: {dominio}).", linha)

            # Regra 3: Validação de Estados (Gatilhos e Condições)
            elif tipo == 'ESTADO':
                if entidade_contexto and entidade_contexto in self.tabela_simbolos:
                    dominio = self.tabela_simbolos[entidade_contexto]
                    if valor not in self.estados_permitidos.get(dominio, []):
                        self.reportar_erro(f"Incompatibilidade de Tipo: A entidade '{entidade_contexto}' ({dominio}) não suporta o estado '{valor}'.", linha)

        if len(self.erros) == 0:
            print("Análise Semântica concluída com SUCESSO! A lógica está consistente.")
            return True
        else:
            print(f"Falha na Análise Semântica. Foram encontrados {len(self.erros)} erros.")
            return False