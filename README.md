# Agentes-Inteligentes-e-Sistemas-Multiagentes

# Exam and Flashcard Generator

## 1. O que o projeto faz

Aplicação com interface gráfica (Tkinter) que transforma notas de estudo em material de revisão. Três agentes simples (Scout, Author e Reviewer) trabalham em sequência: o Scout extrai conceitos das notas, o Author cria perguntas de escolha múltipla e flashcards, e o Reviewer verifica a qualidade das perguntas. O resultado é mostrado na janela e guardado em `pacote_estudo.md`.

## 2. Como instalar

- Python 3.8 ou superior
- Tkinter (já vem incluído no Python em Windows e macOS; em Linux: `sudo apt install python3-tk`)
- Não são necessárias bibliotecas externas, contas nem chaves de API.

## 3. Como executar

```bash
python main.py
```

Na janela que abre:

1. Cola as notas no painel esquerdo, no formato `Nome: definição.` (cada frase termina com ". "). Exemplo:

```
Velocidade: variação da posição por unidade de tempo, v = d / t. Aceleração: variação da velocidade por unidade de tempo, a = dv / dt. Força: interação que altera o movimento de um corpo, F = m * a. Trabalho: energia transferida por uma força, W = F * d. Potência: trabalho por unidade de tempo, P = W / t.
```

2. Clica em **Generate**.

## 4. Resultado esperado

- A barra de estado mostra "Agente 1...", "Agente 2...", "Agente 3..." e, no fim, **"Concluido! Resultado guardado."**
- O painel direito mostra o "PACOTE DE ESTUDO" com: conceitos principais, perguntas de escolha múltipla (com resposta correta e explicação das erradas), 3 flashcards e a revisão do agente (por exemplo, "Nao foram encontrados problemas.").
- É criado o ficheiro `pacote_estudo.md` na pasta onde o programa foi executado.

## 5. Estrutura do repositório

```
.
├── main.py            # código completo: agentes, geração do resultado e interface
├── pacote_estudo.md   # ficheiro gerado ao clicar em Generate
└── README.md
```

## 6. Membros do grupo

- Cláudio Lima (230001164)
- Ryhana Rodrigues (240001442)
