# Copyright (c) 2020 Tulir Asokan
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from lxml import html

HTMLNode = html.HtmlElement


def read_html(data: str) -> HTMLNode:
    return html.fromstring(data)
