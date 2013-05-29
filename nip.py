import subprocess
import json


def send(command, **arguments):
    "send a JSON command through a pipe and get back the result."
    command_dict = dict(
        command=command,
        **arguments)
    node_process.stdin.write(json.dumps(command_dict))
    return to_proxy(json.loads(node_process.stdout.readline()))

def to_proxy(representation):
    obj, typ = representation['obj'], representation['type']

    if typ == 'undefined':
        return JSUndefined
    elif typ in ('number', 'boolean', 'string') or obj is None:
        'json.loads() does The Right Thing for these types and null'
        return obj
    else:
        return JSObject()  # pass some handle to JSLand here?

node_process = subprocess.Popen(
    ['node', 'nip.js'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE)

class JSUndefined(object):
    __repr__ = __str__ = lambda self: 'undefined'
    __bool__ = __int__ = lambda self: 0

class JSObject(object):
    def __init__(self):
        def get_attr(self, attr):
            return send('attr', attr=attr)

        def call(self, *args):
            return send('call', arguments=args)

        self.__getitem__ = get_attr
        self.__call__ = call
    
    def __getitem__(self, item):
        return self.__getitem__(self, item)

def eval(expr):
    "create a JSObject by eval()ing a javascript expression"
    return send('eval', expression=expr)

def require(module):
    "create a JSObject by require()ing a module"
    return eval('require("%s")' % module)

if __name__ == '__main__':
    obj = eval('process')
    assert obj['argv'][0] == 'node'  # this fails on windows I think.. It'd be node.exe.

