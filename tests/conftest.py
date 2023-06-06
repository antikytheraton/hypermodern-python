from click.testing import CliRunner
import pytest


@pytest.fixture
def runner(mocker):
    return CliRunner()


@pytest.fixture
def mock_wikipedia_random_page(mocker):
    return mocker.patch("hypermodern_python.wikipedia.random_page")


@pytest.fixture
def mock_requests_get(mocker):
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Lorem Ipsum",
        "extract": "Lorem ipsum dolor sit amet",
    }
    return mock
