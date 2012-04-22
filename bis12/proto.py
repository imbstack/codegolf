#!/usr/bin/env python


import sys
import json
import heapq
from operator import itemgetter
import cProfile

min_n = 3
max_n = 3
tune_freq = 2000
tune_part = 0.98
index = {}
stor = {}
check = {}
freq = {}
lkup = {}

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

def gramify_me_captain(line,wc):
  line = clean(line)
  spl = line.split()
  grams = set()
  for word in spl:
    for i in xrange(min_n-1,max_n+1):
      for j in xrange(0, len(word)-i):
        wd =  word[j:j+i+1]
        if wd not in lkup:
          lkup[wd] = wc
          wc += 1
        grams.add( lkup[wd] )
  return grams

def add_to_index(_id, grams, tid):
  stor[tid] = _id
  for gram in grams:
    if gram not in index:
      freq[gram] = 0
      index[gram] = set()
    else:
      freq[gram] += 1
    if tid not in index[gram]:
      #if str(type(index[gram])) == "<type 'list'>":
      #  index[gram] = set(index[gram])
      index[gram].add(tid)

def query(inpt,q):
  try:
    first = inpt.pop()
  except:
    return
  if first in index:
    results = set(index[first])
  else:
    r = []
    sys.stdout.write( json.dumps(r) )
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

def compact():
  tab = heapq.nsmallest(int(tune_part*len(freq)),freq.iteritems(), key=itemgetter(1))
  for pair in tab:
    if str(type(index[pair[0]])) != "<type 'list'>":
      index[pair[0]] = list(index[pair[0]])

if __name__ == '__main__':
  fs = sys.argv[1]

  f = open(fs,'r')

  i = 0
  j = 0
  for line in f:
    i+=1
    spl = line.split(':')
    _id = spl[0].strip()
    text = ' '.join(spl[1:])
    check[i] = clean(text)
    grams = gramify_me_captain(text,j)
    add_to_index(_id,grams,i)
    if i%1000 == 0:
      sys.stderr.write('\nAdded %d documents to index'%(i,))
    #if i%tune_freq == 0:
    #  compact()

  while True:
    sys.stdout.write('> '); sys.stdout.flush()
    try: inpt = sys.stdin.readline()
    except: break;
    if not inpt: continue
    inpt = clean(inpt)
    grm = gramify_me_captain(inpt,j)
    query(grm,inpt)
  sys.stdout.flush()


