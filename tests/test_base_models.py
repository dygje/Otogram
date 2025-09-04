"""
Tests for Base Models
"""

import pytest
from datetime import datetime
from unittest.mock import patch
import uuid

from src.models.base import BaseDocument


class TestBaseDocument:
    """Test BaseDocument class"""

    def test_base_document_creation(self):
        """Test creating a BaseDocument instance"""
        doc = BaseDocument()
        
        # Check that all required fields are present
        assert hasattr(doc, 'id')
        assert hasattr(doc, 'created_at')
        assert hasattr(doc, 'updated_at')
        
        # Check that ID is a string (UUID format)
        assert isinstance(doc.id, str)
        assert len(doc.id) == 36  # Standard UUID string length
        
        # Check that timestamps are datetime objects
        assert isinstance(doc.created_at, datetime)
        assert isinstance(doc.updated_at, datetime)

    def test_base_document_id_generation(self):
        """Test that each document gets a unique ID"""
        doc1 = BaseDocument()
        doc2 = BaseDocument()
        
        assert doc1.id != doc2.id
        
        # Check that IDs are valid UUIDs
        uuid.UUID(doc1.id)  # Should not raise an exception
        uuid.UUID(doc2.id)  # Should not raise an exception

    def test_base_document_timestamps(self):
        """Test that timestamps are set properly"""
        before_creation = datetime.utcnow()
        doc = BaseDocument()
        after_creation = datetime.utcnow()
        
        # Check that created_at is set to current time
        assert before_creation <= doc.created_at <= after_creation
        
        # Check that updated_at is initially equal to created_at
        assert doc.created_at == doc.updated_at

    def test_update_timestamp(self):
        """Test the update_timestamp method"""
        doc = BaseDocument()
        original_created_at = doc.created_at
        original_updated_at = doc.updated_at
        
        # Wait a small amount to ensure timestamp difference
        import time
        time.sleep(0.01)
        
        # Update timestamp
        doc.update_timestamp()
        
        # Check that created_at remains unchanged
        assert doc.created_at == original_created_at
        
        # Check that updated_at has been updated
        assert doc.updated_at > original_updated_at
        assert doc.updated_at != doc.created_at

    def test_update_timestamp_multiple_calls(self):
        """Test multiple calls to update_timestamp"""
        doc = BaseDocument()
        timestamps = [doc.updated_at]
        
        # Update timestamp multiple times
        for _ in range(3):
            import time
            time.sleep(0.01)  # Small delay to ensure different timestamps
            doc.update_timestamp()
            timestamps.append(doc.updated_at)
        
        # Check that each timestamp is later than the previous
        for i in range(1, len(timestamps)):
            assert timestamps[i] > timestamps[i-1]

    def test_base_document_with_inheritance(self):
        """Test BaseDocument when used as a base class"""
        class TestModel(BaseDocument):
            name: str
            value: int
        
        model = TestModel(name="test", value=42)
        
        # Check inherited fields
        assert hasattr(model, 'id')
        assert hasattr(model, 'created_at')
        assert hasattr(model, 'updated_at')
        
        # Check custom fields
        assert model.name == "test"
        assert model.value == 42
        
        # Check that inherited functionality works
        original_updated_at = model.updated_at
        import time
        time.sleep(0.01)
        model.update_timestamp()
        assert model.updated_at > original_updated_at

    def test_base_document_serialization(self):
        """Test that BaseDocument can be serialized"""
        doc = BaseDocument()
        
        # Test dict() method (Pydantic v1 style)
        try:
            doc_dict = doc.dict()
            assert isinstance(doc_dict, dict)
            assert 'id' in doc_dict
            assert 'created_at' in doc_dict
            assert 'updated_at' in doc_dict
        except AttributeError:
            # Pydantic v2 style
            doc_dict = doc.model_dump()
            assert isinstance(doc_dict, dict)
            assert 'id' in doc_dict
            assert 'created_at' in doc_dict
            assert 'updated_at' in doc_dict

    def test_base_document_json_serialization(self):
        """Test that BaseDocument can be serialized to JSON"""
        doc = BaseDocument()
        
        # Test JSON serialization
        try:
            json_str = doc.json()
            assert isinstance(json_str, str)
            assert doc.id in json_str
        except AttributeError:
            # Pydantic v2 style
            json_str = doc.model_dump_json()
            assert isinstance(json_str, str)
            assert doc.id in json_str

    def test_base_document_field_validation(self):
        """Test field validation in BaseDocument"""
        # Create a model that extends BaseDocument with validation
        class ValidatedModel(BaseDocument):
            name: str
            age: int
            
            @classmethod
            def validate_age(cls, v):
                if v < 0:
                    raise ValueError('Age must be non-negative')
                return v
        
        # Valid model should work
        model = ValidatedModel(name="John", age=25)
        assert model.name == "John"
        assert model.age == 25

    def test_base_document_uuid_format(self):
        """Test that generated UUIDs are in correct format"""
        doc = BaseDocument()
        
        # Check UUID format (8-4-4-4-12 characters)
        uuid_parts = doc.id.split('-')
        assert len(uuid_parts) == 5
        assert len(uuid_parts[0]) == 8
        assert len(uuid_parts[1]) == 4
        assert len(uuid_parts[2]) == 4
        assert len(uuid_parts[3]) == 4
        assert len(uuid_parts[4]) == 12

    def test_base_document_timestamp_timezone(self):
        """Test that timestamps use UTC"""
        doc = BaseDocument()
        
        # Timestamps should be timezone-naive UTC times
        assert doc.created_at.tzinfo is None
        assert doc.updated_at.tzinfo is None

    @patch('src.models.base.datetime')
    def test_base_document_mocked_time(self, mock_datetime):
        """Test BaseDocument with mocked time"""
        fixed_time = datetime(2023, 1, 1, 12, 0, 0)
        mock_datetime.utcnow.return_value = fixed_time
        
        doc = BaseDocument()
        
        assert doc.created_at == fixed_time
        assert doc.updated_at == fixed_time

    def test_base_document_equality(self):
        """Test BaseDocument equality based on ID"""
        doc1 = BaseDocument()
        doc2 = BaseDocument()
        
        # Different documents should not be equal
        assert doc1 != doc2
        
        # Same document should be equal to itself
        assert doc1 == doc1

    def test_base_document_copy(self):
        """Test copying BaseDocument"""
        doc1 = BaseDocument()
        
        # Create a copy with same ID
        doc2 = BaseDocument(
            id=doc1.id,
            created_at=doc1.created_at,
            updated_at=doc1.updated_at
        )
        
        assert doc1.id == doc2.id
        assert doc1.created_at == doc2.created_at
        assert doc1.updated_at == doc2.updated_at

    def test_base_document_custom_id(self):
        """Test BaseDocument with custom ID"""
        custom_id = "custom-test-id-12345"
        doc = BaseDocument(id=custom_id)
        
        assert doc.id == custom_id
        assert isinstance(doc.created_at, datetime)
        assert isinstance(doc.updated_at, datetime)

    def test_base_document_custom_timestamps(self):
        """Test BaseDocument with custom timestamps"""
        custom_time = datetime(2023, 1, 1, 10, 0, 0)
        doc = BaseDocument(
            created_at=custom_time,
            updated_at=custom_time
        )
        
        assert doc.created_at == custom_time
        assert doc.updated_at == custom_time

    def test_base_document_repr(self):
        """Test BaseDocument string representation"""
        doc = BaseDocument()
        repr_str = repr(doc)
        
        # Should contain class name and key information
        assert 'BaseDocument' in repr_str
        assert doc.id in repr_str