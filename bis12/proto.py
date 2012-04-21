#!/usr/bin/env python


import sys
import json

n = 3
index = {}

def clean(text):
  return (
    text
    .lower()
    .replace('/', '')
    .replace('(', '')
    .replace(')', '')
    .replace(')', '')
    .replace(':', '')
    .replace('.', '')
    .replace(',', '')
    .replace(';', '')
    .replace(';', '')
    .replace('?', ' ?')
    .replace('!', ' !')
    .replace('-', ' - '))

def gramify_me_captain(line):
  line = clean(line)
  spl = line.split()
  grams = []
  for word in spl:
    for i in xrange(1,n+2):
      for j in xrange(len(word)-i+1):
        grams.append( word[j:j+i] )
  return grams

def add_to_index(_id, grams):
  for gram in grams:
    if gram not in index:
      index[gram] = set()
    index[gram].add(_id)

def query(inpt,q):
  results = set()
  results.update(index[inpt[0]])
  for wd in inpt:
    if wd in index:
      results = results.intersection(index[wd])
  rem = set()
  for r in results:
    for w in q.split():
      if (w in index and r not in index[w]) or w not in index:
        rem.add(r)
  results = results.difference(rem)
  sys.stdout.write( json.dumps(list(results)) )

if __name__ == '__main__':
  fs = sys.argv[1]

  f = open(fs,'r')

  for line in f:
    spl = line.split(':')
    _id = spl[0].strip()
    text = ' '.join(spl[1:])
    grams = gramify_me_captain(text)
    add_to_index(_id,grams)

  while True:
    sys.stdout.write('> '); sys.stdout.flush()
    try: inpt = sys.stdin.readline()
    except: break;
    if not inpt: continue
    inpt = clean(inpt)
    grm = gramify_me_captain(inpt)
    query(grm,inpt)
  sys.stdout.flush()
