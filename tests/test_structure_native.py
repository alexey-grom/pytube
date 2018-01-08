# -*- coding: utf-8 -*-
from functools import partial
from json import dumps as _dumps

import pytest

from pytube.structure import filters
from pytube.structure import flags
from pytube.structure import Schema as x


dumps = partial(_dumps, sort_keys=True)

testdata = {
    'named': {
        'items': [
            {
                'id': 1,
                'inner': {
                    'title': 'first',
                },
                'other': [
                    0, 1,
                ],
                'unique': {
                    'two': 2,
                },
            },
            {
                'id': 2,
                'inner': {
                    'title': 'second',
                    'description': [
                        'line 1',
                        'line 2',
                        'line 3',
                    ],
                },
                'other': [
                    2, 3,
                ],
                'nested': {
                    'one': 1,
                },
            },
        ],
    },
}

short_testlist = [
    [
        testdata,
        x(
            ('named', 'items', 'inner', ),
            title='title',
        ),
        [
            {'title': 'first'},
            {'title': 'second'},
        ],
    ],
]

testcases = [
    [
        testdata,
        x(),
        testdata,
    ],

    [
        testdata,
        x(
            ('named', 'items'),
            x(
                'inner',
                title='title',
            ),
            id='id',
        ),
        [
            {'title': 'first', 'id': 1},
            {'title': 'second', 'id': 2},
        ],
    ],

    [
        testdata,
        x(
            ('named', 'items'),
            x('id'),
        ),
        [1, 2],
    ],

    [
        testdata,
        x(
            ('named', 'items'),
            x('id'),
            x('other'),
            x(('inner', 'title')),
        ),
        [
            [1, [0, 1], 'first'],
            [2, [2, 3], 'second'],
        ],
    ],

    [
        testdata,
        x(
            ('named', 'items'),
            id=x('id'),
        ),
        [{'id': 1}, {'id': 2}],
    ],

    [
        testdata,
        x(
            ('named', 'items'),
            id=x(filters.str_cast, 'id'),
        ),
        [{'id': '1'}, {'id': '2'}],
    ],

    [
        testdata,
        x(
            lambda value, *args: sum(value),
            ('named', 'items', 'id'),
        ),
        3,
    ],

    [
        testdata,
        x(
            filters.join(' '),
            ('named', 'items', 1, 'inner', 'description'),
        ),
        'line 1 line 2 line 3',
    ],

    [
        testdata,
        x(
            flags.KEEP_EMPTY,
            ('named', 'items'),
            item=x(
                'nested',
                one=x(
                    'one',
                ),
            ),
        ),
        [{'item': {'one': None}}, {'item': {'one': 1}}],
    ],

    [
        testdata,
        x(
            ('named', 'items'),
            item=x(
                'nested',
                one=x(
                    'one',
                ),
            ),
        ),
        [{'item': None}, {'item': {'one': 1}}],
    ],

    [
        testdata,
        x(
            ('named', 'items'),
            x(
                one=x(
                    filters.default('-'),
                    ('nested', 'one', ),
                ),
                two=x(
                    filters.default('-'),
                    ('unique', 'two', ),
                ),
            ),
        ),
        [{'one': '-', 'two': 2}, {'one': 1, 'two': '-'}],
    ],

    [
        testdata,
        x(
            ('named', 'items'),
            x(
                filters.drop_null_values,
                one=('nested', 'one', ),
                two=('unique', 'two', ),
            ),
        ),
        [{'two': 2}, {'one': 1}],
    ],

    [
        testdata,
        x(
            ('named', 'items'),
            x(
                'inner',
                title='title',
                description=x(filters.join('\n'), 'description'),
            ),
            id='id',
        ),
        [
            {
                'title': 'first',
                'id': 1,
                'description': '',
            },
            {
                'title': 'second',
                'id': 2,
                'description': 'line 1\nline 2\nline 3',
            },
        ],
    ],

]


@pytest.mark.parametrize('data, scheme, result', short_testlist)
def test_short(data, scheme, result):
    assert dumps(scheme(data)) == dumps(result)


@pytest.mark.parametrize('data, scheme, result', testcases)
def test_simple(data, scheme, result):
    assert dumps(scheme(data)) == dumps(result)


def test_strict():
    with pytest.raises(KeyError):
        x(
            flags.STRICT,
            ('named', 'items', ),
            x(
                ('unique', ),
            ),
        )(testdata)

    with pytest.raises(KeyError):
        x(
            flags.STRICT,
            ('named', 'items', 'unique', ),
        )(testdata)
