#!/usr/bin/env python3
import os
import sys
import clr
import inspect
from Python.LSLpkg.LSLEvents import Events, getScript, setScript, resetScript
from Python.LSLpkg.LSLFunc import Func, key, rotation, vector
from Python.LSLpkg.LSLConst import CONST

clr.AddReference("OpenSim.Region.ScriptEngine.Shared.CodeTools")
from SecondLife import LSLUtilities
clr.AddReference("OpenSim.Region.ScriptEngine.Shared.Api.Runtime")
from OpenSim.Region.ScriptEngine.Shared.ScriptBase import ScriptBaseClass

def main():
    # Get current working directory
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    print("Hello World!")
    print("cur_dir = ", cur_dir.replace("\\","\\\\")  )
    print("\n")
    
    utils = LSLUtilities()
    utils.lsl_log("******************** Touching an object ********************")

    resetScript()
    default = Events("default")
    default.state_entry()
    default.listen("channel", "name", "_id", "message")
    default.state_exit()
    
    funcs = Func(default, CONST.STATE_ENTRY)
    funcs.pySay(ScriptBaseClass.PUBLIC_CHANNEL, "Script Running!")
    funcs.pySay(ScriptBaseClass.PUBLIC_CHANNEL, "Just another llSay() statement!!")
    k=key("")
    funcs.pyListen(-9, "", k, "")

    colors = {}
    colors["red"]="<1,0,0>"
    colors["orange"]="<1,0.5,0>"
    colors["yelow"]="<1,1,0>"
    colors["lime"]="<0.5,1,0>"
    colors["green"]="<0,1,0>"
    colors["teal"]="<0,1,0.5>"
    colors["cyan"]="<0,1,1>"
    colors["skyblue"]="<0,0.5,1>"
    colors["blue"]="<0,0,1>"
    colors["purple"]="<0.5,0,1>"
    colors["magenta"]="<1,0,1>"
    colors["pink"]="<1,0,0.5>"
    colors["white"]="<1,1,1>"
    colors["random"]="<r,g,b>"
    nl='\n'
    fStr=""
    cnt=0
    for x,y in colors.items():
        adjust=""
        if cnt!=0:
            adjust=f"{CONST.TAB}{CONST.TAB}"

        extra=""
        if x == "random":
            extra=f"{CONST.TAB}{CONST.TAB}{CONST.TAB}float r = llFrand(1);{nl}"
            extra+=f"{CONST.TAB}{CONST.TAB}{CONST.TAB}float g = llFrand(1);{nl}"
            extra+=f"{CONST.TAB}{CONST.TAB}{CONST.TAB}float b = llFrand(1);{nl}"

        lStr = f"{adjust}if (message == __dquote__{x}__dquote__){nl}{CONST.TAB}{CONST.TAB}__obrace__{nl}{extra}{CONST.TAB}{CONST.TAB}{CONST.TAB}llSetColor({y}, ALL_SIDES);{nl}{CONST.TAB}{CONST.TAB}__cbrace__{nl}"
        fStr += lStr

        cnt += 1
        if cnt < len(colors):
            fStr += f"{CONST.TAB}{CONST.TAB}else{nl}"
        else:
            fStr += f"{CONST.TAB}{CONST.TAB}else{nl}"
            fStr += f"{CONST.TAB}{CONST.TAB}__obrace__{nl}{CONST.TAB}{CONST.TAB}{CONST.TAB}llSetColor(message, ALL_SIDES);{nl}{CONST.TAB}{CONST.TAB}__cbrace__{nl}"

    funcs2 = Func(default, CONST.LISTEN)
    funcs2.pyMisc(fStr)
    vvv = "<0.5,1,0.5>"
    v=vector(vvv)
    funcs2.pySetColor(v,ScriptBaseClass.ALL_SIDES)


    from io import StringIO
    import sys
    tmp=sys.stdout
    my_result=StringIO()
    sys.stdout=my_result
    print(f"{getScript()}")
    strOutput=my_result.getvalue()
    sys.stdout=tmp

    strOutput = strOutput.replace("__obrace__", "{");
    strOutput = strOutput.replace("__cbrace__", "}");
    strOutput = strOutput.replace("__dquote__", "\"");
    print(f"final script = \n{strOutput}\n")


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
