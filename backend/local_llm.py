"""Local LLM API client for Ollama."""
import httpx
from typing import List, Dict, Any, Optional

async def query_model(
    node_url: str,
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """Version modifiée pour Ollama local."""
    
    # On convertit le format 'messages' en un seul prompt pour /api/generate
    # Ou on utilise /api/chat si on veut garder la structure
    prompt = messages[-1]['content'] 

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False # Important pour ne pas recevoir mot par mot
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            # On ajoute /api/generate à l'URL de base du config
            response = await client.post(
                f"{node_url}/api/generate",
                json=payload
            )
            response.raise_for_status()
            data = response.json()

            return {
                'content': data.get('response'),
                'reasoning_details': None # Ollama n'envoie pas ça par défaut
            }
    except Exception as e:
        print(f"Error querying local node {node_url}: {e}")
        return None

async def query_models_parallel(
    nodes: List[Dict[str, str]],
    messages: List[Dict[str, str]]
) -> Dict[str, Optional[Dict[str, Any]]]:
    """Appels en parallèle sur plusieurs adresses IP."""
    import asyncio
    
    # On crée une tâche par dictionnaire dans COUNCIL_NODES
    tasks = [query_model(node['url'], node['model'], messages) for node in nodes]
    responses = await asyncio.gather(*tasks)

    # On retourne un dictionnaire { "Nom_du_PC": réponse }
    return {node['name']: resp for node, resp in zip(nodes, responses)}