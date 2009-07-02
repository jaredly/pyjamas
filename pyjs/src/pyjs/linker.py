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
        # look if we have a public dir
        dir_name = os.path.dirname(module_path)
        if not dir_name in self.merged_public:
            public_folder = os.path.join(dir_name, 'public')
            if os.path.isdir(public_folder):
                util.copytree_exists(public_folder,
                                     self.output)
                self.merged_public.add(dir_name)
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
        self.merged_public = set()

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


    def visit_end(self):
        html_output_filename = os.path.join(self.output, self.top_module + '.html')
        if not os.path.exists(html_output_filename):
            # autogenerate
            self._create_app_html(html_output_filename)

    def _create_app_html(self, file_name):
        """ Checks if a base HTML-file is available in the PyJamas
        output directory.
        If the HTML-file isn't available, it will be created.

        If a CSS-file with the same name is available
        in the output directory, a reference to this CSS-file
        is included.

        If no CSS-file is found, this function will look for a special
        CSS-file in the output directory, with the name
        "pyjamas_default.css", and if found it will be referenced
        in the generated HTML-file.

        [thank you to stef mientki for contributing this function]
        """

        base_html = """\
        <html>
        <!-- auto-generated html - you should consider editing and
        adapting this to suit your requirements
        -->
        <head>
        <meta name="pygwt:module" content="%(modulename)s">
        %(css)s
        <title>%(title)s</title>
        </head>
        <body bgcolor="white">
        <script language="javascript" src="pygwt.js"></script>
        </body>
        </html>
        """
        # if html file in output directory exists, leave it alone.
        if os.path.exists(file_name):
            return 0
        if os.path.exists(
            os.path.join(self.output, self.top_module + '.css' )):
            css = "<link rel='stylesheet' href='" + self.top_module + ".css'>"
        elif os.path.exists(
            os.path.join(self.output, 'pyjamas_default.css' )):
            css = "<link rel='stylesheet' href='pyjamas_default.css'>"
        else:
            css = ''

        title = 'PyJamas Auto-Generated HTML file ' + self.top_module

        base_html = base_html % {'modulename': self.top_module,
                                 'title': title, 'css': css}

        fh = open (file_name, 'w')
        fh.write  (base_html)
        fh.close  ()
        return 1
