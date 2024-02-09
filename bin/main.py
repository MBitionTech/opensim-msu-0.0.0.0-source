#!/usr/bin/env python3
from io import StringIO
import os
import sys
sys.path.append(os.getcwd())  # Required for successful import below
import traceback
import inspect
import clr
clr.AddReference("OpenSim.Region.ScriptEngine.Shared.CodeTools")
from SecondLife import LSLUtilities
clr.AddReference("OpenSim.Region.ScriptEngine.Shared.Api.Runtime")
from OpenSim.Region.ScriptEngine.Shared.ScriptBase import ScriptBaseClass
from Python.LSLpkg.LSLEvents import Events, getScript, resetScript
from Python.LSLpkg.LSLFunc import Func, key, rotation, vector
from Python.LSLpkg.LSLConst import CONST

try:
    utils = LSLUtilities()
    utils.lsl_log("******************** Color changing object ********************")

    # Instantiate the LSLEvents class
    resetScript()
    default = Events("default")
    default.state_entry()
    default.listen("channel", "name", "_id", "message")

    funcs = Func(default, CONST.STATE_ENTRY)
    funcs.pySay(ScriptBaseClass.PUBLIC_CHANNEL, "Color Changing Object Script Running!")
    k=key("")
    funcs.pyListen(-9, "", k, "")

    colors = {}
    colors["red"]="<1,0,0>"
    colors["orange"]="<1,0.5,0>"
    colors["yellow"]="<1,1,0>"
    colors["lime"]="<0.5,1,0>"
    colors["lime"]="<0.5,1,0>"
    colors["green"]="<0,1,0>"
    colors["teal"]="<0,1,0.5>"
    colors["cyan"]="<0,1,1>"
    colors["skyblue"]="<0,0.5,1>"
    colors["blue"]="<0,0,1>"
    colors["purple"]="<0.5,0,1>"
    colors["magenta"]="<1,0,1>"
    colors["pink"]="<1.0,0.0,0.5>"
    colors["white"]="<1,1,1>"
    colors["random"]="<r,g,b>"
    nl=CONST.NL
    tab=CONST.TAB
    fStr=""
    v="<r,g,b>"
    cnt=0
    line=""
    for x,y in colors.items():
        adjust=""
        if cnt!=0:
            adjust=f"{tab}{tab}"

        extra=""
        if x == "random":
            extra =f"{tab}{tab}{tab}float r = llFrand(1.0);{nl}"
            extra+=f"{tab}{tab}{tab}float g = llFrand(1.0);{nl}"
            extra+=f"{tab}{tab}{tab}float b = llFrand(1.0);{nl}"
            extra+=f"{tab}{tab}{tab}llSay(PUBLIC_CHANNEL,__dquote__llSetColor(<__dquote__ + (string) r + __dquote__, __dquote__ + (string) g + __dquote__, __dquote__ + (string) b + __dquote__>, ALL_SIDES);__dquote__);{nl}"
            line = f"llSetColor({y}, ALL_SIDES);{nl}"
        else:
            v=vector(y)
            line = f"llSetColor({v}, ALL_SIDES);{nl}"

        lStr = f"{adjust}if (message == __dquote__{x}__dquote__){nl}{tab}{tab}__obrace__{nl}{extra}{tab}{tab}{tab}{line}{nl}{tab}{tab}__cbrace__{nl}"
        fStr += lStr

        cnt += 1
        if cnt < len(colors):
            fStr += f"{tab}{tab}else{nl}"
        else:
            fStr += f"{tab}{tab}else{nl}"
            fStr += f"{tab}{tab}__obrace__{nl}{tab}{tab}{tab}llSetColor(message, ALL_SIDES);{nl}{tab}{tab}__cbrace__{nl}"

    funcs2 = Func(default, CONST.LISTEN)
    funcs2.pyMisc(fStr)


    tmp1234567890=sys.stdout
    stdout_result=StringIO()
    sys.stdout=stdout_result
    print(f"{getScript()}")
    internallyGrabLSLScript=stdout_result.getvalue()
    sys.stdout=tmp1234567890
except Exception:
    tmp9876543210=sys.stdout
    stderr_result=StringIO()
    sys.stdout=stderr_result
    print(f"Traceback Error: {traceback.format_exc()}")
    internallyGrabErrOutput=stderr_result.getvalue()
    sys.stdout=tmp9876543210

# Print LSL script
print(f"{getScript()}")