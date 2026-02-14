"""Tests for specs.parser."""

import pytest
from pathlib import Path
from specs import parser


def test_load_spec_stub_raises():
    with pytest.raises(NotImplementedError):
        parser.load_spec(Path("specs/examples/churn_investigation.yml"))


def test_validate_spec_stub_raises():
    with pytest.raises(NotImplementedError):
        parser.validate_spec({"objective": "test"})
