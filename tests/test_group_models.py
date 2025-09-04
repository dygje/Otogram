"""
Tests for Group Models
"""

import pytest
from pydantic import ValidationError

from src.models.group import Group, GroupCreate, GroupBulkCreate


class TestGroup:
    """Test Group model"""

    def test_group_creation_minimal(self):
        """Test creating group with minimal fields"""
        group = Group()
        
        # Check default values
        assert group.group_id is None
        assert group.group_username is None
        assert group.group_link is None
        assert group.group_title is None
        assert group.is_active is True
        assert group.message_count == 0
        
        # Check inherited fields
        assert hasattr(group, 'id')
        assert hasattr(group, 'created_at')
        assert hasattr(group, 'updated_at')

    def test_group_creation_with_id(self):
        """Test creating group with group ID"""
        group = Group(group_id="-1001234567890")
        
        assert group.group_id == "-1001234567890"
        assert group.group_username is None
        assert group.group_link is None

    def test_group_creation_with_username(self):
        """Test creating group with username"""
        group = Group(group_username="testgroup")
        
        assert group.group_username == "@testgroup"  # Should add @ prefix

    def test_group_creation_with_username_at_prefix(self):
        """Test creating group with username that already has @ prefix"""
        group = Group(group_username="@testgroup")
        
        assert group.group_username == "@testgroup"  # Should not add another @

    def test_group_creation_with_link(self):
        """Test creating group with group link"""
        group = Group(group_link="https://t.me/testgroup")
        
        assert group.group_link == "https://t.me/testgroup"

    def test_group_creation_full(self):
        """Test creating group with all fields"""
        group = Group(
            group_id="-1001234567890",
            group_username="@testgroup",
            group_link="https://t.me/testgroup",
            group_title="Test Group",
            is_active=False,
            message_count=10
        )
        
        assert group.group_id == "-1001234567890"
        assert group.group_username == "@testgroup"
        assert group.group_link == "https://t.me/testgroup"
        assert group.group_title == "Test Group"
        assert group.is_active is False
        assert group.message_count == 10

    def test_group_username_validator(self):
        """Test group username validator"""
        # Without @ prefix
        group1 = Group(group_username="testgroup")
        assert group1.group_username == "@testgroup"
        
        # With @ prefix
        group2 = Group(group_username="@testgroup")
        assert group2.group_username == "@testgroup"
        
        # None value
        group3 = Group(group_username=None)
        assert group3.group_username is None

    def test_group_default_values(self):
        """Test group default values"""
        group = Group()
        
        assert group.is_active is True
        assert group.message_count == 0

    def test_group_message_count_operations(self):
        """Test group message count operations"""
        group = Group(message_count=5)
        assert group.message_count == 5
        
        # Simulate incrementing message count
        group.message_count += 1
        assert group.message_count == 6

    def test_group_active_inactive(self):
        """Test group active/inactive states"""
        # Active group
        active_group = Group(is_active=True)
        assert active_group.is_active is True
        
        # Inactive group
        inactive_group = Group(is_active=False)
        assert inactive_group.is_active is False

    def test_group_serialization(self):
        """Test group serialization"""
        group = Group(
            group_id="-1001234567890",
            group_username="@testgroup",
            group_title="Test Group",
            is_active=True,
            message_count=5
        )
        
        data = group.model_dump()
        assert isinstance(data, dict)
        assert data['group_id'] == "-1001234567890"
        assert data['group_username'] == "@testgroup"
        assert data['group_title'] == "Test Group"
        assert data['is_active'] is True
        assert data['message_count'] == 5
        assert 'id' in data
        assert 'created_at' in data
        assert 'updated_at' in data

    def test_group_json_serialization(self):
        """Test group JSON serialization"""
        group = Group(group_title="JSON Test Group")
        
        json_str = group.model_dump_json()
        assert isinstance(json_str, str)
        assert "JSON Test Group" in json_str

    def test_group_different_identifier_types(self):
        """Test group with different identifier types"""
        # Group ID only
        group1 = Group(group_id="-1001111111")
        assert group1.group_id == "-1001111111"
        assert group1.group_username is None
        
        # Username only
        group2 = Group(group_username="@channel123")
        assert group2.group_username == "@channel123"
        assert group2.group_id is None
        
        # Link only
        group3 = Group(group_link="https://t.me/testchannel")
        assert group3.group_link == "https://t.me/testchannel"
        assert group3.group_id is None


