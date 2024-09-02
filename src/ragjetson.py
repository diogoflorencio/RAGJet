import torch
import faiss
import os

# from sentence_transformers import SentenceTransformer
# from transformers import AutoTokenizer, AutoModelForCausalLM
from llama_index.core import SimpleDirectoryReader, Settings, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.legacy.embeddings.langchain import LangchainEmbedding
from langchain_community.embeddings import HuggingFaceEmbeddings
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import load_index_from_storage
from llama_index.llms.huggingface import HuggingFaceLLM


class RaGJetson:
    """
    A class for generating responses to prompts using a RAG model.

    Attributes:
        stored_index (VectorStoreIndex): The stored index of nodes.
        storage_context (StorageContext): The storage context for the index.
    """
    
    def __init__(self):

        documents = SimpleDirectoryReader(input_files=[os.path.join(os.path.dirname(__file__), 'cuDNN-Developer-Guide.pdf')]).load_data()
        parser = SentenceSplitter.from_defaults(chunk_size=512, chunk_overlap=20)
        nodes = parser.get_nodes_from_documents(documents)
        faiss_index = faiss.IndexFlatL2(768) # refers to the creation of a sentence transformer embedding of 768 dimensions

        Settings.embed_model = LangchainEmbedding(
            HuggingFaceEmbeddings(model_name=os.path.join(os.path.dirname(__file__), 'sentence-transformers'))
        )

        vector_store = FaissVectorStore(faiss_index=faiss_index)
        self.storage_context = StorageContext.from_defaults(vector_store=vector_store)

        index = VectorStoreIndex(nodes, storage_context=self.storage_context)
        index.storage_context.persist()

        Settings.llm = HuggingFaceLLM(
            context_window=2048,
            max_new_tokens=512,
            generate_kwargs={"temperature": 0.1, "do_sample": False},
            tokenizer_name=os.path.join(os.path.dirname(__file__), 'tinyllama-tokenizer'),
            model_name=os.path.join(os.path.dirname(__file__), 'tinyllama-model'),
            tokenizer_kwargs={"max_length": 2048},
            model_kwargs={"torch_dtype": torch.float16}
        )

        self.stored_index = load_index_from_storage(self.storage_context)

    def predict(self, prompt):
        """
        Predicts the response to a given prompt.

        Args:
            prompt (str): The prompt to generate a response for.

        Returns:
            str: The generated response.
        """
        stored_index = load_index_from_storage(self.storage_context)
        query_engine = stored_index.as_query_engine()
        response = query_engine.query(prompt)
        return response