# requirements.txt: langchain, langchain-community, langchain-ollama, chromadb
import re

from langchain_core.output_parsers import JsonOutputParser
from langchain_ollama import  OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
import json
import os
from dotenv import load_dotenv
load_dotenv("key.env")
api_key = os.getenv("API_KEY")

class MOMGenerator:
    def __init__(self, model="gemini-2.5-flash"):  # Your local Ollama model
        self.llm = ChatGoogleGenerativeAI(model=model,api_key=api_key)
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.parser = JsonOutputParser()

    def extract_mom(self, transcript: str, persist_dir="./mom_db"):
        """Generate structured MOM from transcript"""
        # Chunk transcript
        chunks = self.splitter.split_text(transcript)
        docs = [Document(page_content=c) for c in chunks]

        # Store temporarily
        vectorstore = Chroma.from_documents(
            docs, self.embeddings, persist_directory=persist_dir
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

        # MOM Extraction Prompt
        prompt = PromptTemplate.from_template("""
        Analyze this meeting transcript and generate structured MOM:

        Transcript: {context}

        Extract in JSON format:
        {{
            "date": "YYYY-MM-DD",
            "attendees": ["Name1", "Name2"],
            "agenda_items": [
                {{"topic": "Item1", "discussion": "Summary", "duration": "10min"}}
            ],
            "decisions": [
                {{"decision": "Approved budget", "owner": "Alice"}}
            ],
            "action_items": [
                {{"task": "Follow up with vendor", "owner": "Bob", "due_date": "2026-01-20"}}
            ],
            "next_meeting": "Date/Time"
        }}
        """)

        # Retrieve + Generate
        relevant = retriever.invoke("meeting decisions actions attendees agenda")
        context = "\n".join([doc.page_content for doc in relevant])

        response = self.llm.invoke(prompt.format(context=context))
        mom = self.clean_json_response(response)
        return mom

    def save_mom(self, mom_data, filename="mom.json"):
        with open(filename, 'w') as f:
            json.dump(mom_data, f, indent=2)
        print(f"✅ MOM saved: {filename}")

    def clean_json_response(self, response):
        """Extract JSON from LLM response"""
        if hasattr(response, 'content'):
            text = response.content
        else:
            text = str(response)

        # Strip markdown
        text = re.sub(r'```json\s*|\s*```', '', text).strip()
        return json.loads(text)


# Usage
generator = MOMGenerator()
transcript = """
Alice: Let's approve the Q1 budget...
Bob: Action item for me - contact vendor by Friday.
Meeting adjourned. Next: Jan 20.
"""

mom = generator.extract_mom(transcript)
print("📋 GENERATED MOM:")
print(json.dumps(mom, indent=2))
generator.save_mom(mom)
