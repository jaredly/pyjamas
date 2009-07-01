from zope.testing.doctestunit import DocFileSuite

def test_suite():
    translator = DocFileSuite('translator.txt', tearDown=tearDown,
                    optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
                              )
    s = unittest.TestSuite((translator,))
    return s
