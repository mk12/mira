"""This module defines custom error types for Mira."""


class InvalidAttribute(Exception):
    """Error for an invalid attribute on a model."""

    def __init__(self, attribute, value, message):
        self.attribute = attribute
        self.value = value
        self.message = message

    def __str__(self):
        return "Invalid value '{}' for attribute '{}': {}".format(
            self.value, self.attribute, self.message
        )
