#!/usr/bin/env python

"""Tests for `whitex` package."""

from textwrap import dedent
import pytest

from click.testing import CliRunner

from whitex import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface(tmpdir):
    """Test the CLI."""
    input_file = tmpdir / 'input.tex'
    input_content = dedent(
        """\
        Because   of $$a+b=c$$ ({\\it Pythogoras}),
        % @dude, let's go bowling
        and $y=2^ng$ with $n=1,...,10$,
        we have ${\\Gamma \\over 2}=8.$
        """
    )
    input_file.write(input_content)

    expected_content = dedent(
        """\
        Because of
        \\[
        a+b = c
        \\]
        (\\textit{Pythogoras}),
        and $y = 2^n g$ with $n = 1,\\dots,10$,
        we have $\\frac{\\Gamma}{2} = 8$.
        """
    )

    output_file = tmpdir / 'output.tex'

    runner = CliRunner()
    result = runner.invoke(cli.main, [str(input_file), str(output_file)])
    assert result.exit_code == 0

    with open(output_file, 'r') as out:
        assert expected_content == out.read()

    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
