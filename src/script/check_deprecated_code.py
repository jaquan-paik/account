import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))

from lib.docstring import inspect_deprecated  # flake8: noqa: E402

src_path = os.path.dirname(os.getcwd())
deprecated_reports = inspect_deprecated.inspect_path(src_path)
for report in deprecated_reports:
    print("[DEPRECATED] %s" % report)

exit_code = 0 if len(deprecated_reports) == 0 else 1
sys.exit(exit_code)
