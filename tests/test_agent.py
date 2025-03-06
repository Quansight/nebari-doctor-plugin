import pytest
from unittest.mock import MagicMock, patch
import pathlib

from nebari_doctor.agent import (
    tool_output_wrapper,
    message_user,
    run_agent,
    ChatResponse
)
from nebari_doctor.styling import MessageType


@pytest.fixture
def mock_display_message():
    """Mock the display_message function"""
    with patch("nebari_doctor.agent.display_message") as mock:
        yield mock


@pytest.fixture
def mock_get_user_input():
    """Mock the get_user_input function"""
    with patch("nebari_doctor.agent.get_user_input") as mock:
        mock.return_value = "Test user input"
        yield mock


@pytest.fixture
def mock_agent():
    """Mock the Agent class"""
    with patch("nebari_doctor.agent.Agent") as mock:
        agent_instance = MagicMock()
        mock.return_value = agent_instance
        
        # Mock the run_sync method
        result = MagicMock()
        result.data = ChatResponse(message="Test agent response")
        agent_instance.run_sync.return_value = result
        
        yield agent_instance


def test_tool_output_wrapper(mock_display_message):
    """Test that the tool output wrapper correctly displays tool information"""
    # Create a test function
    def test_tool():
        return "Tool result"
    
    # Apply the wrapper
    wrapped_tool = tool_output_wrapper(test_tool)
    
    # Call the wrapped function
    result = wrapped_tool()
    
    # Check that display_message was called correctly
    assert mock_display_message.call_count == 2
    # First call should be for running the tool
    assert mock_display_message.call_args_list[0][0][0] == "Running tool: test_tool"
    assert mock_display_message.call_args_list[0][0][1] == MessageType.SYSTEM
    
    # Second call should be for the tool output
    assert mock_display_message.call_args_list[1][0][0] == "Tool result"
    assert mock_display_message.call_args_list[1][0][1] == MessageType.TOOL
    
    # Check that the function returns the correct result
    assert result == "Tool result"


def test_message_user(mock_display_message, mock_get_user_input):
    """Test that message_user correctly displays a message and gets user input"""
    result = message_user("Test message")
    
    # Check that display_message was called correctly
    mock_display_message.assert_called_once_with("Test message", MessageType.AGENT)
    
    # Check that get_user_input was called
    mock_get_user_input.assert_called_once()
    
    # Check that the function returns the user input
    assert result == "Test user input"


@patch("nebari_doctor.agent.display_header")
def test_run_agent_with_input(mock_display_header, mock_display_message, mock_get_user_input, mock_agent):
    """Test running the agent with initial user input"""
    # Run the agent with initial input
    run_agent(user_input="Initial input")
    
    # Check that display_header was called
    mock_display_header.assert_called_once()
    
    # Check that the agent was run with the initial input
    mock_agent.run_sync.assert_called_with("Initial input", message_history=[])


@patch("nebari_doctor.agent.display_header")
def test_run_agent_without_input(mock_display_header, mock_display_message, mock_get_user_input, mock_agent):
    """Test running the agent without initial user input"""
    # Run the agent without initial input
    run_agent()
    
    # Check that get_user_input was called to get the initial input
    assert mock_get_user_input.call_count >= 1
    
    # Check that the agent was run with the user input
    mock_agent.run_sync.assert_called()


@patch("nebari_doctor.agent.display_header")
def test_run_agent_with_exception(mock_display_header, mock_display_message, mock_get_user_input, mock_agent):
    """Test handling exceptions in the agent"""
    # Make the agent raise an exception
    mock_agent.run_sync.side_effect = Exception("Test exception")
    
    # Run the agent
    run_agent(user_input="Initial input")
    
    # Check that an error message was displayed
    error_calls = [call for call in mock_display_message.call_args_list 
                  if call[0][1] == MessageType.ERROR]
    assert len(error_calls) >= 1
    assert "Test exception" in str(error_calls[0])
