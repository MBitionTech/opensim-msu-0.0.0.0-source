import os
import sys

def constant(f):
    def fset(self, value):
        raise TypeError
    def fget(self):
        return f()
    return property(fget, fset)

####################################
# Constants
####################################
class _Const(object):
    @constant
    def TAB():
        return "    "  # Four spaces
    @constant
    def NL():
        return "\n"

    @constant
    def LISTEN():
        return "listen"
    @constant
    def STATE_ENTRY():
        return "state_entry"
    @constant
    def STATE_EXIT():
        return "state_exit"
    @constant
    def TOUCH():
        return "touch"
    @constant
    def TOUCH_START():
        return "touch_start"
    @constant
    def TOUCH_END():
        return "touch_end"


CONST = _Const()
