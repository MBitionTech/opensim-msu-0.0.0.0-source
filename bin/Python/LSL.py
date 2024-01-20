########################################################################
# FILE NAME:      LSL.py
# 
# VERSION:        1.0
# 
# AUTHOR:         Dr. Mel Bayne
# 
# Date            Description
# --------        ---------------------------------------------------
# 01192024        The purpose of this class is to provide a mechanism
#                 for using Python to dynamically generate LSL structured
#                 code inside OpenSimulator.
#
# LSL (Linden Scripting Language) is the scripting language that gives
# behavior to Second Life primitives, objects, and avatars. For the 39
# LSL events defined below, a "LSL script" can be generated following
# its basic structure defined here; https://wiki.secondlife.com/wiki/State
# 
# For example;
# default
# {
#     state_entry()
#     {
#         llSay(0,
#             "You either just saved the script after editing it"
#             + "\nand/or the script (re)entered the default state.");
#
#         // white and opaque text
#         llSetText("Click to change states", <1.0, 1.0, 1.0>, (float)TRUE);
#     }
#
#     touch_end(integer num_detected)
#     {
#         // Note: NEVER do a state change from within a touch_start event -
#         // - that can lead to the next touch_start on return to this state to be missed.
#         // Here we do the state change safely, from within touch_end
#         state two;
#     }
#
#     state_exit()
#     {
#         llSay(0, "The script leaves the default state.");
#     }
# }
#
# state two
# {
#     state_entry()
#     {
#         llSay(0, "The script entered state 'two'");
#         state default;
#     }
#
#     state_exit()
#     {
#         llSay(0, "The script leaves state 'two'");
#     }
# }
#
########################################################################
# Typical Python usage inside OpenSimulator would be similar to this;
# (Note: The generated LSL script is not intended to be functional)
#
# //py
# import os
# import sys
# import clr
# import inspect
# import Python.LSL as LSL
# clr.AddReference("OpenSim.Region.ScriptEngine.Shared.CodeTools")
# from SecondLife import LSLUtilities
#
# # Instantiate the SecondLife.LSLUtilities class
# utils = LSLUtilities()
# utils.lsl_log("******************** Success FOR PYTHON.NET ********************\\n")
#
# # Instantiate the LSLEvents class
# script = ""
# lsl = LSL.LSLEvents("default")
# script, args = lsl.state_entry(script)
# script = lsl.state_entry_event_should_contain(script, "llSay(0, __dquote__Script Running!__dquote__);\n")
#
# script, args = lsl.timer(script)
#
# script, func_name = lsl.add_function(script, "ShowAbsolute", [["integer inputInteger"], ["string inputStr"]])
# script = lsl.function_should_contain(func_name, script, "string output = __dquote__llAbs()__dquote__ + \
# (string)inputInteger + __dquote__) --> __dquote__ + (string)llAbs(inputInteger);\n")
#
# script = lsl.function_add_newline(func_name, script)
# script = lsl.function_should_contain(func_name, script, "llSay(PUBLIC_CHANNEL, output);\n")
# script = lsl.timer_event_should_contain(script, "llSay(PUBLIC_CHANNEL, __dquote__The absolute value of -4 is: __dquote__ + (string)llAbs(-4) );\n");
# script, args = lsl.state_exit(script)
#
# lsl2 = LSL.LSLEvents("two")
# script, args = lsl2.state_entry(script)
# script = lsl2.state_entry_event_should_contain(script, "llSay(0, __dquote__How are ya?__dquote__);\n")
#
# script, args = lsl2.touch_start(script, "num_detected")
#
# script, args = lsl2.listen(script, "channel", "name", "_id", "message")
#
# script, args = lsl2.state_exit(script)
# utils.lsl_log("\n" + script)
#
# # The writeToFile() C# utility function is defined to write the "script"
# # to a file.  It will convert 3 special keywords as appropriate before
# # generating the file.  They are;
# # Replace("__obrace__", "{");
# # Replace("__cbrace__", "}");
# # Replace("__dquote__", "\"");
# utils.writeToFile("{0}", script)
#
########################################################################
import os
import sys
import inspect

########################################################################
# Note: In Python, methods and functions have similar purposes but
# differ in important ways. Functions are independent blocks of code
# that can be called from anywhere, while methods are tied to objects
# or classes and need an object or class instance to be invoked.
########################################################################

