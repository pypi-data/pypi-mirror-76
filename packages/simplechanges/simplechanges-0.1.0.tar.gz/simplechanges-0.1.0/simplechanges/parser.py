# coding=utf-8
#
# parser.py
# Simple Changes
#
# Created by Marquis Kurt on 08/08/20.
# Copyright © 2020 Marquis Kurt. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

from typing import List, Tuple, Literal


class SimpleChangesTokenizeError(Exception):
    """An error occurred when tokenizing the changes file."""


class SimpleChangesParseError(Exception):
    """An error occurred when parsing the changes file."""


class SimpleChangesParser(object):
    _file_stream = []       # type: List[str]
    _changes = {}           # type: dict[str, List[str]]
    _tokens = []            # type: List[Tuple[str, str]]
    _latest = ""

    def __init__(self, path):
        # type: (SimpleChangesParser, str) -> None
        """Initialize the parser.

        Args:
            path (str): The path to the changes file to parse.
        """
        with open(path, 'r') as file:
            self._file_stream = list(file.read())
        self._changes = {}
        self._tokens = []

    @property
    def _has_more_characters(self):
        # type: (SimpleChangesParser) -> bool
        """Whether or not the file stream contains more characters."""
        return len(self._file_stream) > 0

    def _next_character(self):
        # type: (SimpleChangesParser) -> str
        """Get the next character in the file stream."""
        return self._file_stream.pop(0)

    @property
    def versions(self):
        # type: (SimpleChangesParser) -> dict[str, List[str]]
        """The parsed changelog."""
        return self._changes

    @property
    def latest(self):
        # type: (SimpleChangesParser) -> Tuple[str, List[str]]
        """The latest version in the changelog and its associated notes."""
        return self._latest, self._changes[self._latest]

    def _unread_character(self, char):
        # type: (SimpleChangesParser, str) -> None
        """Unread the character and add it back to the file stream.

        Args:
            char (str): The character to add back to the file stream.
        """
        self._file_stream += char

    def _tokenize_once(self):
        # type: (SimpleChangesParser) -> None
        """Generate a single token and add it to the list of tokens.

        Raises: SimpleChangesTokenizeError if the token is not recognized.
        """
        current_token = ""

        # type: Literal["COMMENT", "VERSION", "NOTE", "NULL"]
        token_type = "NULL"
        # type: Literal['START', 'INP', 'ERR', 'FINISH',  "MAYBE"]
        current_state = "START"

        if not self._has_more_characters:
            return

        while current_state not in ["FINISH", "ERROR"]:
            if not self._has_more_characters:
                return
            current_character = self._next_character()

            if current_state == "START":
                if current_character == "[":
                    token_type = "VERSION"
                elif current_character == "-":
                    token_type = "NOTE"
                elif current_character == "/":
                    current_state = "MAYBE"
                elif current_character in ["\n", "\t", " "]:
                    continue
                else:
                    token_type = "NULL"
                    current_state = "ERR"
                if token_type not in ["NOTE", "VERSION"]:
                    current_token += current_character
                if current_state != "MAYBE":
                    current_state = "INP"
            elif current_state == "MAYBE":
                if current_character == "*":
                    token_type = "COMMENT"
                    current_state = "INP"
                elif current_character == "/":
                    current_state = "FINISH"
                else:
                    token_type = "NULL"
                    current_state = "ERR"
                current_token += current_character
            elif current_state == "INP":
                if token_type == "COMMENT" and current_character == "*":
                    current_state = "MAYBE"
                    current_token += current_character
                elif token_type == "VERSION" and current_character == "]":
                    current_state = "FINISH"
                elif token_type == "NOTE" and current_character == "\n":
                    current_state = "FINISH"
                else:
                    current_token += current_character

        if current_state == "ERR":
            raise SimpleChangesTokenizeError(current_token)

        if token_type == "NOTE":
            current_token = current_token.replace("\n", "")
            if current_token.startswith(" "):
                current_token = current_token[1:]

        self._tokens.append((token_type, current_token))

    def _tokenize_all(self):
        # type: (SimpleChangesParser) -> None
        """Create the list of tokens while the file stream is not empty."""
        while self._has_more_characters:
            self._tokenize_once()

    def parse(self):
        # type: (SimpleChangesParser) -> None
        """Parse the file contents into a dictionary."""
        self._tokenize_all()
        current_key = ""
        current_notes = []
        changelog = {}

        tokens = self._tokens
        while len(tokens) > 0:
            c_type, c_token = tokens.pop(0)
            if c_type == "COMMENT":
                continue
            elif c_type == "NOTE":
                current_notes.append(c_token)
            elif c_type == "VERSION":
                if current_key:
                    if current_key in changelog:
                        raise SimpleChangesParseError(
                            "Version %s is duplicated." % (current_key))
                    changelog[current_key] = current_notes
                    current_notes = []
                if not self._latest:
                    self._latest = c_token
                current_key = c_token
            else:
                raise SimpleChangesParseError(
                    "Unexpected token encountered: %s" % (c_token))
        if current_key and current_notes:
            changelog[current_key] = current_notes
        self._changes = changelog
