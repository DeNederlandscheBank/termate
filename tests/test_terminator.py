#!/usr/bin/env python

"""Tests for `terminator` package."""


import unittest
from click.testing import CliRunner

from determinator import determinator


class TestTerminator(unittest.TestCase):
    """Tests for `terminator` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def test_000_something(self):
        """Test something."""
        t = determinator.TbxDocument()
        params = {"sourceDesc": "TBX file, created via dnb/determinator"}
        t.generate(params)
        c = {
            "id": "c1",
            "lang": {
                "en": [
                    [
                        {"type": "term", "text": "open cluster"},
                        {
                            "type": "note",
                            "text": "Another name for an open star cluster. They are often termed Galactic Clusters because they are found mainly in the plane of our galaxy. If you were to view our galaxy from afar, you would find that all the open/galactic clusters lie within the spiral arms of the galaxy.",
                        },
                        {
                            "type": "note",
                            "text": "N-Source: \nhttp://www.delscope.demon.co.uk/astronomy/glossary.htm#G",
                        },
                        {
                            "type": "descrip",
                            "attrib": {"reliabilityCode": "9"},
                        },
                    ]
                ],
                "es": [[{"type": "term", "text": "cúmulo abierto"}]],
            },
        }

        t.add_conceptEntry(c)

        t.write("data//test.tbx")

        print(t.validate())

        t = determinator.TbxDocument().open(
            "data//examples//Example_Astronomy_DCA_VALID.tbx"
        )
        print(t.validate())

    # def test_command_line_interface(self):
    #     """Test the CLI."""
    #     runner = CliRunner()
    #     result = runner.invoke(cli.main)
    #     assert result.exit_code == 0
    #     assert 'terminator.cli.main' in result.output
    #     help_result = runner.invoke(cli.main, ['--help'])
    #     assert help_result.exit_code == 0
    #     assert '--help  Show this message and exit.' in help_result.output