####################################
# Constants
####################################
TAB = "    "  # Four spaces

####################################
# Function
####################################
def write_to_file(fullPathToSrcFileName, content_to_write):
    # Open the file in write mode ('w')
    # If the file doesn't exist, it will be created. If it does exist, its contents will be overwritten.
    with open(fullPathToSrcFileName, 'w') as file:
        # Write the string to the file
        file.write(content_to_write)

########################################################################
# LSL Events class
# According to https://wiki.secondlife.com/wiki/Category:LSL_Events
# there are 39 of 41 possible events defined.
#
# NOTE:
# Event Order - not actually an event.  Instead, it defines which events
# are called for different actions and the order in which they are
# called.
#
# Remote data - remote_data( integer event_type, key channel,
#                            key message_id, string sender,
#                            integer idata, string sdata )
# DEPRECATED - use LSL_http_server instead
# https://wiki.secondlife.com/wiki/LSL_HTTP_server
########################################################################

class LSLEvents:
    ########################################################################
    # Define LSLEvents class - variable
    ########################################################################
    EVarray = []

    ########################################################################
    # Define LSLEvents class - private methods
    ########################################################################
    def __init__(self, stateName=""):
        if not isinstance(stateName, str):
            raise ValueError("[Error]: When instantiated, parameter must be a string")
        stateName = stateName.strip()
        if " " in stateName:
            raise ValueError("[Error]: State name must be a string with no internal spaces")
        self.stateName = stateName
        if not(self.stateName and self.stateName.strip()):
            print("WARN: State name not provided. Defaulting to 'default'.")
            self.stateName = "default"

        if self.stateName != "default":
            self.stateName = "state " + self.stateName

        self.statePrinted = False
        LSLEvents.EVarray.append([self.stateName,self.statePrinted])

    def __str__(self):
        # LSLEvents.EVarray[LSLEvents.EVarray.index([self.stateName,False])] = [self.stateName,True];
        return f"{self.stateName} {{\n}}\n\n"

    def __event_should_contain(self, event_name, contents, line=""):
        if not(line and line.strip()):
            return
        
        pos = contents.find(self.stateName)
        if pos != -1:
            pos += len(self.stateName)
            pos = contents.find(event_name,pos)
            if pos != -1:
                pos += len(event_name)
                pos = contents.find(f"{TAB}}}  // End of '{event_name}' event",pos)
                if pos != -1:
                    newcontents = contents[:pos] + f"{TAB}{TAB}" + line + contents[pos:]
                    return newcontents
                else:
                    raise Exception(f"Unable to find start of event: '{event_name}' in state: '{self.stateName}'")
            else:
                raise Exception(f"Unable to find event: '{event_name}' in state: '{self.stateName}'") 
        else:
            raise Exception(f"Unable to find state: '{self.stateName}'") 

    def __call_event(self, eventName, contents="", params=""):
        # Check to see if 'contents' is an empty string
        if not(contents and contents.strip()):
            if [self.stateName,True] in LSLEvents.EVarray:
                print(f"WARN: Event was not encapsulated in a state. Using state = {self.stateName}")
                self.statePrinted = False
                LSLEvents.EVarray[LSLEvents.EVarray.index([self.stateName,True])] = [self.stateName,self.statePrinted];

            contents = f"{TAB}{eventName}({params})\n{TAB}{{\n{TAB}}}  // End of '{eventName}' event\n\n"
            contents = self.stateName + "\n{\n" + contents + "}  // End of '" + self.stateName + "' state \n\n"
            self.statePrinted = True
            LSLEvents.EVarray[LSLEvents.EVarray.index([self.stateName,False])] = [self.stateName,self.statePrinted];
        else:
            if [self.stateName,False] in LSLEvents.EVarray:
                contents += self.stateName + "\n{\n}  // End of '" + self.stateName + "' state \n\n"
                LSLEvents.EVarray[LSLEvents.EVarray.index([self.stateName,False])] = [self.stateName,True];

            pos = contents.rfind('}')
            if pos!= -1:
                newcontents = contents[:pos] + f"{TAB}{eventName}({params})\n{TAB}{{\n{TAB}}}  // End of '{eventName}' event\n\n" + contents[pos:]
                contents = newcontents
            else:
                raise Exception("Could not find end of current state: '{}'".format(self.stateName))    

        return contents, params

    ########################################################################
    # Define LSLEvents class - public methods
    ########################################################################
    def add_function(self, contents, function_name, function_params=[]):
        # function_params is expected to be a list of lists
        final_params_list=""
        tmp_list = []
        for params_list in function_params:
            for arg_pair in params_list:
                # LSL accepts seven types of variable data: string,
                # key, integer, float, vector, rotation, or list
                tmp = arg_pair.split(' ')
                if f"{tmp[0]}" != "string" and f"{tmp[0]}" != "key" and \
                    f"{tmp[0]}" != "integer" and f"{tmp[0]}" != "float" and \
                    f"{tmp[0]}" != "vector" and f"{tmp[0]}" != "rotation" and f"{tmp[0]}" != "list":
                    raise ValueError(f"[Error]: {{{inspect.currentframe().f_code.co_name}}} - LSL accepts seven " + 
                                     "types of variable data: string, key, integer, float, vector, rotation, or list")
                
                if len(tmp) == 2:
                    tmp_list.append(f"{arg_pair}")
                else:
                    raise ValueError("An argument needs a valid LSL type and a name!")
                
        final_params_list = ", ".join(tmp_list)
                
        function_string = f"{function_name}({final_params_list})\n{{\n}}  // End of '{function_name}' function\n\n"
        contents = function_string + contents
        return contents, function_name

    def function_add_newline(self, function_name, contents):        
        pos = contents.find(function_name)
        if pos != -1:
            pos += len(function_name)
            pos = contents.find(f"}}  // End of '{function_name}' function",pos)
            if pos != -1:
                newcontents = contents[:pos] + f"\n" + contents[pos:]
                return newcontents
            else:
                raise Exception(f"Unable to find end of function: '{function_name}'")
        else:
            raise Exception(f"Unable to find function: '{function_name}'")
        
        return contents

    def function_should_contain(self, function_name, contents, line=""):
        if not(line and line.strip()):
            return
        
        pos = contents.find(function_name)
        if pos != -1:
            pos += len(function_name)
            pos = contents.find(f"}}  // End of '{function_name}' function",pos)
            if pos != -1:
                newcontents = contents[:pos] + f"{TAB}" + line + contents[pos:]
                return newcontents
            else:
                raise Exception(f"Unable to find end of function: '{function_name}'")
        else:
            raise Exception(f"Unable to find function: '{function_name}'")

        return contents

    ########################################################################
    # Define 39 LSLEvents class functions
    ########################################################################
    # Attach  - attach( key _id )
    def attach(self, contents, _id):
        eventName = inspect.currentframe().f_code.co_name
        params = f"key {_id}"
        return self.__call_event(eventName, contents, params)

    def attach_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)
    
    # At rot target - at_rot_target( integer handle, rotation targetrot, rotation ourrot )
    # A rotation is a data type that contains a set of four float vlaues.
    def at_rot_target(self, contents, handle, targetrot, ourrot):
        eventName = inspect.currentframe().f_code.co_name
        params = f"integer {handle}, rotation {targetrot}, rotation {ourrot}"
        return self.__call_event(eventName, contents, params)
    
    def at_rot_target_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # At target - at_target( integer tnum, vector targetpos, vector ourpos )
    def at_target(self, contents, tnum, targetpos, ourpos):
        eventName = inspect.currentframe().f_code.co_name
        params = f"integer {tnum}, vector {targetpos}, vector {ourpos}"
        return self.__call_event(eventName, contents, params)
   
    def at_target_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Changed - changed( integer change )
    def changed(self, contents, change):
        eventName = inspect.currentframe().f_code.co_name
        params = f"integer {change}"
        return self.__call_event(eventName, contents, params)

    def changed_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Collision - collision( integer num_detected )
    def collision(self, contents, num_detected):
        eventName = inspect.currentframe().f_code.co_name
        params = f"integer {num_detected}"
        return self.__call_event(eventName, contents, params)

    def collision_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Collision end - collision_end( integer num_detected )
    def collision_end(self, contents, num_detected):
        eventName = inspect.currentframe().f_code.co_name
        params = f"integer {num_detected}"
        return self.__call_event(eventName, contents, params)

    def collision_end_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Collision start - collision_start( integer num_detected )
    def collision_start(self, contents, num_detected):
        eventName = inspect.currentframe().f_code.co_name
        params = f"integer {num_detected}"
        return self.__call_event(eventName, contents, params)

    def collision_start_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Control - control( key i_idd, integer level, integer edge )    
    def control(self, contents, _id, level, edge):
        eventName = inspect.currentframe().f_code.co_name
        params = f"key {_id}, integer {level}, integer {edge}"
        return self.__call_event(eventName, contents, params)

    def control_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Dataserver - dataserver( key queryid, string data )
    def dataserver(self, contents, queryid, data):
        eventName = inspect.currentframe().f_code.co_name
        params = f"key {queryid}, string {data}"
        return self.__call_event(eventName, contents, params)
   
    def dataserver_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Email -  email( string time, string address, string subject, string message, integer num_left )
    def email(self, contents, time, address, subject, message, num_left):
        eventName = inspect.currentframe().f_code.co_name
        params = f"string {time}, string {address}, string {subject}, string {message}, integer {num_left}"
        return self.__call_event(eventName, contents, params)

    def email_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Experience permissions - experience_permissions( key agent_id )
    def experience_permissions(self, contents, agent_id):
        eventName = inspect.currentframe().f_code.co_name
        params = f"key {agent_id}"
        return self.__call_event(eventName, contents, params)

    def experience_permissions_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Experience permissions denied - experience_permissions_denied( key agent_id, integer reason )
    def experience_permissions_denied(self, contents, agent_id, reason):
        eventName = inspect.currentframe().f_code.co_name
        params = f"key {agent_id}, integer {reason}"
        return self.__call_event(eventName, contents, params)
            
    def experience_permissions_denied_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Game control - game_control( key _id, integer button_levels, integer button_edges, list axes )
    def game_control(self, contents, _id, button_levels, button_edges, axes):
        eventName = inspect.currentframe().f_code.co_name
        params = f"key {_id}, integer {button_levels}, integer {button_edges}, list {axes}"
        return self.__call_event(eventName, contents, params)
                        
    def game_control_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Http request - http_request( key request_id, string method, string body )
    def http_request(self, contents, request_id, method, body):
        eventName = inspect.currentframe().f_code.co_name
        params = f"key {request_id}, string {method}, string {body}"
        return self.__call_event(eventName, contents, params)

    def http_request_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Http response - http_response( key request_id, integer status, list metadata, string body )
    def http_response(self, contents, request_id, status, metadata, body):
        eventName = inspect.currentframe().f_code.co_name
        params = f"key {request_id}, integer {status}, list {metadata}, string {body}"
        return self.__call_event(eventName, contents, params)

    def http_response_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Land collision - land_collision( vector pos )
    def land_collision(self, contents, pos):
        eventName = inspect.currentframe().f_code.co_name
        params = f"vector {pos}"
        return self.__call_event(eventName, contents, params)
            
    def land_collision_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Land collision end - land_collision_end( vector pos )
    def land_collision_end(self, contents, pos):
        eventName = inspect.currentframe().f_code.co_name
        params = f"vector {pos}"
        return self.__call_event(eventName, contents, params)

    def land_collision_end_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Land collision start - land_collision_start( vector pos )
    def land_collision_start(self, contents, pos):
        eventName = inspect.currentframe().f_code.co_name
        params = f"vector {pos}"
        return self.__call_event(eventName, contents, params)

    def land_collision_start_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Linkset data - linkset_data( integer action, string name, string value )
    def linkset_data(self, contents, action, name, value):
        eventName = inspect.currentframe().f_code.co_name
        params = f"integer {action}, string {name}, string {value}"
        return self.__call_event(eventName, contents, params)

    def linkset_data_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Link message - link_message( integer sender_num, integer num, string aString, key _id )
    def link_message(self, contents, sender_num, num, aString, _id):
        eventName = inspect.currentframe().f_code.co_name
        params = f"integer {sender_num}, integer {num}, string {aString}, key {_id}"
        return self.__call_event(eventName, contents, params)

    def link_message_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Listen - listen( integer channel, string name, key _id, string message )
    def listen(self, contents, channel, name, _id, message):
        eventName = inspect.currentframe().f_code.co_name
        params = f"integer {channel}, string {name}, key {_id}, string {message}"
        return self.__call_event(eventName, contents, params)

    def listen_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Money - money( key _id, integer amount )
    def money(self, contents, _id, amount):
        eventName = inspect.currentframe().f_code.co_name
        params = f"key {_id}, integer {amount}"
        return self.__call_event(eventName, contents, params)

    def money_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Moving end - moving_end( )
    def moving_end(self, contents):
        eventName = inspect.currentframe().f_code.co_name
        return self.__call_event(eventName, contents)
    
    def moving_end_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Moving start - moving_start( )
    def moving_start(self, contents):
        eventName = inspect.currentframe().f_code.co_name
        return self.__call_event(eventName, contents)

    def moving_start_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Not at rot target - not_at_rot_target( )
    def not_at_rot_target(self, contents):
        eventName = inspect.currentframe().f_code.co_name
        return self.__call_event(eventName, contents)

    def not_at_rot_target_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Not at target - not_at_target( )
    def not_at_target(self, contents):
        eventName = inspect.currentframe().f_code.co_name
        return self.__call_event(eventName, contents)

    def not_at_target_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # No sensor - no_sensor( )
    def no_sensor(self, contents):
        eventName = inspect.currentframe().f_code.co_name
        return self.__call_event(eventName, contents)

    def no_sensor_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Object rez - object_rez( key _id )
    def object_rez(self, contents, _id):
        eventName = inspect.currentframe().f_code.co_name
        params = f"key {_id}"
        return self.__call_event(eventName, contents, params)

    def object_rez_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # On rez - on_rez( integer start_param )
    def on_rez(self, contents, start_param):
        eventName = inspect.currentframe().f_code.co_name
        params = f"integer {start_param}"
        return self.__call_event(eventName, contents, params)

    def on_rez_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Path update - path_update( integer _type, list reserved )
    def path_update(self, contents, _type, reserved):
        eventName = inspect.currentframe().f_code.co_name
        params = f"integer {_type}, list {reserved}"
        return self.__call_event(eventName, contents, params)

    def path_update_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Run time permissions - run_time_permissions( integer perm )
    def run_time_permissions(self, contents, perm):
        eventName = inspect.currentframe().f_code.co_name
        params = f"integer {perm}"
        return self.__call_event(eventName, contents, params)

    def run_time_permissions_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Sensor - sensor( integer num_detected )
    def sensor(self, contents, num_detected):
        eventName = inspect.currentframe().f_code.co_name
        params = f"integer {num_detected}"
        return self.__call_event(eventName, contents, params)

    def sensor_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # State entry - state_entry( )
    def state_entry(self, contents):
        eventName = inspect.currentframe().f_code.co_name
        return self.__call_event(eventName, contents)

    def state_entry_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # State exit - state_exit( )
    def state_exit(self, contents):
        eventName = inspect.currentframe().f_code.co_name
        return self.__call_event(eventName, contents)

    def state_exit_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Timer - timer( )
    def timer(self, contents):
        eventName = inspect.currentframe().f_code.co_name
        return self.__call_event(eventName, contents)

    def timer_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Transaction result - transaction_result( key _id, integer success, string data )
    def transaction_result(self, contents, _id, success, data):
        eventName = inspect.currentframe().f_code.co_name
        params = f"key {_id}, integer {success}, string {data}"
        return self.__call_event(eventName, contents, params)

    def transaction_result_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Touch - touch( integer num_detected )
    def touch(self, contents, num_detected):
        eventName = inspect.currentframe().f_code.co_name
        params = f"integer {num_detected}"
        return self.__call_event(eventName, contents, params)
        
    def touch_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Touch end - touch_end( integer num_detected )
    def touch_end(self, contents, num_detected):
        eventName = inspect.currentframe().f_code.co_name
        params = f"integer {num_detected}"
        return self.__call_event(eventName, contents, params)
            
    def touch_end_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)

    # Touch start - touch_start( integer num_detected )
    def touch_start(self, contents, num_detected):
        eventName = inspect.currentframe().f_code.co_name
        params = f"integer {num_detected}"
        return self.__call_event(eventName, contents, params)
    
    def touch_start_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)
    
    # Listen - listen( integer channel, string name, key _id, string message )
    def listen(self, contents, channel, name, _id, message):
        eventName = inspect.currentframe().f_code.co_name
        params = f"integer {channel}, string {name}, key {_id}, string {message}"
        return self.__call_event(eventName, contents, params)
    
    def listen_event_should_contain(self, contents, line=""):
        event = inspect.currentframe().f_code.co_name.removesuffix("_event_should_contain").strip()
        return self.__event_should_contain(event, contents, line)
