from qdrant_client import QdrantClient
from qdrant_client.http import models
from llama_index.embeddings.ollama import OllamaEmbedding
import os
import json


def recipe_to_embedding(recipe, embed_model):
    # Combine relevant fields for embedding
    text = recipe["title"] + ", " + recipe["description"]
    return embed_model.get_text_embedding(text)


def upload_recipe_to_qdrant(recipe, client, embed_model, idx):
    points = []
    embedding = recipe_to_embedding(recipe, embed_model)
    points.append(
        models.PointStruct(
            id=idx,
            vector=embedding,
            payload=recipe  # Store full recipe as metadata
        )
    )
    client.upsert(collection_name="recipes", points=points)
    print(f"Loaded recipe {idx} ({recipe['title']}) to Qdrant.")



if __name__ == "__main__":

    # Si l'embedding n'a pas encore été fait et la bdd qdrant n'a pas encore été créée
    if not os.path.isdir("./qdrant_data"):
        
        # Initialize the embedding model using Ollama
        embed_model = OllamaEmbedding(
            model_name="mistral",
            base_url="http://localhost:11434",  # Default Ollama server URL
        )

        client = QdrantClient(path="./qdrant_data") 

        # Create a collection
        client.create_collection(
            collection_name="recipes",
            vectors_config=models.VectorParams(
                size=4096,  # Embedding dim de mistral 7b
                distance=models.Distance.COSINE
            )
        )

        # Load recipes from JSON files
        for idx in range(len(os.listdir("./data"))):
            with open(f"./data/recipe{idx}.json", "r", encoding="utf-8") as f:
                recipe = json.load(f)
            upload_recipe_to_qdrant(recipe, client, embed_model, idx)

        client.close()
    # Si la bdd qdrant existe déjà, charge la bdd 
    else:
        pass

