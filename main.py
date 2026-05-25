# 1. Importa a função do ficheiro lexico.py
from lexico import analisador_lexico

# 2. Importa a classe do ficheiro sintatico.py
from sintatico import AnalisadorSintatico

def main():
    # Código fonte de teste na nossa linguagem "Homi"
    codigo_teste = """
    AUTOMACAO "Ligar Luzes da Sala"
    #teste comentario
    QUANDO horario for 18:00
    SE light.sala_estar estiver desligado
    ENTAO ligar light.sala_estar
    E notificar "Luzes ligadas!"
    """

    print("========================================")
    print("      COMPILADOR HOMI - INICIADO        ")
    print("========================================\n")

    # --- FASE 1: ANÁLISE LÉXICA ---
    print("[FASE 1] A executar o Analisador Léxico...")
    tokens_gerados = analisador_lexico(codigo_teste)
    
    # (Opcional) Imprimir os tokens para ver se está tudo correto
    # for t in tokens_gerados:
    #     print(t)
        
    print(f"-> {len(tokens_gerados)} tokens extraídos com sucesso.\n")

    # --- FASE 2: ANÁLISE SINTÁTICA ---
    print("[FASE 2] A executar o Analisador Sintático...")
    
    # Passamos os tokens gerados na fase 1 para o parser da fase 2
    parser = AnalisadorSintatico(tokens_gerados)
    sucesso = parser.analisar()

    print("\n========================================")
    if sucesso:
        print(" RESULTADO: Sucesso! Código Homi válido.")
    else:
        print(" RESULTADO: Falha! Encontrados erros de sintaxe.")
    print("========================================")

# Este bloco garante que o código principal só corre se executarmos o main.py diretamente
if __name__ == "__main__":
    main()