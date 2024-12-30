import pytest
from helper import sanitise, advanced_strip


def test_sanitise_html():
    """
    tests sanitise function removes HTML tags
    """
    test_string = "This is a <b>test string</b> with HTML."
    cleaned_string = sanitise(test_string)
    assert cleaned_string == "This is a test string with HTML."


def test_sanitise_unicode():
    """
    tests sanitise function removes unicode artifacts
    """
    test_string = "This is a test string with unicode char ™."
    cleaned_string = sanitise(test_string)
    assert cleaned_string == "This is a test string with unicode char ."


def test_advanced_strip_prefix():
    """
    tests advanced_strip removes prefix occurrences
    """
    test_string = " prefixed string"
    cleaned_string = advanced_strip(test_string, ["prefixed "])
    assert cleaned_string == "string"


def test_advanced_strip_suffix():
    """
    tests advanced_strip removes suffix occurrences
    """
    test_string = "string with suffix"
    cleaned_string = advanced_strip(test_string, ["suffix"])
    assert cleaned_string == "string with"


def test_advanced_strip_multiple():
    """
    tests advanced_strip removes multiple occurrences
    """
    test_string = " prefixed string with suffix"
    cleaned_string = advanced_strip(test_string, ["prefixed ", "suffix"])
    assert cleaned_string == "string"
