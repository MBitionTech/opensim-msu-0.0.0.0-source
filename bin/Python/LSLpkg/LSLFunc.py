import os
import sys
import re
import inspect
from .LSLEvents import Events, setScript
from .LSLConst import CONST

class key:
    def __init__(self, uuid):
        if not isinstance(uuid, str):
            raise ValueError("Value should be in the form of a string")

        # Note: key can also be an empty string
        p = re.compile('[a-zA-Z\d]{8}-[a-zA-Z\d]{4}-[a-zA-Z\d]{4}-[a-zA-Z\d]{4}-[a-zA-Z\d]{12}|^$')
        if p.match(uuid) is None:        
            raise ValueError("UUID value is not formatted correctly")

        self.uuid = uuid

    def __str__(self):
        return f"{self.uuid}"


class rotation:
    def __init__(self, rotation):
    
        if not isinstance(rotation, str):
            raise ValueError("[Error]: {{{}}} should be in the form of a string (i.e. <0.1,0.2,0.3,0.4>)".format(inspect.currentframe().f_code.co_name))
            
        p = re.compile('\<\s*([+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)\s*,\s*){3}\s*[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)\s*\>')
        if p.match(rotation) is None:
            raise ValueError("{{{}}} value is not formatted correctly".format(inspect.currentframe().f_code.co_name))

        q = re.compile('\<(.+)\>')
        m = q.match(rotation)
        
        rot_list = []
        if m is None:
            raise ValueError("{{{}}} values are not floats".format(inspect.currentframe().f_code.co_name))
        else:
            rot_list = m.group(1).split(",")         # This is a list of strings
            rot_list = [float(i) for i in rot_list]  # This is a list of floats
            for r in rot_list:
              if not isinstance(r, float):
                raise ValueError("[Error]: {{{}}} - all parameters must be float".format(inspect.currentframe().f_code.co_name))
            if len(rot_list) != 4:
                raise ValueError("[Error]: {{{}}} - type requires 4 float parameters".format(inspect.currentframe().f_code.co_name))
                
        self.listRotation = rot_list

    def __str__(self):
        return f"<{self.listRotation[0]},{self.listRotation[1]},{self.listRotation[2]},{self.listRotation[3]}>"


class vector:
    def __init__(self, vector):
    
        if not isinstance(vector, str):
            raise ValueError("[Error]: {{{}}} should be in the form of a string (i.e. <0.1,0.2,0.3>)".format(inspect.currentframe().f_code.co_name))
            
        p = re.compile('\<\s*([+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)\s*,\s*){2}\s*[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)\s*\>')
        if p.match(vector) is None:
            raise ValueError("{{{}}} value is not formatted correctly".format(inspect.currentframe().f_code.co_name))

        q = re.compile('\<(.+)\>')
        m = q.match(vector)
        
        vec_list = []
        if m is None:
            raise ValueError("{{{}}} values are not floats".format(inspect.currentframe().f_code.co_name))
        else:
            vec_list = m.group(1).split(",")         # This is a list of strings
            vec_list = [float(i) for i in vec_list]  # This is a list of floats
            for v in vec_list:
              if not isinstance(v, float):
                raise ValueError("[Error]: {{{}}} - all parameters must be float".format(inspect.currentframe().f_code.co_name))
            if len(vec_list) != 3:
                raise ValueError("[Error]: {{{}}} - type requires 3 float parameters".format(inspect.currentframe().f_code.co_name))

        self.listVector = vec_list

    def __str__(self):
        return f"<{self.listVector[0]},{self.listVector[1]},{self.listVector[2]}>"


class Func:
    def __init__(self, lsl, eventName):
        if not isinstance(lsl, Events):
            raise ValueError("[Error]: {{{}}} - 'lsl' parameter must be an LSLEvents object".format(inspect.currentframe().f_code.co_name))
        
        self.object  = lsl
        self.eventName = eventName

    ##################################################################################################
    # llFunctions have been converted to pyFunctions here;
    # They are explained here; https://wiki.secondlife.com/wiki/Category:LSL_Functions
    #
    # If function returns void, then no 'embed' is necessary
    # If function return non-void, then add 'embed' option.  This will allow the user to 'embed' the
    # function as part of a longer Python line.  This means it will not have a semicolon at the end
    # of its printed result.
    ##################################################################################################

    # integer llListen( integer channel, string name, key id, string msg );
    def pyListen(self, channel, name, _id, message, embed=False):
        if not isinstance(channel, int):
            raise ValueError("[Error]: {{{}}} - 'channel' parameter must be an integer".format(inspect.currentframe().f_code.co_name))

        if not isinstance(name, str):
            raise ValueError("[Error]: {{{}}} - 'name' parameter must be a string".format(inspect.currentframe().f_code.co_name))

        if not isinstance(_id, key):
            raise ValueError("[Error]: {{{}}} - '_id' parameter must be a key".format(inspect.currentframe().f_code.co_name))

        if not isinstance(message, str):
            raise ValueError("[Error]: {{{}}} - 'message' parameter must be a string".format(inspect.currentframe().f_code.co_name))

        if not isinstance(embed, bool):
            raise ValueError("[Error]: {{{}}} - 'message' parameter must be a string".format(inspect.currentframe().f_code.co_name))

        ll = "llListen"
        line = f"{ll}({channel}, __dquote__{name}__dquote__, __dquote__{_id}__dquote__, __dquote__{message}__dquote__)"
        if embed is False:
            line += ";\n"

        contents = self.object._event_should_contain(self.eventName, line)

        setScript(contents)
        return contents

    # llSay( integer channel, string msg );
    def pySay(self, channel, message=""):
        if not isinstance(channel, int):
            raise ValueError("[Error]: {{{}}} - 'channel' parameter must be an integer".format(inspect.currentframe().f_code.co_name))

        if not isinstance(message, str):
            raise ValueError("[Error]: {{{}}} - 'message' parameter must be a string".format(inspect.currentframe().f_code.co_name))

        ll = "llSay"
        line = f"{ll}({channel}, __dquote__{message}__dquote__);\n"

        contents = self.object._event_should_contain(self.eventName, line)

        setScript(contents)
        return contents

    # llSetColor( vector color, integer face );
    def pySetColor(self, color, face):
        if not isinstance(color, vector):
            raise ValueError("[Error]: {{{}}} - 'color' parameter must be a vector".format(inspect.currentframe().f_code.co_name))

        if not isinstance(face, int):
            raise ValueError("[Error]: {{{}}} - 'face' parameter must be an integer".format(inspect.currentframe().f_code.co_name))

        ll = "llSetColor"
        line = f"{ll}({color}, {face});\n"

        contents = self.object._event_should_contain(self.eventName, line)

        setScript(contents)
        return contents







    # This is here as a placeholder function until all 500 functions are written in Python
    def pyMisc(self, whatever):
        line = f"{whatever}"

        contents = self.object._event_should_contain(self.eventName, line)

        setScript(contents)
        return contents
    
