# -*- coding: utf-8 -*-
"""docbuild — モジュール群から文書を組み立てるビルド。設計は ../DESIGN.md。"""
from .index import Index, load_paths
from .module import Module
from .heading import shift_headings
from .token import Resolver
from .assemble import build_document
