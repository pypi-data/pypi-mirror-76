#!/usr/bin/env python

"""Tests for `geospots` package."""


import unittest
from click.testing import CliRunner

from geospots import geospots
from geospots import cli


class TestGeospots(unittest.TestCase):
    """Tests for `geospots` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_return_iso(self):
        """Test that an isochrone within Indicium returns a polygon."""
        test_this = return_iso(
            api_key='5b3ce3597851110001cf62488b98dba3f6c7452b9d391c8306afa037',
            locations=[[-48.51057, -27.57482]],
            profile='driving-car',
            range=[5]
        )


    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'geospots.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
