# This is going to be quite important - what data do we get to create the index?
# The way that we get the data is also going to be extremely linked to the structure of the data in the database

from typing import Any, Dict, List, Optional

from llama_index.readers.base import BaseReader
from llama_index.schema import Document


class SimpleMongoReader(BaseReader):
    """Simple mongo reader.

    Concatenates each Mongo doc into Document used by LlamaIndex.

    Args:
        host (str): Mongo host.
        port (int): Mongo port.
        max_docs (int): Maximum number of documents to load. Defaults to 0 (no limit).

    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        uri: Optional[str] = None,
        max_docs: int = 0,
    ) -> None:
        """Initialize with parameters."""
        try:
            import pymongo
            from pymongo import MongoClient
        except ImportError:
            raise ImportError(
                "`pymongo` package not found, please run `pip install pymongo`"
            )

        client: MongoClient
        if uri:
            client = MongoClient(uri)
        elif host and port:
            client = MongoClient(host, port)
        else:
            raise ValueError("Either `host` and `port` or `uri` must be provided.")

        self.client = client
        self.max_docs = max_docs

    def load_data(
        self,
        db_name: str,
        collection_name: str,
        field_names: List[str] = ["text"],
        separator: str = "",
        query_dict: Optional[Dict] = None,
        metadata_names: Optional[List[str]] = None,
    ) -> List[Document]:
        """Load data from the input directory.

        Args:
            db_name (str): name of the database.
            collection_name (str): name of the collection.
            field_names(List[str]): names of the fields to be concatenated.
                Defaults to ["text"]
            separator (str): separator to be used between fields.
                Defaults to ""
            query_dict (Optional[Dict]): query to filter documents.
                Defaults to None
            metadata_names (Optional[List[str]]): names of the fields to be added
                to the metadata attribute of the Document. Defaults to None

        Returns:
            List[Document]: A list of documents.

        """
        documents = []
        db = self.client[db_name]
        cursor = db[collection_name].find(filter=query_dict or {}, limit=self.max_docs)

        for item in cursor:
            texts = []
            for field_name in field_names:
                if field_name not in item:
                    break
                field = item[field_name]
                if  isinstance(field, str):
                    texts += [field] 
                # I dont think that this is particularly good practice tbh
                # This is probably a bit more complicated - I would rather standardize the data in the database better
                elif field_name == 'speeches':
                    texts = ['topic of the session:' + field['session_topic']]
                    for speech in field:
                        texts += ['the speaker for the following text is:' + speech['speaker']]
                        texts += [comment['text'] for comment in speech['comment']]
                         
                     
                elif field_name == 'comment':
                     texts = [comment['text'] for comment in field]
                    
                    
            text = separator.join(texts)

            if metadata_names is None:
                documents.append(Document(text=text))
            else:
                metadata = {}
                for metadata_name in metadata_names:
                    if metadata_name not in item:
                        raise ValueError(
                            f"`{metadata_name}` field not found in Mongo document."
                        )
                    metadata[metadata_name] = item[metadata_name]
                documents.append(Document(text=text, metadata=metadata))
        
        return documents
