import asyncio
import httpx
from .config import COUNCIL_NODES, CHAIRMAN_NODE

async def check_node(node):
    url = f"{node['url']}/api/tags" # Endpoint léger pour vérifier l'état d'Ollama
    print(f"🔍 Test de {node['name']} ({node['url']})...")
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
            if response.status_code == 200:
                models = [m['name'] for m in response.json().get('models', [])]
                if node['model'] in [m.split(':')[0] for m in models]:
                    print(f"✅ {node['name']} est EN LIGNE et possède le modèle '{node['model']}'")
                else:
                    print(f"⚠️  {node['name']} est EN LIGNE mais '{node['model']}' n'est pas installé ! (Modèles vus: {models})")
                return True
            else:
                print(f"❌ {node['name']} répond avec l'erreur {response.status_code}")
    except Exception as e:
        print(f"❌ {node['name']} est INJOIGNABLE. Erreur: {type(e).__name__}")
    return False

async def main():
    print("--- DÉBUT DU CHECK RÉSEAU LLM COUNCIL ---")
    tasks = [check_node(node) for node in COUNCIL_NODES]
    tasks.append(check_node(CHAIRMAN_NODE))
    results = await asyncio.gather(*tasks)
    
    if all(results):
        print("\n🚀 TOUS LES NŒUDS SONT PRÊTS !")
    else:
        print("\n🚨 ATTENTION : Certains nœuds ne sont pas configurés correctement.")

if __name__ == "__main__":
    asyncio.run(main())