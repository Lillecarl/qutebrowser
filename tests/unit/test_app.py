# SPDX-FileCopyrightText: Freya Bruhin (The Compiler) <mail@qutebrowser.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Tests for the qutebrowser.app module."""

import os
import sys

import pytest
from qutebrowser.qt.core import QBuffer, QUrl

from qutebrowser.misc import objects
from qutebrowser import app


def test_on_focus_changed_issue1484(monkeypatch, qapp, caplog):
    """Check what happens when on_focus_changed is called with wrong args.

    For some reason, Qt sometimes calls on_focus_changed() with a QBuffer as
    argument. Let's make sure we handle that gracefully.
    """
    monkeypatch.setattr(objects, 'qapp', qapp)

    buf = QBuffer()
    app.on_focus_changed(buf, buf)

    expected = "on_focus_changed called with non-QWidget {!r}".format(buf)
    assert caplog.messages == [expected]


@pytest.mark.parametrize('url, expected', [
    # The script path, when Python runs qutebrowser as a script.
    (QUrl.fromLocalFile('/nix/store/x/bin/.qutebrowser-wrapped'), True),
    # A URL from the command line, which Cocoa reads as a relative path.
    (QUrl.fromLocalFile(os.path.abspath('about:blank')), True),
    (QUrl.fromLocalFile('/home/user/page.html'), False),
    (QUrl('about:blank'), False),
])
def test_is_launch_argument(monkeypatch, url, expected):
    monkeypatch.setattr(sys, 'orig_argv', [
        'python3', '/nix/store/x/bin/.qutebrowser-wrapped',
        '--basedir', '/tmp/base', 'about:blank',
    ])
    assert app._is_launch_argument(url) == expected
