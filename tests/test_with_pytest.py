from importlib.metadata import version

from minimal_template import __version__


def test_package_version_matches_metadata():
    assert version("minimal_template") == __version__
