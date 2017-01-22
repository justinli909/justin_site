#!/usr/bin/python
#
from ops1.tasks import test1,test2

str1 = "test1"
test1.delay(str1)
str2 = "test2"
test2.delay(str2)
