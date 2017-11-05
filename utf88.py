#!/usr/bin/env python
# -*- coding: utf-8 -*-
def whatisthis(s):
    if isinstance(s, str):
        print "ordinary string"
    elif isinstance(s, unicode):
        print "unicode string"
    else:
        print "not a string"


whatisthis(u"015fekilde")
s = u"015fekilde"
if isinstance(s, str):
    print 's is a string object'
elif isinstance(s, unicode):
    print 's is a unicode object'