import uuid

from cerberus import Validator as Cerberus


class Validator(Cerberus):
    def __init__(self, *args, **kwargs):
        super(Validator, self).__init__(*args, **kwargs)

    def _check_with_uuid(self, field, value):
        """
        Custom checker for validating UUIDs
        example::
            schema = {"contact_uuid": {"type": "string", "check_with": "uuid"}}
        :param field: The field being checked
        :param value: The value to check
        """
        if value is not None:
            try:
                uuid.UUID(value)
            except ValueError:
                self._error(field, "Must be a UUID")

    def _normalize_coerce_to_string(self, value):
        """
        Custom normalizer for coercing string based "None" values to real None values.
        example::
            schema = {"forename": {"type": "string", "coerce": "to_string"}}
        :param value: The value to coerce
        :return: The coerced value
        """
        if value == "None" or value is None:
            return ""
        return str(value)

    def _normalize_coerce_to_nullable_string(self, value):
        """
        Customer normalizer for coercing values into None or strings.
        example::
            schema = {"forename": {"type": "string", "nullable": True, "coerce": "to_nullable_string"}}
        :param value: The value to coerce
        :return: The coerced value
        """
        if value == "" or value == "None" or value is None:
            return None
        return str(value)

    def _normalize_coerce_to_integer(self, value):
        """
        Custom normalizer for coercing string based "None" values to real None values.
        example::
            schema = {"forename": {"type": "integer", "coerce": "to_integer"}}
        :param value: The value to coerce
        :return: The coerced value
        """
        if value == "" or value == "None" or value is None:
            return 0
        return int(value)

    def _normalize_coerce_to_nullable_integer(self, value):
        """
        Customer normalizer for coercing values into None or ints.
        example::
            schema = {"forename": {"type": "integer", "nullable": True, "coerce": "to_nullable_integer"}}
        :param value: The value to coerce
        :return: The coerced value
        """
        if value == "" or value == "None" or value is None:
            return None
        return int(value)

    def _normalize_coerce_to_bool(self, value):
        """
        Custom normalizer for coercing string based boolean values to real boolean.
        example::
            schema = {"address_as_pupil": {"type": "boolean", "coerce": "to_bool"}}
        :param value: The value to coerce
        :return: The coerced value
        """
        if value == "True":
            return True
        if value == "" or value == "False" or value == "None" or value is None:
            return False
        return value
