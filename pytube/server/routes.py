# -*- coding: utf-8 -*-
from . import views


def install(app):
    app.router.add_route('*', '/', views.HelloView)
    app.router.add_route('*', '/slow/', views.SlowView)
    app.router.add_route('*', '/video/', views.VideoView)
    app.router.add_route('*', '/search-keywords/', views.SearchKeywordsView)
    app.router.add_route('*', '/search/', views.SearchView)
