from click.testing import CliRunner

from hypermodern_python import console, wikipedia


def test_random_page_uses_given_language(mock_requests_get):
    wikipedia.random_page(language="de")
    args, _ = mock_requests_get.call_args
    assert "de.wikipedia.org" in args[0]


def test_main_uses_specified_language(runner: CliRunner, mock_wikipedia_random_page):
    runner.invoke(console.main, ["--language=pl"])
    mock_wikipedia_random_page.assert_called_with(language="pl")
