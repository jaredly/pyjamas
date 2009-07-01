import translator
import os
import sys

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
            override_path = None
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

class BrowserLinker(BaseLinker):

    def visit_module(self, module_path, overrides, platform=None,
                     module_name=None):
        if platform and overrides:
            out_file = '%s.__%s__.js' % (module_path[:-3], platform)
        else:
            out_file = '%s.js' % module_path[:-3]
        if platform is None:
            if out_file in self.done.get(platform, []):
                return
            deps = translator.translate([module_path] +  overrides,
                                        out_file, module_name=module_name)
            self.dependencies[out_file] = deps
        else:
            deps = self.dependencies[out_file]
        if platform in self.done:
            self.done[platform].append(out_file)
        else:
            self.done[platform] = [out_file]
        self.visit_modules(deps, platform)

    def visit_start(self):
        if not os.path.exists(self.output):
            os.makedirs(self.output)

    def visit_end_platform(self, platform):
        if not platform:
            return
        done = self.done[platform]
        out_path = os.path.join(
            self.output,
            '.'.join((self.top_module, platform, 'cache.html')))
        out_file = file(out_path, 'w')
        for p in done:
            f = file(p)
            out_file.write(f.read())
            f.close()
        out_file.close()


