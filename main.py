from lexico import analisador_lexico
from sintatico import AnalisadorSintatico
from semantico import AnalisadorSemantico

def main():
    # Vamos criar um código com um ERRO SEMÂNTICO propositado
    # Tentar "ligar" uma porta (sensor.porta_entrada)
    codigo_teste = """
    AUTOMACAO "Teste Semântico"
    QUANDO sensor.porta_entrada for ligado
    ENTAO ligar sensor.porta_entrada
    """

    print("========================================")
    print("      COMPILADOR HOMI - INICIADO        ")
    print("========================================\n")

    # FASE 1: Léxico
    tokens = analisador_lexico(codigo_teste)
    
    # FASE 2: Sintático
    parser = AnalisadorSintatico(tokens)
    sucesso_sintatico = parser.analisar()

    if sucesso_sintatico:
        # FASE 3: Semântico (Só corre se a sintaxe estiver correta)
        print("\n[FASE 3] A executar o Analisador Semântico...")
        semantico = AnalisadorSemantico(tokens)
        sucesso_semantico = semantico.analisar()
        
        if sucesso_semantico:
            print("\nRESULTADO FINAL: Pronto para gerar o YAML!")
        else:
            print("\nRESULTADO FINAL: Erros semânticos impedem a geração do YAML.")

if __name__ == "__main__":
    main()