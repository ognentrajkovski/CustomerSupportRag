import argparse
from src.retriever import FAQRetriever
from typing import List, Dict


def print_results(results: List[Dict], query: str):

    if not results:
        print("No relevant FAQs found.\n")
        return

    # Part 1: Show all 3 results with scores
    print("Top 3 Matching FAQs:\n")

    for i, result in enumerate(results, 1):
        print(f"{i}. [ID: {result['id']}] Score: {result['score']:.4f} | Confidence: {result['confidence']}")
        print(f"   Q: {result['question']}")
        print(f"   A: {result['answer'][:100]}{'...' if len(result['answer']) > 100 else ''}")
        print()

    # Part 2: Show best matching answer
    best = results[0]
    print("BEST MATCHING ANSWER:")
    print(f"Confidence: {best['confidence']} (Score: {best['score']:.4f})\n")
    print(f"Q: {best['question']}\n")
    print(f"A: {best['answer']}\n")


def interactive_mode(retriever: FAQRetriever):
    """Interactive query mode."""


    print("FAQ RETRIEVAL ASSISTANT - Interactive Mode")

    print("Type your question (or 'quit' to exit)\n")

    while True:
        query = input("Your question: ").strip()

        if query.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!\n")
            break

        if not query:
            continue

        results = retriever.retrieve(query, top_k=3)
        print_results(results, query)


def main():
    parser = argparse.ArgumentParser(
        description="FAQ Retrieval Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('query', nargs='*', help='Your question')
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Start interactive mode')
    parser.add_argument('--top-k', type=int, default=3,
                        help='Number of results to retrieve (default: 3)')

    args = parser.parse_args()

    # Initialize retriever
    print("\n Loading FAQ Retrieval System...")
    retriever = FAQRetriever()
    stats = retriever.get_stats()
    print(f" Ready! Loaded {stats['total_faqs']} FAQs from database\n")

    if args.interactive:
        interactive_mode(retriever)
    elif args.query:
        query = ' '.join(args.query)
        results = retriever.retrieve(query, top_k=args.top_k)
        print_results(results, query)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()