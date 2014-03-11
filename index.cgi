#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()

from string import Template

t = open('templates/main.html', 'r')
main = Template(t.read())

print "Content-Type: text/html;charset=utf-8"
print
print main.substitute()

