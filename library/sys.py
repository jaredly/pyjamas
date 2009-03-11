# the platform name (PyV8, smjs, Mozilla, IE6, Opera, Safari etc.)
global platform
platform = '' # to be updated by app, on compile

# a dictionary of module override names (platform-specific)
global overrides
overrides = None # to be updated by app, on compile

global stacktrace
stacktrace = None 

def addstack(linedebug):
    JS("""
        if (pyjslib.bool((sys.stacktrace === null))) {
            sys.stacktrace = new pyjslib.List([]);
        }
        sys.stacktrace.append(linedebug);
    """)
def popstack():
    JS("""
        sys.stacktrace.pop()
    """)

def printstack():
    JS("""
        var res = '';

        var __l = sys.stacktrace.__iter__();
        try {
            while (true) {
                var l = __l.next();
                res +=  ( l + '\\n' ) ;
            }
        } catch (e) {
            if (e != StopIteration) {
                throw e;
            }
        }

        return res;
    """)
