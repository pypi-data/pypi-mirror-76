from enum import Enum


# 接收服务器下发指令之后处理的逻辑，根据指令的action判断做什么操作
# {"message_id":"2020092120","at":"2020-07-23 13:34:45","action":1,"data":{"did":"121201"}}
class Action(Enum):
    # 更新数据库
    UPDATEDB = 1
    # 更新配置
    UPDATECONFIG = 2
    # 上传数据
    UPLOADDATA = 3
    # 停止服务
    STOPSERVICE = 4
    # 开启服务
    STARTSERVICE = 5
    