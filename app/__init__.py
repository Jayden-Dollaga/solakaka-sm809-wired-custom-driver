"""app -- the PySide6 desktop GUI for the SM809 Pro."""

import logging as _logging

# Quiet by default (tests, library imports); app.logging_setup installs the
# console and file handlers when the application actually starts.
if not _logging.getLogger("sm809").handlers:
    _logging.getLogger("sm809").addHandler(_logging.NullHandler())
