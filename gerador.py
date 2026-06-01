class GeradorYAML:
    def __init__(self, tokens):
        self.tokens = tokens
        self.yaml_output = ""

    def gerar(self):
        print("--- INICIANDO A GERAÇÃO DE CÓDIGO (YAML) ---")
        
        alias = "Automacao Homi"
        trigger = {}
        conditions = []
        actions = []

        # Como as fases anteriores já garantiram que o código é 100% válido,
        # podemos fazer uma varredura direta nos tokens para extrair os dados.
        i = 0
        while i < len(self.tokens):
            tipo, valor, _ = self.tokens[i]

            if tipo == 'AUTOMACAO':
                alias = self.tokens[i+1][1].replace('"', '')
                i += 2
                continue

            elif tipo == 'QUANDO':
                i += 1
                # Gatilho de Horário: QUANDO horario for 18:00
                if self.tokens[i][0] == 'TIPO_GATILHO' and self.tokens[i][1] == 'horario':
                    tempo = self.tokens[i+2][1]
                    trigger = {'platform': 'time', 'at': tempo}
                    i += 3
                # Gatilho de Estado: QUANDO sensor.porta_entrada for aberto
                elif self.tokens[i][0] == 'ID_ENTIDADE':
                    entidade = self.tokens[i][1]
                    estado_homi = self.tokens[i+2][1]
                    # Mapeamento do estado Homi para o padrão binário do Home Assistant
                    estado_ha = 'on' if estado_homi in ['ligado', 'aberto', 'movimento'] else 'off'
                    trigger = {'platform': 'state', 'entity_id': entidade, 'to': estado_ha}
                    i += 3
                continue

            elif tipo == 'SE':
                # Condição: SE light.sala_estar estiver desligado
                entidade = self.tokens[i+1][1]
                estado_homi = self.tokens[i+3][1]
                estado_ha = 'on' if estado_homi in ['ligado', 'aberto', 'movimento'] else 'off'
                conditions.append({'condition': 'state', 'entity_id': entidade, 'state': estado_ha})
                i += 4
                
                # Trata condições adicionais encadeadas com 'E'
                while i < len(self.tokens) and self.tokens[i][0] == 'OP_LOGICO' and self.tokens[i][1] == 'E' and self.tokens[i+1][0] == 'ID_ENTIDADE':
                    entidade = self.tokens[i+1][1]
                    estado_homi = self.tokens[i+3][1]
                    estado_ha = 'on' if estado_homi in ['ligado', 'aberto', 'movimento'] else 'off'
                    conditions.append({'condition': 'state', 'entity_id': entidade, 'state': estado_ha})
                    i += 4
                continue

            elif tipo == 'ENTAO' or (tipo == 'OP_LOGICO' and valor == 'E'):
                # Ação: ENTAO ligar light.sala_estar  OU  E notificar "Mensagem"
                i += 1
                verbo = self.tokens[i][1]
                complemento = self.tokens[i+1][1]
                
                if verbo == 'notificar':
                    msg = complemento.replace('"', '')
                    actions.append({'service': 'notify.persistent_notification', 'data': {'message': msg}})
                else:
                    # Extrai o domínio da entidade (ex: 'light' de 'light.sala_estar')
                    dominio = complemento.split('.')[0]
                    acao_ha = 'turn_on' if verbo == 'ligar' else 'turn_off' if verbo == 'desligar' else 'toggle'
                    actions.append({
                        'service': f"{dominio}.{acao_ha}",
                        'target': {'entity_id': complemento}
                    })
                i += 2
                continue
            
            i += 1

        # --- CONSTRUÇÃO DA STRING FINAL YAML (Sintaxe Estrita) ---
        import random
        id_aleatorio = random.randint(1000000000, 9999999999)
        
        yaml = f"- id: '{id_aleatorio}'\n"
        yaml += f"  alias: \"{alias}\"\n"
        yaml += f"  description: \"Gerado automaticamente pelo Compilador Homi\"\n"
        yaml += f"  trigger:\n"
        yaml += f"  - platform: {trigger.get('platform')}\n"
        if trigger.get('platform') == 'time':
            yaml += f"    at: \"{trigger.get('at')}\"\n"
        else:
            yaml += f"    entity_id: {trigger.get('entity_id')}\n"
            yaml += f"    to: \"{trigger.get('to')}\"\n"

        if conditions:
            yaml += f"  condition:\n"
            for cond in conditions:
                yaml += f"  - condition: {cond['condition']}\n"
                yaml += f"    entity_id: {cond['entity_id']}\n"
                yaml += f"    state: \"{cond['state']}\"\n"

        yaml += f"  action:\n"
        for act in actions:
            yaml += f"  - service: {act['service']}\n"
            if 'target' in act:
                yaml += f"    target:\n"
                yaml += f"      entity_id: {act['target']['entity_id']}\n"
            elif 'data' in act:
                yaml += f"    data:\n"
                yaml += f"      message: \"{act['data']['message']}\"\n"
        
        self.yaml_output = yaml
        return yaml