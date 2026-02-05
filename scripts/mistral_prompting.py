import requests
import json

context_str = f'''
Recette 1 : 
- Ingrédients :
{", ".join(json.load(open("./data/recipe0.json", "r", encoding="utf-8"))["ingredients"])}
- Instructions : 
{json.load(open("./data/recipe0.json", "r", encoding="utf-8"))["instructions"]}

Recette 2 : 
- Ingrédients :
{",".join(json.load(open("./data/recipe1.json", "r", encoding="utf-8"))["ingredients"])}
- Instructions : 
{json.load(open("./data/recipe1.json", "r", encoding="utf-8"))["instructions"]}
'''
query_str = "Je veux faire un muffin à la banane"

prompt = f'''
TU ES "RASTA MUFFIN", UN ASSISTANT CULINAIRE OBSESSIONNEL MAIS SYMPATHIQUE, FAN DE MUFFINS ET DE REGGAE.
TU AIMES PARLER COMME UN RASTA, AVEC DES EXPRESSIONS COLORÉES ET UN TON DÉCONTRACTÉ.
TON OBJECTIF EST DE TROUVER LA RECETTE DE MUFFIN IDÉALE PARMI LE CONTEXTE FOURNI.

### TES DIRECTIVES (GUARDRAILS) :
1. OBSESSION : Tu ne cuisines QUE des muffins. Si on te demande des lasagnes ou une pizza, REFUSE poliment avec humour.
2. ANCRAGE : Utilise UNIQUEMENT les recettes fournies sous la balise [CONTEXTE]. N'invente rien. Mentionne les quantités des ingrédients.
3. LANGUE : Réponds toujours en français courant et appétissant.
4. MARKDOWN : Réponds en Markdown.

[CONTEXTE]
{context_str}
[QUESTION]
{query_str}
'''


response = requests.post(
    'http://localhost:11434/api/generate',
    json={
        'model': 'mistral',
        'prompt': prompt,
        'stream': False
    }
)

print(response.json()['response'])

print(context_str)