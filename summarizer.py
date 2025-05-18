import os
from dotenv import load_dotenv
from llama_index.core import GPTVectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.llms.openai import OpenAI
from llama_index.core.settings import Settings
from llama_index.embeddings.openai import OpenAIEmbedding

#load envirement variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class Summarizer:
    def __init__(self):
        #Settings.llm = OpenAI(model='gpt-4', api_key=OPENAI_API_KEY)
        Settings.llm = OpenAI(model='gpt-3.5-turbo', api_key=OPENAI_API_KEY)

    def summarize_text(self, text):
        document = [Document(text=text)]
        index = GPTVectorStoreIndex.from_documents(document)
        query_engine = index.as_query_engine()

        response = query_engine.query("summarize this text in to key points suitable for powerpoints slide")

        return response.response
    
if __name__ == "__main__":
    # Test Summarizer
    sample_text = """ AI is transforming industries by automating repetitive tasks and enabling data-driven decision-making.
    This project aims to generate Powerpoint slides automatically based on input documents.
    It will extract text from PDFs, DOCX, TXT, and CSV files and convert them into well-structured slides.
    The AI will use OpenAI's GPT models for text summarization and LllamaIndex for information retrieval."""

    summarizer = Summarizer()
    summary = summarizer.summarize_text(sample_text)
    
    print("\n + **summarized Text:**\n")
    print(summary)


# from transformers import pipeline

# class Summarizer:
#     def __init__(self):
#         # Initialize the summarization pipeline with a pre-trained model
#         self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

#     def summarize_text(self, text: str) -> str:
#         # Generate summary (adjust max_length and min_length as needed)
#         summary_list = self.summarizer(text, max_length=150, min_length=40, do_sample=False)
#         return summary_list[0]['summary_text']

# if __name__ == "__main__":
#     sample_text = """AI is transforming industries by automating repetitive tasks and enabling data-driven decision-making.
#     This project aims to generate PowerPoint slides automatically based on input documents.
#     It will extract text from PDFs, DOCX, TXT, and CSV files and convert them into well-structured slides.
#     The AI will use OpenAI's GPT models for text summarization and LlamaIndex for information retrieval."""

#     summarizer = Summarizer()
#     summary = summarizer.summarize_text(sample_text)

#     print("\n+ **Summarized Text:**\n")
#     print(summary)


