"""One-time script to populate ChromaDB with FAQs."""

from src.data_loader import load_faqs
from src.retriever import FAQRetriever


def main():
    print("Setting up FAQ Retrieval System...")

    print("\n1. Loading FAQs from data/faqs.json")
    faqs = load_faqs()

    print(f"   Loaded {len(faqs)} FAQs")
    print("\n2. Initializing ChromaDB")

    retriever = FAQRetriever()

    # Clear existing data
    try:
        retriever.client.delete_collection("faq_collection")
        retriever.collection = retriever.client.create_collection(
            name="faq_collection",
            metadata={"hnsw:space": "cosine"}
        )
        print("   Cleared existing collection")
    except:
        pass

    print("\n3. Adding FAQs to ChromaDB")
    retriever.add_faqs(faqs)

    stats = retriever.get_stats()
    print(f"\n Setup complete! {stats['total_faqs']} FAQs indexed")

    print("\n4. Testing with sample query...")
    results = retriever.retrieve("How do I reset my password?", top_k=3)

    print(f"\nTop result:")
    print(f"  Q: {results[0]['question']}")
    print(f"  A: {results[0]['answer'][:100]}...")
    print(f"  Score: {results[0]['score']:.3f}")
    print(f"  Confidence: {results[0]['confidence']}")


if __name__ == "__main__":
    main()
