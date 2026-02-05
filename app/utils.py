from qdrant_client import QdrantClient
from qdrant_client.http import models
from llama_index.embeddings.ollama import OllamaEmbedding
import os
import json
import requests



embed_model = OllamaEmbedding(
        model_name="mistral",
        base_url="http://localhost:11434",  # Default Ollama server URL
    )

client = QdrantClient(path="./qdrant_data") 


def query_embedding(query:str):
    return embed_model.get_text_embedding(query)


def retrieve_best_recipes(query:str, top_k=3):

    embedding = query_embedding(query)

    results = client.search(
            collection_name="recipes",
            query_vector=embedding,
            limit=top_k
        )
    
    recipes = []
    for result in results:
        recipes.append(result.payload)
    
    return recipes


def prompt_mistral(recipes, question):
    
    context_str = f'''
    Recette : 
    - Ingrédients :
    {", ".join(recipes[0]["ingredients"])}
    - Instructions : 
    {recipes[0]["instructions"]}

    Recette :
    - Ingrédients :
    {", ".join(recipes[1]["ingredients"])}
    - Instructions : 
    {recipes[1]["instructions"]}*

    Recette :
    - Ingrédients :
    {", ".join(recipes[2]["ingredients"])}
    - Instructions : 
    {recipes[2]["instructions"]}
    '''

    prompt = f'''
    TU ES "RASTA MUFFIN", UN ASSISTANT CULINAIRE OBSESSIONNEL MAIS SYMPATHIQUE, FAN DE MUFFINS ET DE REGGAE.
    TU AIMES PARLER COMME UN RASTA, AVEC DES EXPRESSIONS COLORÉES ET UN TON DÉCONTRACTÉ.
    TON OBJECTIF EST DE TROUVER LA RECETTE DE MUFFIN IDÉALE PARMI LE CONTEXTE FOURNI.

    ### TES DIRECTIVES (GUARDRAILS) :
    1. OBSESSION : Tu ne cuisines QUE des muffins. Si on te demande des lasagnes ou une pizza, REFUSE poliment avec humour.
    2. ANCRAGE : Utilise UNIQUEMENT les recettes fournies sous la balise [CONTEXTE]. Sélectionne celle qui te semble la plus appropriée. N'invente rien. Mentionne les quantités des ingrédients.
    3. LANGUE : Réponds toujours en français courant et appétissant.
    4. MARKDOWN : Réponds en Markdown.

    [CONTEXTE]
    {context_str}
    [QUESTION]
    {question}
    '''
    
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': 'mistral',
            'prompt': prompt,
            'stream': False
        }
    )

    return response.json()['response']
