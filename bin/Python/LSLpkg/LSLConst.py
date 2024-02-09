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
    def ATTACH():
        return "attach"
    @constant
    def AT_ROT_TARGET():
        return "at_rot_target"
    @constant
    def AT_TARGET():
        return "at_target"
    @constant
    def CHANGED():
        return "changed"
    @constant
    def COLLISION():
        return "collision"
    @constant
    def COLLISION_END():
        return "collision_end"
    @constant
    def COLLISION_START():
        return "collision_start"
    @constant
    def CONTROL():
        return "control"
    @constant
    def DATASERVER():
        return "dataserver"
    @constant
    def EMAIL():
        return "email"
    # @constant
    # def EVENT_ORDER():
    #    return "event_order"
    @constant
    def EXPERIENCE_PERMISSIONS():
        return "experience_permissions"
    @constant
    def EXPERIENCE_PERMISSIONS_DENIED():
        return "experience_permissions_denied"
    @constant
    def GAME_CONTROL():
        return "game_control"
    @constant
    def HTTP_REQUEST():
        return "http_request"
    @constant
    def HTTP_RESPONSE():
        return "http_response"
    @constant
    def LAND_COLLISION():
        return "land_collision"
    @constant
    def LAND_COLLISION_END():
        return "land_collision_end"
    @constant
    def LAND_COLLISION_START():
        return "land_collision_start"
    @constant
    def LINKSET_DATA():
        return "linkset_data"
    @constant
    def LINK_MESSAGE():
        return "link_message"
    @constant
    def LISTEN():
        return "listen"
    @constant
    def MONEY():
        return "money"
    @constant
    def MOVING_END():
        return "moving_end"
    @constant
    def MOVING_START():
        return "moving_start"
    @constant
    def NOT_AT_ROT_TARGET():
        return "not_at_rot_target"
    @constant
    def NOT_AT_TARGET():
        return "not_at_target"
    @constant
    def NO_SENSOR():
        return "no_sensor"
    @constant
    def OBJECT_REZ():
        return "object_rez"
    @constant
    def ON_REZ():
        return "on_rez"
    @constant
    def PATH_UPDATE():
        return "path_update"
    # @constant
    # def REMOTE_DATA():
    #    return "remote_data"
    @constant
    def RUN_TIME_PERMISSIONS():
        return "run_time_permissions"
    @constant
    def SENSOR():
        return "sensor"
    @constant
    def STATE_ENTRY():
        return "state_entry"
    @constant
    def STATE_EXIT():
        return "state_exit"
    @constant
    def TIMER():
        return "timer"
    @constant
    def TOUCH():
        return "touch"
    @constant
    def TOUCH_END():
        return "touch_end"
    @constant
    def TOUCH_START():
        return "touch_start"
    @constant
    def TRANSACTION_RESULT():
        return "transaction_result"


CONST = _Const()
