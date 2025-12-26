# CustomerSupportRag

A simple multilingual FAQ Retrieval System for customer support. This project allows users to ask questions and retrieve the most relevant answers from a pre-defined set of FAQs using semantic search.

---

## Project Overview

The system works by embedding FAQ questions and user queries into vector representations using a transformer model. Then, it uses a vector database to perform similarity search and retrieve the most relevant FAQs based on semantic similarity.


### Approach

1. **Data Preparation**  
   - FAQs are stored in a JSON file containing questions, answers, and unique IDs
   
2. **Embedding Generation**  
   - Each FAQ question is converted into a vector using the `SentenceTransformer` model:  
     `"paraphrase-multilingual-MiniLM-L12-v2"` from HuggingFace
   - The model was a requirements driven choice. It supports 50+ languages including both, enabling true cross-lingual semantic search without 
     translation layers
   - Specifically trained for finding semantically similar text, which is exactly our use case (matching user queries to FAQ questions)
   - Runs locally without API keys or costs and good for home tasks where the reviewer needs to run the project immediately
   - Provides excellent quality for FAQ matching while maintaining fast retrieval speeds
     

3. **Database Storage**  
   - ChromaDB is used as a vector database to store embedded questions, answers, and metadata
   - It is a lightweight, production-ready vector database that requires zero infrastructure setup while providing all the features needed for semantic search at this scale
   - Optimized for cosine similarity search
   
4. **Query & Retrieval**  
   - User queries are encoded into embeddings
   - ChromaDB performs a similarity search to return top-k (in this case 3) relevant FAQs
   - The system outputs results with a confidence score: HIGH (above 70), MEDIUM (between 40 and 70), or LOW (under 40)

---

## Tools and Libraries Used

- **Python 3.12+**
- **ChromaDB**: Vector database for storing and retrieving embeddings
- **Sentence Transformers**: For generating semantic embeddings
- **NumPy**: For handling numerical arrays (embeddings)
- **Pathlib & OS**: For file and path management
- **Argparse**: For interactive command-line interface

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 500MB free disk space (for models and dependencies)

## How to run the project

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/faq-retrieval.git
cd faq-retrieval
```

### 2. Create Virtual Environment

A virtual environment isolates project dependencies from your system Python.
```bash
# Create virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

You should see `(venv)` prefix in your terminal, indicating the environment is active.

### 3. Install Dependencies

This installs all required packages: ChromaDB, sentence-transformers, and utilities.
```bash
pip install -r requirements.txt
```

### 4. Setup the Database

This script loads FAQs from `data/faqs.json` and creates the ChromaDB vector database. Make sure you are in root directory `/CustomerSupportRag`
```bash
python -m data.setup_db
```

**What this does:**
- Reads FAQ entries from `data/faqs.json`
- Generates embeddings for each question using the multilingual model
- Stores vectors in `data/chroma_db/` (auto-created)
- Verifies setup with a test query

**Expected output:**
```
Setting up FAQ Retrieval System...

1. Loading FAQs from data/faqs.json
   Loaded 15 FAQs

2. Initializing ChromaDB
   Cleared existing collection

3. Adding FAQs to ChromaDB
 Added 15 FAQs to ChromaDB

 Setup complete! 15 FAQs indexed

4. Testing with sample query...

Top result:
  Q: How do I reset my password?
  A: To reset your password, click on the 'Forgot Password' link on the login page and follow the instruc...
  Score: 1.000
  Confidence: HIGH
```

### 5. Run the Application

#### Interactive Mode (Recommended)

Chat-like interface where you can ask multiple questions.
```bash
python app.py --interactive
```

**Expected output after a query:**

```
 Loading FAQ Retrieval System...
 Ready! Loaded 15 FAQs from database

FAQ RETRIEVAL ASSISTANT - Interactive Mode
Type your question (or 'quit' to exit)

Your question: what if my order is damaged
Top 3 Matching FAQs:

1. [ID: faq_011] Score: 0.8930 | Confidence: HIGH
   Q: What should I do if my order arrives damaged?
   A: If your order arrives damaged, please contact customer support within 48 hours and include photos of...

2. [ID: faq_012] Score: 0.4886 | Confidence: MEDIUM
   Q: Can I change my shipping address after placing an order?
   A: Shipping addresses can only be changed before the order is shipped. Please contact support as soon a...

3. [ID: faq_010] Score: 0.4461 | Confidence: MEDIUM
   Q: How can I track my order?
   A: Once your order is shipped, you will receive a tracking number via email. You can also find it in yo...

BEST MATCHING ANSWER:
Confidence: HIGH (Score: 0.8930)

Q: What should I do if my order arrives damaged?

A: If your order arrives damaged, please contact customer support within 48 hours and include photos of the damage.
```




