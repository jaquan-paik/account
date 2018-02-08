from datetime import datetime, timedelta

from django.test import TestCase

from lib.docstring.inspect_deprecated import _inspect_docstring, _parse_deprecated_date


class DeprecatedInspectorTestCase(TestCase):
    def _dummy_docstring(self, is_deprecated: bool):
        deprecated_date = None
        if is_deprecated:
            deprecated_date = datetime.now() - timedelta(1)
        else:
            deprecated_date = datetime.now() + timedelta(1)

        docstring = """
       this is dummy docstring
       :deprecated: %s
       """ % deprecated_date.strftime('%Y.%m.%d')

        return docstring

    def test_parse_deprecated_date(self):
        self.assertIsNotNone(_parse_deprecated_date(self._dummy_docstring(True)))
        self.assertIsNotNone(_parse_deprecated_date(self._dummy_docstring(False)))

    def test_inspect_docstring(self):
        self.assertIsNotNone(_inspect_docstring(self._dummy_docstring(True)))
        self.assertIsNone(_inspect_docstring(self._dummy_docstring(False)))
