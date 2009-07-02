import translator
import os
import sys
import util

_path_cache= {}
def module_path(name, path=None):
    # TODO: check relative
    path = path or sys.path
    global _path_cache
    k = (name, tuple(sorted(path)))
    if k in _path_cache:
        return _path_cache[k]
    parts = name.split('.')
    candidates = []
    tail = []
    packages = {}
    modules = {}
    for pn in parts:
        tail.append(pn)
        for p in path:
            cp = os.path.join(*([p] + tail))
            if os.path.isdir(cp) and os.path.exists(
                os.path.join(cp, '__init__.py')):
                packages['.'.join(tail)] = os.path.join(cp, '__init__.py')
            elif os.path.exists(cp + '.py'):
                modules['.'.join(tail)] = cp + '.py'
    res = None
    if modules:
        assert len(modules)==1
        res = modules.values()[0]
    elif packages:
        res = packages[sorted(packages)[-1]]
    _path_cache[k] = res
    return res

class BaseLinker(object):

    def __init__(self, top_module, output='output',
                 debug=False, js_libs=[], platforms=[], path=[]):
        self.js_path = os.path.abspath(output)
        self.path = path
        self.platforms = platforms
        self.top_module = top_module
        self.output = os.path.abspath(output)
        self.js_libs = js_libs

    def __call__(self):
        self.done = {}
        self.dependencies = {}
        self.visit_start()
        for platform in [None] + self.platforms:
            self.visit_start_platform(platform)
            self.visit_modules([self.top_module], platform)
            self.visit_end_platform(platform)
        self.visit_end()

    def visit_modules(self, module_names, platform=None):
        prefix = ''
        all_names = []
        for mn in module_names:
            prefix = ''
            for part in mn.split('.')[:-1]:
                pn = prefix + part
                prefix = pn + '.'
                if pn not in all_names:
                    all_names.append(pn)
            all_names.append(mn)

        for mn in all_names:
            # TODO: check relative
            p = module_path(mn, path=self.path)
            if mn==self.top_module:
                self.top_module_path = p
            override_path=None
            if platform:
                override_path = module_path('__%s__.%s' % (
                    platform, mn))
            if override_path:
                self.visit_module(p, [override_path], platform, module_name=mn)
            else:
                self.visit_module(p, [], platform, module_name=mn)

    def visit_start(self):
        pass

    def visit_start_platform(self, platform):
        pass

    def visit_end_platform(self, platform):
        pass

    def visit_end(self):
        pass

