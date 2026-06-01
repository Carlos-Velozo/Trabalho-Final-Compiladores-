from lexico import analisador_lexico
from sintatico import AnalisadorSintatico
from semantico import AnalisadorSemantico
from gerador import GeradorYAML  

def main():
    # Código fonte completo e válido escrito na nossa linguagem "Homi"
    codigo_teste = """
    AUTOMACAO "Rotina Noturna da Sala"
    QUANDO horario for 22:30
    SE light.sala_estar estiver ligado
    ENTAO desligar light.sala_estar
    E notificar "A casa foi recolhida e as luzes apagadas!"
    """

    print("========================================")
    print("      COMPILADOR HOMI - INICIADO        ")
    print("========================================\n")

    # FASE 1: Análise Léxica
    tokens = analisador_lexico(codigo_teste)
    
    # FASE 2: Análise Sintática
    parser = AnalisadorSintatico(tokens)
    sucesso_sintatico = parser.analisar()

    if sucesso_sintatico:
        # FASE 3: Análise Semântica
        print("")
        semantico = AnalisadorSemantico(tokens)
        sucesso_semantico = semantico.analisar()
        
        if sucesso_semantico:
            # FASE 4: Geração de Código
            print("")
            gerador = GeradorYAML(tokens)
            codigo_yaml = gerador.gerar()
            
            print("\n[SUCESSO] Código YAML Intermediário Gerado:")
            print("----------------------------------------")
            print(codigo_yaml)
            print("----------------------------------------")
            
            # Grava o resultado final num ficheiro físico
            nome_arquivo = "automacao_home_assistant.yaml"
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                f.write(codigo_yaml)
                
            print(f"\n[CONCLUÍDO] Ficheiro '{nome_arquivo}' guardado com sucesso!")
            print("O compilador terminou a execução com 0 erros.")
            
        else:
            print("\n[ERRO] Compilação abortada na Fase Semântica.")
    else:
        print("\n[ERRO] Compilação abortada na Fase Sintática.")

if __name__ == "__main__":
    main()