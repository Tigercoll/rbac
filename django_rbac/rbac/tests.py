from django.test import TestCase

# Create your tests here.


class Per(object):
    def __init__(self,a):
        self.a=a

    def add(self):
        return "add" in self.a


per = Per(['add','delete'])
b = per.add
print(b)