class TestGroupCreate:
    """Test GroupCreate model"""

    def test_group_create_with_id(self):
        """Test GroupCreate with group ID"""
        data = GroupCreate(group_identifier="-1001234567890")
        
        assert data.group_identifier == "-1001234567890"

    def test_group_create_with_username(self):
        """Test GroupCreate with username"""
        data = GroupCreate(group_identifier="@testgroup")
        
        assert data.group_identifier == "@testgroup"

    def test_group_create_with_link(self):
        """Test GroupCreate with link"""
        data = GroupCreate(group_identifier="https://t.me/testgroup")
        
        assert data.group_identifier == "https://t.me/testgroup"

    def test_group_create_username_without_at(self):
        """Test GroupCreate with username without @ prefix"""
        data = GroupCreate(group_identifier="testgroup")
        
        assert data.group_identifier == "@testgroup"  # Should add @ prefix

    def test_group_create_validator_whitespace(self):
        """Test GroupCreate validator with whitespace"""
        data = GroupCreate(group_identifier="  @testgroup  ")
        
        assert data.group_identifier == "@testgroup"  # Should strip whitespace

    def test_group_create_validator_id_format(self):
        """Test GroupCreate validator with ID format"""
        # Valid negative ID
        data1 = GroupCreate(group_identifier="-1001234567890")
        assert data1.group_identifier == "-1001234567890"
        
        # Invalid ID (positive number)
        data2 = GroupCreate(group_identifier="1001234567890")
        assert data2.group_identifier == "@1001234567890"  # Treated as username

    def test_group_create_validator_link_formats(self):
        """Test GroupCreate validator with different link formats"""
        # Full HTTPS link
        data1 = GroupCreate(group_identifier="https://t.me/testgroup")
        assert data1.group_identifier == "https://t.me/testgroup"
        
        # HTTP link
        data2 = GroupCreate(group_identifier="http://t.me/testgroup")
        assert data2.group_identifier == "http://t.me/testgroup"
        
        # Short link
        data3 = GroupCreate(group_identifier="t.me/testgroup")
        assert data3.group_identifier == "t.me/testgroup"

    def test_group_create_required_field(self):
        """Test that group_identifier is required"""
        with pytest.raises(ValidationError):
            GroupCreate()

    def test_group_create_empty_string(self):
        """Test GroupCreate with empty string"""
        with pytest.raises(ValidationError):
            GroupCreate(group_identifier="")

    def test_group_create_whitespace_only(self):
        """Test GroupCreate with whitespace only"""
        with pytest.raises(ValidationError):
            GroupCreate(group_identifier="   ")

    def test_group_create_various_formats(self):
        """Test GroupCreate with various identifier formats"""
        # Different valid formats
        test_cases = [
            ("-1001234567890", "-1001234567890"),  # Valid ID
            ("@channel", "@channel"),              # Username with @
            ("channel", "@channel"),               # Username without @
            ("https://t.me/channel", "https://t.me/channel"),  # Full link
            ("t.me/channel", "t.me/channel"),      # Short link
        ]
        
        for input_val, expected in test_cases:
            data = GroupCreate(group_identifier=input_val)
            assert data.group_identifier == expected


