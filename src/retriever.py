import chromadb
from typing import Dict, List
from sentence_transformers import SentenceTransformer
from pathlib import Path
import os


class FAQRetriever:
    def __init__(
        self,
        collection_name: str = "faq_collection",
        model_name: str = "paraphrase-multilingual-MiniLM-L12-v2",
    ):

        BASE_DIR = Path(__file__).resolve().parents[1]
        persist_directory = BASE_DIR / "data" / "chroma_db"
        os.makedirs(persist_directory, exist_ok=True)

        self.model = SentenceTransformer(model_name)

        self.client = chromadb.PersistentClient(
            path=str(persist_directory)
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )


    def add_faqs(self, faqs: List[Dict]):
        documents = [faq['question'] for faq in faqs]
        ids = [faq['id'] for faq in faqs]
        metadatas = [{'answer': faq['answer']} for faq in faqs]
        embeddings = self.model.encode(documents).tolist()

        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

        print(f" Added {len(faqs)} FAQs to ChromaDB")

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        query = str(query).strip()
        query_embedding = self.model.encode([query])[0].tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        formatted_results = []
        for i in range(len(results['ids'][0])):
            distance = results['distances'][0][i]
            similarity = 1 - distance

            formatted_results.append({
                'id': results['ids'][0][i],
                'question': results['documents'][0][i],
                'answer': results['metadatas'][0][i]['answer'],
                'score': float(similarity),
                'confidence': self.calculate_confidence(similarity)
            })

        return formatted_results

    def calculate_confidence(self, similarity: float) -> str:
        if similarity >= 0.70:
            return "HIGH"
        elif similarity >= 0.40:
            return "MEDIUM"
        else:
            return "LOW"

    def get_stats(self) -> Dict:
        count = self.collection.count()
        return {
            "total_faqs": count,
            "collection_name": self.collection.name
        }
