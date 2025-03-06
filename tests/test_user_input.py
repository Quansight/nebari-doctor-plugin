import pytest
from unittest.mock import patch

from nebari_doctor.styling import get_user_input


@patch("nebari_doctor.styling.Prompt.ask")
def test_get_user_input_default_prompt(mock_ask):
    """Test get_user_input with default prompt"""
    mock_ask.return_value = "Test input"
    
    result = get_user_input()
    
    # Check that Prompt.ask was called with the default prompt
    mock_ask.assert_called_once()
    args = mock_ask.call_args[0][0]
    assert "User" in args
    
    # Check that the function returns the input
    assert result == "Test input"


@patch("nebari_doctor.styling.Prompt.ask")
def test_get_user_input_custom_prompt(mock_ask):
    """Test get_user_input with custom prompt"""
    mock_ask.return_value = "Test input"
    
    result = get_user_input("Custom prompt")
    
    # Check that Prompt.ask was called with the custom prompt
    mock_ask.assert_called_once()
    args = mock_ask.call_args[0][0]
    assert "Custom prompt" in args
    
    # Check that the function returns the input
    assert result == "Test input"
