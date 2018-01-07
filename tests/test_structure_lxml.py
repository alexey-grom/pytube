# -*- coding: utf-8 -*-
from functools import partial
from json import dumps as _dumps

import pytest
from lxml.etree import fromstring

from pytube.structure import EtreeSchema as x
from pytube.structure import filters
from pytube.structure import flags


dumps = partial(_dumps, sort_keys=True)

testdata = """
    <issue index="2">
        <title>XML today</title>
        <date>12.09.98</date>
        <about>XML</about>
        <home-url>www.j.ru/issues/</home-url>
        <number>448</number>
        <detail>
            <description>
                issue 2
                detail description
            </description>
            <number>445</number>
        </detail>
        <articles>
            <article ID="3">
                <title>Issue overview</title>
                <url>/article1</url>
                <hotkeys>
                    <hotkey>language</hotkey>
                    <hotkey>marckup</hotkey>
                    <hotkey>hypertext</hotkey>
                </hotkeys>
                <article-finished/>
            </article>
            <article>
                <title>Latest reviews</title>
                <url>/article2</url>
                <author ID="3"/>
                <hotkeys>
                    <hotkey/>
                </hotkeys>
            </article>
            <article ID="4">
                <title/>
                <url/>
                <hotkeys/>
            </article>
        </articles>
    </issue>
"""

testcases = [
    [
        testdata,
        x(
            flags.MULTIPLE,
            '//issue',
            title='./title/text()',
            date='./date/text()',
            about='./about/text()',
            number=x(filters.type_cast(int), './number/text()'),
            home_url='./home-url/text()',
        ),
        [
            {
                'date': '12.09.98',
                'about': 'XML',
                'home_url': 'www.j.ru/issues/',
                'number': 448,
                'title': 'XML today',
            },
        ],
    ],

    [
        testdata,
        x(
            flags.MULTIPLE,
            '//issue',
            x(
                './detail',
                description=x(
                    lambda item, *args: ' '.join(item.split()),
                    './description/text()',
                ),
                detail_number=x(
                    filters.type_cast(int),
                    './number/text()',
                ),
            ),
            title='./title/text()',
            date='./date/text()',
        ),
        [
            {
                'detail_number': 445,
                'date': '12.09.98',
                'description': 'issue 2 detail description',
                'title': 'XML today',
            },
        ],
    ],

    [
        testdata,
        x(
            flags.MULTIPLE,
            '//issue',
            home_url='./home-url/text()',
            articles=x(
                flags.MULTIPLE,
                './articles/article',
                id='./@ID',
                title='./title/text()',
                url='./url/text()',
                hotkeys=x(
                    flags.MULTIPLE,
                    flags.KEEP_EMPTY,
                    './hotkeys',
                    hotkey='./hotkey/text()',
                ),
            ),
        ),
        [
            {
                'articles': [
                    {
                        'url': '/article1',
                        'id': '3',
                        'hotkeys': [
                            {
                                'hotkey': 'language',
                            },
                        ],
                        'title': 'Issue overview',
                    },
                    {
                        'url': '/article2',
                        'id': None,
                        'hotkeys': [
                            {
                                'hotkey': None,
                            },
                        ],
                        'title': 'Latest reviews',
                    },
                    {
                        'url': None,
                        'id': '4',
                        'hotkeys': [
                            {
                                'hotkey': None,
                            },
                        ],
                        'title': None,
                    },
                ],
                'home_url': 'www.j.ru/issues/',
            },
        ],
    ],

]


@pytest.mark.parametrize('data, scheme, result', testcases)
def test_simple(data, scheme, result):
    data = fromstring(data.encode())
    assert dumps(scheme(data)) == dumps(result)
