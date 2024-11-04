import json
import pickle

from typing import Dict, List, Literal

from llm_foundation import logger
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_pdf(file_path:str = "2405.14831v1.pdf"): 

    doc_loader = PyPDFLoader(file_path)
    pages = doc_loader.load_and_split()
    return "\n".join([p.page_content for p in pages])


def split_text(text: str, chunk_size: int=1000, char_overlap: int=0) -> List[Document]:

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=char_overlap,
        length_function=len,
        is_separator_regex=False,
    )

    return text_splitter.create_documents([text])


def build_document_structure(document_path: str, chunk_size=1000) -> List[Dict]:
    text = load_pdf(document_path)
    chunks = split_text(text, chunk_size=chunk_size, char_overlap=0)
    document_chunks: List[Dict] = [ { "id":idx, "text":chunk.page_content } for idx, chunk in enumerate(chunks[0:1])]  # TODO Remove this [0:1] filter!!!! Just for testing
    assert len(document_chunks) == 1, f"Number of chunks mismatch: {len(document_chunks)} is not 1"  # TODO Remove this assert!!!! Just for testing
    logger.info("--------------------------------------------------------------------------------")
    logger.info(f"Number of chunks: {len(chunks)}")
    logger.info("--------------------------------------------------------------------------------")
    return document_chunks


def save_document_structure(document_chunks: List[dict], output_file: str, format: Literal["pickle", "json"] = "pickle"):
    logger.info(f"Saving document structure to {output_file}")
    match format:
        case "pickle":
            with open(output_file, "wb") as f:
                pickle.dump(document_chunks, f)
        case "json":
            with open(output_file, "w") as f:
                json.dump(document_chunks, f, indent=4)
        case _:
            raise ValueError(f"Invalid format: {format}")
