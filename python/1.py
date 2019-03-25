import glob
import itertools
import logging, inspect
import uuid
import hmac, hashlib
import zlib
import atexit
import math
import time

def foo(*args):
    print('number of args: {}'.format(len(args)))
    for i,x in enumerate(args):
        print('index={0} data={1}'.format(i, x))

foo(1,2,3)



files = glob.glob('/Users/urugang/playground/python/*.py')
print(files)


def multiple_file_types(*patterns):
    itertools.chain.from_iterable(glob.glob(pattern) for pattern in patterns)


# for filename in multiple_file_types("/Users/urugang/playground/python/*.py"):
#     print(filename)


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(filename)s:%(lineno)-4d: %(message)s',
                    datefmt='%m-%d %H:%M')

def test():
    frame, file_name, lineno, func_name, lines, index = \
        inspect.getouterframes(inspect.currentframe())[1]
    print(frame, file_name, lineno, lines, index)

test()

print(uuid.uuid1())

key= b'l'
data= b'a'
print(hmac.new(key, data, hashlib.sha256).hexdigest())

m = hashlib.sha1()
m.update(b'the quick way')
print(m.hexdigest())

string = 'hello, your name. name name name'
print('uncompressed={}, compressed={}'.format(len(string), len(zlib.compress(string.encode()))))
print(zlib.decompress(zlib.compress(string.encode())))

def shutdown():
    global start_time
    print("execution took: {0} seconds".format(start_time))

def microtime(get_as_float= False):
    if get_as_float:
        return time.time()
    else:
        return "%f %d".format(math.modf(time.time()))
start_time = microtime(False)
