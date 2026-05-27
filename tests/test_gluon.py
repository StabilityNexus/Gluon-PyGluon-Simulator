"""Tests for gluon."""

from stability_nexus.gluon import __version__


def test_version() -> None:
    """Test that version is set."""
    assert __version__ == "1.0.0"
