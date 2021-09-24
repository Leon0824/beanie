import pytest
from pydantic import ValidationError

from tests.odm.models import DocumentWithPydanticConfig


def test_pydantic_config():
    doc = DocumentWithPydanticConfig(num_1=2)
    print(doc.Config)
    print(doc.Config.validate_assignment)
    with pytest.raises(ValidationError):
        doc.num_1 = "wrong"
