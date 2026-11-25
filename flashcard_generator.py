
import tkinter as tk
import random

# ==========================================
# DADOS PARTILHADOS PELOS AGENTES
# ==========================================

world = {
    "raw_text": "",
    "concepts": [],
    "questions": [],
    "flashcards": [],
    "notes": [],
    "final": ""
}


# ==========================================
# AGENTE 1 - SCOUT
# Procura conceitos nas notas
# ==========================================

def scout(text):
    concepts = []

    sentences = text.replace("\n", " ").split(". ")

    for sentence in sentences:
        if ":" in sentence:
            parts = sentence.split(":", 1)

            name = parts[0].strip()
            definition = parts[1].strip().rstrip(".")

            formula = ""

            if "=" in definition or "->" in definition:
                formula = definition.split(",")[0]

            concept = {
                "name": name,
                "definition": definition,
                "formula": formula
            }

            concepts.append(concept)

    return concepts[:5]


# ==========================================
# AGENTE 2 - AUTHOR
# Cria perguntas e flashcards
# ==========================================

def author(concepts):
    questions = []

    for concept in concepts:

        others = []

        for item in concepts:
            if item != concept:
                others.append(item)

        wrong_answers = random.sample(
            others, min(3, len(others))
        )

        options = []

        options.append({
            "text": concept["definition"],
            "correct": True,
            "about": concept["name"]
        })

        for item in wrong_answers:
            options.append({
                "text": item["definition"],
                "correct": False,
                "about": item["name"]
            })

        random.shuffle(options)

        question = {
            "concept": concept["name"],
            "options": options
        }

        questions.append(question)

    flashcards = []

    for concept in concepts[:3]:
        card = {
            "front": concept["name"],
            "back": concept["definition"]
        }

        flashcards.append(card)

    return questions, flashcards


# ==========================================
# AGENTE 3 - REVIEWER
# Verifica as perguntas
# ==========================================

def reviewer(concepts, questions):
    notes = []

    for number, question in enumerate(questions, 1):

        correct = 0
        answers = []

        for option in question["options"]:
            answers.append(option["text"])

            if option["correct"]:
                correct += 1

        if correct != 1:
            notes.append(
                "Pergunta " + str(number) +
                ": numero de respostas corretas incorreto."
            )

        if len(answers) != len(set(answers)):
            notes.append(
                "Pergunta " + str(number) +
                ": existem respostas repetidas."
            )

    if len(concepts) < 5:
        notes.append("Foram encontrados menos de 5 conceitos.")

    if len(notes) == 0:
        notes.append("Nao foram encontrados problemas.")

    return notes


# ==========================================
# CRIAR RESULTADO FINAL
# ==========================================

def create_result():
    concepts = world["concepts"]
    questions = world["questions"]
    flashcards = world["flashcards"]
    notes = world["notes"]

    result = "# PACOTE DE ESTUDO\n\n"

    result += "## Conceitos principais\n\n"

    for concept in concepts:
        result += "- " + concept["name"] + ": "
        result += concept["definition"] + "\n"

        if concept["formula"]:
            result += "  Formula: " + concept["formula"] + "\n"

    result += "\n## Perguntas de escolha multipla\n\n"

    letters = ["A", "B", "C", "D"]

    for number, question in enumerate(questions, 1):

        result += str(number) + ". Qual e a definicao correta de "
        result += question["concept"] + "?\n\n"

        correct_letter = ""

        for i, option in enumerate(question["options"]):
            result += letters[i] + ") " + option["text"] + "\n"

            if option["correct"]:
                correct_letter = letters[i]

        result += "\nResposta correta: " + correct_letter + "\n\n"

        result += "Explicacao das respostas erradas:\n"

        for i, option in enumerate(question["options"]):
            if not option["correct"]:
                result += "- " + letters[i] + ") Esta resposta "
                result += "corresponde ao conceito "
                result += option["about"] + ".\n"

        result += "\n"

    result += "## Flashcards\n\n"

    for card in flashcards:
        result += "Pergunta: " + card["front"] + "\n"
        result += "Resposta: " + card["back"] + "\n\n"

    result += "## Revisao do agente\n\n"

    for note in notes:
        result += "- " + note + "\n"

    return result


