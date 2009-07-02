import os
from pyjs import linker
from pyjs import translator
from pyjs import util

APP_HTML_TEMPLATE = """\
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

class BrowserLinker(linker.BaseLinker):

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

        base_html = APP_HTML_TEMPLATE % {'modulename': self.top_module,
                                         'title': title, 'css': css}

        fh = open (file_name, 'w')
        fh.write  (base_html)
        fh.close  ()
        return 1
