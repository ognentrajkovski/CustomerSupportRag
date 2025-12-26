# Current vs future scalable implementation 

## Current
 - The current implementation is a balance between a fully scalable system and a fast local solution
 - The pros of this solution are that it uses a lightweight database, relatively small but capable model, easy data-adding process and no API costs
 - The cons are that for this particular case (15 FAQS), a more optimized and faster solution could have been implemented, for example instead of using a vector database, a simple array for storing the embeddings and a similarity search function, but I wanted to at least go in the "Scalable" direction

## Future Improvements 
### Some functionalities I would implement for a large scale product like VerbaAI would be:
 - Change of database - while ChromaDB is good enough for a MVP, it is file based and local, in other words limited, so for a production-ready product I would use server-based database like Pincecone
 - Question and answer filter functionality - if a particular QA pair is already in the dataset, there is no need for it to be added. This could be done by doing a similarity seach when adding new data and if the score is above a certain threshold, for example > 95% similarity, it is basically the same and there is no need to be added. Or if it is an exact copy, a CRUD API would do the work
 - Cache layer - for the most repetitive and simple queries there would not be a need for embedding
 - Change embedding model - if the product and it's data are large, other paid embedding models would be more robust and better for multilingual support
 - Optimized performance - GPU acceleration (ex. CUDA) and batch embeddings to reduce computation time
 - Logging - errors, crashes logging
 - Security endpoints
 - Latency monitoring
 - Accuracy tracking overtime
 - LLM integration - based on my other RAG project, if the data is large enough and the queries are more complicated, an LLM could search for the information and retrieve a custom tailored response, collected from the entire document instead of a single best fit.