#!/usr/bin/env python


import sys
import json

n = 3
index = {}
stor = {}
check = []

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
    for i in xrange(1,n+1):
      for j in xrange(0, len(word)-i+1):
        grams.append( word[j:j+i] )
  return grams

def add_to_index(_id, grams):
  stor[len(stor)] = _id
  for gram in grams:
    if gram not in index:
      index[gram] = []
    if (len(stor)-1) not in index:
      index[gram].append(len(stor)-1)

def query(inpt,q):
  if inpt[0] in index:
    results = set(index[inpt[0]])
  else:
    sys.stdout.write(json.dump([]))
    return
  for wd in inpt:
    if wd in index:
      results = results.intersection(set(index[wd]))
  rem = set()
  for r in results:
    for w in q.split():
      if w not in check[r]:
        rem.add(r)
  results = results.difference(rem)
  res = []
  for i in results:
    res.append(stor[i])
  sys.stdout.write( json.dumps(res) )

if __name__ == '__main__':
  fs = sys.argv[1]

  f = open(fs,'r')

  for line in f:
    spl = line.split(':')
    _id = spl[0].strip()
    text = ' '.join(spl[1:])
    check.append(clean(text))
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
