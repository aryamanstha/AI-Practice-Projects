import pytest
from unittest.mock import patch, MagicMock
from LLM.prompt_template.prompt_test import generate_response, zero_shot_prompting, few_shot_prompting, chain_of_thought,react_prompting


# UNIT TEST: Mock OpenAI API Response
@patch("LLM.prompt_template.prompt_test.client.chat.completions.create")
def test_generate_response(mock_openai):
    """Test generate_response function with a mocked API response."""
    mock_openai.return_value.choices = [
        MagicMock(message=MagicMock(content="Mocked response"))
    ]

    response = generate_response("Test prompt")
    assert response == "Mocked response"
    mock_openai.assert_called_once()

# UNIT TEST: Test Zero-Shot Prompting (Mocked)
@patch("LLM.prompt_template.prompt_test.generate_response", return_value="Hola, ¿cómo estás hoy?")
def test_zero_shot_prompting(mock_generate_response):
    """Test zero-shot prompting translation function."""
    response = zero_shot_prompting()
    assert response == "Hola, ¿cómo estás hoy?"
    mock_generate_response.assert_called_once()

#  UNIT TEST: Test Few-Shot Prompting (Mocked)
@patch("LLM.prompt_template.prompt_test.generate_response", return_value="Bonjour! Comment ça va?")
def test_few_shot_prompting(mock_generate_response):
    """Test few-shot prompting translation function."""
    response = few_shot_prompting()
    assert response == "Bonjour! Comment ça va?"
    mock_generate_response.assert_called_once()

#  UNIT TEST: Test Chain of Thought (Mocked)
@patch("LLM.prompt_template.prompt_test.generate_response", return_value="He has 12 apples.")
def test_chain_of_thought(mock_generate_response):
    """Test chain-of-thought reasoning function."""
    response = chain_of_thought()
    assert response == "He has 12 apples."
    mock_generate_response.assert_called_once()

# UNIT TEST: Test ReAct Prompting (Mocked)
@patch("LLM.prompt_template.prompt_test.generate_response", return_value="Try Café Aroma on 5th Street.")
def test_react_prompting(mock_generate_response):
    """Test ReAct prompting function."""
    response = react_prompting()
    assert response == "Try Café Aroma on 5th Street."
    mock_generate_response.assert_called_once()

# INTEGRATION TEST: Call Real OpenAI API (Optional)
@pytest.mark.integration
def test_integration_real_openai():
    """Test real API response (requires API key)."""
    response = zero_shot_prompting()
    assert isinstance(response, str) and len(response) > 0

if __name__ == "__main__":
    pytest.main()