# ==========================================
# INICIAR OS 3 AGENTES
# ==========================================

def generate():

    text = input_box.get("1.0", "end").strip()

    if text == "":
        status.config(text="Introduz algumas notas primeiro.")
        return

    world["raw_text"] = text

    status.config(text="Agente 1: Scout a trabalhar...")
    window.update_idletasks()

    # Primeiro agente
    world["concepts"] = scout(world["raw_text"])

    status.config(text="Agente 2: Author a trabalhar...")
    window.update_idletasks()

    # Segundo agente
    questions, flashcards = author(world["concepts"])

    world["questions"] = questions
    world["flashcards"] = flashcards

    status.config(text="Agente 3: Reviewer a trabalhar...")
    window.update_idletasks()

    # Terceiro agente
    world["notes"] = reviewer(
        world["concepts"],
        world["questions"]
    )

    # Criar resultado
    world["final"] = create_result()

    output_box.delete("1.0", "end")
    output_box.insert("1.0", world["final"])

    # Guardar resultado
    with open("pacote_estudo.md", "w", encoding="utf-8") as file:
        file.write(world["final"])

    status.config(text="Concluido! Resultado guardado.")


# ==========================================
# INTERFACE GRAFICA
# ==========================================

window = tk.Tk()

window.title("Exam and Flashcard Generator")
window.geometry("1100x700")
window.configure(bg="white")

# Titulo
title = tk.Label(
    window,
    text="Exam and Flashcard Generator",
    font=("Arial", 18, "bold"),
    bg="white",
    fg="#222222"
)

title.pack(pady=(15, 5))

subtitle = tk.Label(
    window,
    text="Transforma as tuas notas em material de estudo",
    font=("Arial", 10),
    bg="white",
    fg="gray"
)

subtitle.pack(pady=(0, 15))


# Area principal dos paineis
main = tk.Frame(window, bg="white")
main.pack(fill="both", expand=True, padx=15, pady=5)

# Painel esquerdo - Notas
left = tk.Frame(main, bg="white")
left.pack(side="left", fill="both", expand=True, padx=(0, 10))

tk.Label(
    left,
    text="Notas de estudo",
    font=("Arial", 11, "bold"),
    bg="white"
).pack(pady=5)

input_area = tk.Frame(left, bg="white")
input_area.pack(fill="both", expand=True)

input_scroll = tk.Scrollbar(input_area)
input_scroll.pack(side="right", fill="y")

input_box = tk.Text(
    input_area,
    wrap="word",
    font=("Consolas", 10),
    bg="#F7F7F7",
    relief="solid",
    bd=1,
    padx=10,
    pady=10,
    yscrollcommand=input_scroll.set
)

input_box.pack(side="left", fill="both", expand=True)
input_scroll.config(command=input_box.yview)


# Painel direito - Resultado
right = tk.Frame(main, bg="white")
right.pack(side="right", fill="both", expand=True, padx=(10, 0))

tk.Label(
    right,
    text="Resultado",
    font=("Arial", 11, "bold"),
    bg="white"
).pack(pady=5)

output_area = tk.Frame(right, bg="white")
output_area.pack(fill="both", expand=True)

output_scroll = tk.Scrollbar(output_area)
output_scroll.pack(side="right", fill="y")

output_box = tk.Text(
    output_area,
    wrap="word",
    font=("Consolas", 10),
    bg="#F7F7F7",
    relief="solid",
    bd=1,
    padx=10,
    pady=10,
    yscrollcommand=output_scroll.set
)

output_box.pack(side="left", fill="both", expand=True)
output_scroll.config(command=output_box.yview)


# Botao Generate - centrado em baixo
button = tk.Button(
    window,
    text="Generate",
    command=generate,
    font=("Arial", 11, "bold"),
    bg="#2563EB",
    fg="white",
    activebackground="#1D4ED8",
    activeforeground="white",
    relief="flat",
    padx=35,
    pady=9,
    cursor="hand2"
)

button.pack(pady=(12, 8))


# Estado do programa
status = tk.Label(
    window,
    text="Introduz as notas e carrega em Generate",
    font=("Arial", 9),
    bg="white",
    fg="gray"
)

status.pack(pady=(0, 12))


# Iniciar programa
window.mainloop()
