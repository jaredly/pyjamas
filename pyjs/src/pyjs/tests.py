from zope.testing.doctestunit import DocFileSuite
import doctest
import unittest

def test_suite():
    translator = DocFileSuite('translator.txt',
                optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
                        )
    linker = DocFileSuite('linker.txt',
                optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
                        )
    s = unittest.TestSuite((translator, linker))
    return s
