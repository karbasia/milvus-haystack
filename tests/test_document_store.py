import logging
import time

import pytest
from haystack import Document
from haystack.document_stores.types import DocumentStore
from haystack.testing.document_store import CountDocumentsTest, DeleteDocumentsTest, WriteDocumentsTest

from src.milvus_haystack import MilvusDocumentStore

logger = logging.getLogger(__name__)


class TestDocumentStore(CountDocumentsTest, WriteDocumentsTest, DeleteDocumentsTest):
    @pytest.fixture
    def document_store(self) -> MilvusDocumentStore:
        return MilvusDocumentStore(
            connection_args={
                "host": "localhost",
                "port": "19530",
                "user": "",
                "password": "",
                "secure": False,
            },
            drop_old=True,
        )

    def test_write_documents(self, document_store: DocumentStore):
        return_value = document_store.write_documents(
            [Document(content="test doc 1"), Document(content="test doc 2"), Document(content="test doc 3")]
        )
        assert document_store.count_documents() == 3
        assert return_value == 3

    def test_delete_documents(self, document_store: DocumentStore):
        """
        Test delete_documents() normal behaviour.
        """
        doc = Document(content="test doc")
        document_store.write_documents([doc])
        assert document_store.count_documents() == 1

        document_store.delete_documents([doc.id])
        time.sleep(1)
        assert document_store.count_documents() == 0

    @pytest.mark.skip(reason="Milvus does not currently check if entity primary keys are duplicates")
    def test_write_documents_duplicate_fail(self, document_store: DocumentStore): ...

    @pytest.mark.skip(reason="Milvus does not currently check if entity primary keys are duplicates")
    def test_write_documents_duplicate_skip(self, document_store: DocumentStore): ...

    @pytest.mark.skip(reason="Milvus does not currently check if entity primary keys are duplicates")
    def test_write_documents_duplicate_overwrite(self, document_store: DocumentStore): ...

    def test_to_and_from_dict(self, document_store: MilvusDocumentStore):
        document_store_dict = document_store.to_dict()
        expected_dict = {
            "type": "src.milvus_haystack.document_store.MilvusDocumentStore",
            "init_parameters": {
                "collection_name": "HaystackCollection",
                "collection_description": "",
                "collection_properties": None,
                "connection_args": {"host": "localhost", "port": "19530", "user": "", "password": "", "secure": False},
                "consistency_level": "Session",
                "index_params": None,
                "search_params": None,
                "drop_old": True,
                "primary_field": "id",
                "text_field": "text",
                "vector_field": "vector",
                "partition_key_field": None,
                "partition_names": None,
                "replica_number": 1,
                "timeout": None,
            },
        }
        assert document_store_dict == expected_dict
        reconstructed_document_store = MilvusDocumentStore.from_dict(document_store_dict)
        for field in vars(reconstructed_document_store):
            if field.startswith("__"):
                continue
            assert getattr(reconstructed_document_store, field) == getattr(document_store, field)
