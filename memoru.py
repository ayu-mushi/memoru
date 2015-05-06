#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import json
import random

orderfile_name  = '.memoru_order'
numerical_chars = '0123456789abcdefghijklmnopqrstuvwxyz'

class Memo:
    def __init__(self, ix, ext):
        self.index     = ix
        self.extension = ext

    def fileName(self):
        return self.index + "." + self.extension

    def make(self, content=''):
        f = open(self.fileName(), 'w')
        f.write(content)
        f.close()

    def toJSON(self):
        return json.dumps({'index': self.index, 'ext': self.extension})

    @staticmethod
    def fromJSON(s):
        d = json.loads(s)
        return Memo(ix=d['index'], ext=d['ext'])

class Order:
    def __init__(self, digits, stack=[]):
        self.digits = digits
        self.stack  = stack

    def add(self, memo):
        self.stack.append(memo)

    def getPreIxes(self):
        return map(lambda memo: rebase_num(memo.index, numerical_chars), self.stack)

    def toJSON(self):
        return json.dumps({'digits': self.digits, 'stack': map(lambda memo: {'index': memo.index, 'ext': memo.extension}, self.stack)})

    def write(self):
        f = open(orderfile_name, 'w')
        f.write(self.toJSON())
        f.close()
    
    @staticmethod
    def fromJSON(s):
       d = json.loads(s)
       return Order(digits=d['digits'], stack=map(lambda e: Memo(e['index'],e['ext']), d['stack']))

    @staticmethod
    def read():
        f     = open(orderfile_name, 'r')
        order = Order.fromJSON(f.read())
        f.close()
        return order

def memoruInit(args):
    Order(digits=args.digits).write()

# ref: http://d.hatena.ne.jp/yuheiomori0718/20121025/1351175190
def base_str(n, numChars):
    radix = len(numChars)
    if n < 0:
        raise ValueError('invalid n %s' % n)
    result = []
    while n:
        result.insert(0, n % radix)
        n /= radix
        if n == 0:
            break
    s = ''.join([numChars[i] for i in result])
    return s

# a inverse fn of base_str
def rebase_num(s, numChars):
    radix  = len(numChars)
    c      = [x for x in reversed(map(lambda c: numChars.index(c), s))]
    T      = 0
    i      = len(c) - 1
    while i >= 0:
        T += c[i] * (radix ** i)
        i -= 1 
    return T

# rand & unique index as string
# preIxes: 既出の番号
def mkIx(digits, preIxes, numChars):
    r = random.randint(0, (len(numChars) ** digits - 1) - len(preIxes))
    i = r + len(filter(lambda x: r >= x, preIxes))
    while i in preIxes:
        i += 1
    return base_str(i, numChars)

def memoGen(args):
    order = Order.read()
    memo  = Memo(mkIx(digits=order.digits, preIxes=order.getPreIxes(), numChars=numerical_chars), args.ext)
    memo.make()
    order.add(memo)
    order.write()
    print memo.fileName()

def trans(args):
    for f in args.file:
        order   = Order.read()
        splited = (os.path.splitext(f.name)[1])
        ext     = splited[1:len(splited)]
        memo    = Memo(mkIx(digits=order.digits, preIxes=order.getPreIxes(), numChars=numerical_chars), ext)
        content = f.read()

        memo.make(content)
        order.add(memo)
        order.write()
        os.remove(f.name)
        print memo.fileName()

if __name__ == '__main__':
    parser     = argparse.ArgumentParser(description='Generate memo files and operate for memos.')
    subparsers = parser.add_subparsers()

    initCmd = subparsers.add_parser('init', help='initialize a directory for memoru')
    initCmd.add_argument('--digits', '-d', type=int, default=5, help='digits of max memo number') #桁
    initCmd.set_defaults(func=memoruInit)

    genCmd = subparsers.add_parser('gen', help='generate a memo file and return the filename')
    genCmd.add_argument('ext', type=str, help='memo file name extension')
    genCmd.set_defaults(func=memoGen)

    transCmd = subparsers.add_parser('trans', help='transform a file to a memo')
    transCmd.add_argument('file', nargs='+', type=argparse.FileType('r'), help='file object which will transform to a memo')
    transCmd.set_defaults(func=trans)

    args = parser.parse_args()
    args.func(args)