class TestGroupBulkCreate:
    """Test GroupBulkCreate model"""

    def test_group_bulk_create_basic(self):
        """Test GroupBulkCreate with basic identifiers"""
        identifiers = "@group1\n@group2\n@group3"
        data = GroupBulkCreate(identifiers=identifiers)
        
        assert data.identifiers == identifiers

    def test_group_bulk_create_get_identifiers_list(self):
        """Test get_identifiers_list method"""
        identifiers = "@group1\n@group2\n-1001234567890"
        data = GroupBulkCreate(identifiers=identifiers)
        
        result = data.get_identifiers_list()
        
        assert len(result) == 3
        assert result[0] == "@group1"
        assert result[1] == "@group2"
        assert result[2] == "-1001234567890"

    def test_group_bulk_create_mixed_formats(self):
        """Test GroupBulkCreate with mixed identifier formats"""
        identifiers = """@username1
-1001234567890
https://t.me/channel1
t.me/channel2
plain_username"""
        
        data = GroupBulkCreate(identifiers=identifiers)
        result = data.get_identifiers_list()
        
        assert len(result) == 5
        assert result[0] == "@username1"
        assert result[1] == "-1001234567890"
        assert result[2] == "https://t.me/channel1"
        assert result[3] == "t.me/channel2"
        assert result[4] == "@plain_username"  # Should add @ prefix

    def test_group_bulk_create_with_empty_lines(self):
        """Test GroupBulkCreate with empty lines"""
        identifiers = """@group1

@group2


@group3"""
        
        data = GroupBulkCreate(identifiers=identifiers)
        result = data.get_identifiers_list()
        
        assert len(result) == 3
        assert result[0] == "@group1"
        assert result[1] == "@group2"
        assert result[2] == "@group3"

    def test_group_bulk_create_with_whitespace(self):
        """Test GroupBulkCreate with whitespace"""
        identifiers = """  @group1  
  @group2  
  -1001234567890  """
        
        data = GroupBulkCreate(identifiers=identifiers)
        result = data.get_identifiers_list()
        
        assert len(result) == 3
        assert result[0] == "@group1"
        assert result[1] == "@group2"
        assert result[2] == "-1001234567890"

    def test_group_bulk_create_single_identifier(self):
        """Test GroupBulkCreate with single identifier"""
        data = GroupBulkCreate(identifiers="@singlegroup")
        result = data.get_identifiers_list()
        
        assert len(result) == 1
        assert result[0] == "@singlegroup"

    def test_group_bulk_create_empty_string(self):
        """Test GroupBulkCreate with empty string"""
        data = GroupBulkCreate(identifiers="")
        result = data.get_identifiers_list()
        
        assert len(result) == 0

    def test_group_bulk_create_whitespace_only(self):
        """Test GroupBulkCreate with whitespace only"""
        data = GroupBulkCreate(identifiers="   \n   \n   ")
        result = data.get_identifiers_list()
        
        assert len(result) == 0

    def test_group_bulk_create_different_line_endings(self):
        """Test GroupBulkCreate with different line endings"""
        # Using \n line endings
        identifiers = "@group1\n@group2\n@group3"
        data = GroupBulkCreate(identifiers=identifiers)
        result = data.get_identifiers_list()
        
        assert len(result) == 3

    def test_group_bulk_create_identifier_processing(self):
        """Test identifier processing in bulk create"""
        identifiers = """channel1
@channel2
-1001234567890
https://t.me/channel3
t.me/channel4"""
        
        data = GroupBulkCreate(identifiers=identifiers)
        result = data.get_identifiers_list()
        
        assert len(result) == 5
        assert result[0] == "@channel1"         # Added @ prefix
        assert result[1] == "@channel2"         # Already has @ prefix
        assert result[2] == "-1001234567890"    # Valid ID
        assert result[3] == "https://t.me/channel3"  # Valid link
        assert result[4] == "t.me/channel4"     # Valid short link

    def test_group_bulk_create_required_field(self):
        """Test that identifiers field is required"""
        with pytest.raises(ValidationError):
            GroupBulkCreate()

    def test_group_bulk_create_long_list(self):
        """Test GroupBulkCreate with long list of identifiers"""
        # Create 50 identifiers
        identifier_list = [f"@group{i}" for i in range(50)]
        identifiers = "\n".join(identifier_list)
        
        data = GroupBulkCreate(identifiers=identifiers)
        result = data.get_identifiers_list()
        
        assert len(result) == 50
        assert result[0] == "@group0"
        assert result[49] == "@group49"


class TestGroupModelIntegration:
    """Test integration between Group models"""

    def test_create_to_group_conversion(self):
        """Test converting GroupCreate to Group creation logic"""
        create_data = GroupCreate(group_identifier="-1001234567890")
        
        # Simulate the logic that would be in the service
        group_kwargs = {
            "group_id": None,
            "group_username": None,
            "group_link": None,
            "is_active": True,
            "message_count": 0,
        }
        
        identifier = create_data.group_identifier
        if identifier.startswith("-") and identifier[1:].isdigit():
            group_kwargs["group_id"] = identifier
        
        group = Group(**group_kwargs)
        assert group.group_id == "-1001234567890"

    def test_bulk_create_processing(self):
        """Test processing GroupBulkCreate data"""
        bulk_data = GroupBulkCreate(identifiers="@group1\n@group2\n-1001234567890")
        identifiers = bulk_data.get_identifiers_list()
        
        groups = []
        for identifier in identifiers:
            create_data = GroupCreate(group_identifier=identifier)
            # Simulate creating Group objects
            if identifier.startswith("@"):
                group = Group(group_username=identifier)
            elif identifier.startswith("-") and identifier[1:].isdigit():
                group = Group(group_id=identifier)
            else:
                group = Group(group_link=identifier)
            
            groups.append(group)
        
        assert len(groups) == 3
        assert groups[0].group_username == "@group1"
        assert groups[1].group_username == "@group2"
        assert groups[2].group_id == "-1001234567890"

    def test_model_config_example(self):
        """Test that model config example is valid"""
        # The example from Group model config should be valid
        example_data = {
            "group_id": "-1001234567890",
            "group_username": "@example_group",
            "group_title": "Example Group",
            "is_active": True,
        }
        
        group = Group(**example_data)
        assert group.group_id == example_data["group_id"]
        assert group.group_username == example_data["group_username"]
        assert group.group_title == example_data["group_title"]
        assert group.is_active == example_data["is_active"]