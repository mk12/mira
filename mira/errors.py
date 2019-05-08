"""This module defines custom error types."""


class InvalidAttribute(Exception):
    """Error for an invalid attribute on a model."""

    def __init__(self, attribute, value, message):
        self.attribute = attribute
        self.value = value
        self.message = message

    def __str__(self):
        return (
            f"Invalid value '{self.value}' for attribute '{self.attribute}'"
            f": {self.message}"
        )
