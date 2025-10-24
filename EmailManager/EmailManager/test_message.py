# test_message.py

import pytest         # Import PyTest for running tests
from message import Message  # Import the Message class to test

def test_stars_empty():
    """
    Test that a Message with default priority (0) returns an empty string for stars.
    """
    # Create a message with default priority (0)
    m = Message("Alice", "Test", "Bob", "Test content")
    # Check if stars() returns an empty string because priority is 0.
    assert m.stars() == ""

def test_stars_with_priority():
    """
    Test that a Message with a priority of 3 returns three asterisks.
    """
    # Create a message with priority set to 3
    m = Message("Alice", "Test", "Bob", "Test content", priority=3)
    # Check if stars() returns "***" for priority 3.
    assert m.stars() == "***"

def test_info_contains_sender_and_subject():
    """
    Test that the info() method returns a string that includes the sender and subject.
    """
    # Create a message with specific sender and subject.
    m = Message("alice@example.com", "Important Subject", "bob@example.com", "Test content", priority=2)
    # Get the string returned by info()
    info_str = m.info()
    # Check that the stars, sender, and subject are all in the info string.
    assert m.stars() in info_str
    assert "alice@example.com" in info_str
    assert "Important Subject" in info_str
