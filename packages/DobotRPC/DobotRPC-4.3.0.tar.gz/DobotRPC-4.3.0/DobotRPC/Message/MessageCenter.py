# python3
# -*- encoding: utf-8 -*-
"""
@Author:
    JoMar Wu (sos901012@gmail.com)
@Create Time:
    2019-08-28 18:08:55
@License:
    Copyright © 2019 Shenzhen Yuejiang Co., Ltd.
@Desc:
    None
"""
from typing import Any, Tuple, Dict
from . import MessageCenterError


class MessageCenter(object):
    def __init__(self):
        # {"module_name": module_obj}
        self.__module_map = {}

    def __del__(self):
        self.__module_map.clear()

    def register(self, module_name: str, module: object) -> None:
        """
        @Create Time:
            2019-09-04 15:58:51
        @Desc:
            1. 注册模块到消息中心
            2. 模块对象挂在MC的对象树中
        @param {module_name: str}:
            模块名字
        @param {module: object}:
            模块对象
        @return {}:
            None
        """
        if not isinstance(module, object):
            raise MessageCenterError.IsNotMessageHandler(module)

        self.__module_map[module_name] = module
        # module.setParent(self)

    def remove(self, name: str) -> object:
        """
        @Create Time:
            2019-09-04 15:58:51
        @Desc:
            1. 从消息中心删除模块对象
            2. 从MC的对象树中删除模块对象
        @param {module_name: str}:
            模块名字
        @param {module: object}:
            模块对象
        @return {}:
            None
        """
        module = self.__module_map.pop(name, None)
        if module:
            del module

    def __method_parser(self, method: str) -> (object, str):
        """
        @Create Time:
            2019-09-04 16:04:05
        @Desc:
            解析method字符串
        @param {method: str}:
            method字符串
        @return {(object, str)}:
            module, func_name
        """
        temp = method.split(".")
        if len(temp) == 3:
            # GUI发出的消息格式：target.obj.func
            target = temp[0]
            module_name = temp[1]
            func_name = temp[2]
        elif len(temp) == 2:
            # 内部发出的消息格式：obj.func
            target = "vm"
            module_name = temp[0]
            func_name = temp[1]
        else:
            raise MessageCenterError.InvalidMethodFormat(method)

        if target == "vm":
            module = self.__module_map.get(module_name, None)
        elif target == "dobotlink":
            # TODO: 优化dobotlink的解释
            dobotlink = self.__module_map.get("dobotlink", None)
            module = eval(f"dobotlink.{module_name}", {"dobotlink": dobotlink})
        else:
            raise MessageCenterError.InvalidMethodFormat(method)

        if module is None:
            raise MessageCenterError.CannotFoundModule(module_name)

        return module, func_name

    async def call(self, method: str, *args: Tuple[Any],
                   **kwargs: Dict[str, Any]) -> None:
        """
        @Create Time:
            2019-09-04 13:33:06
        @Desc:
            1. 解析method，确定转发对象和其对应的Slot
            2. 通过原对象系统，异步调用目标对象的Slot
        @param {method: Any}:
            想调用的方法字符串
            支持两种格式：
            1. target.obj.func 如dobotlink.Magician.SetPTPCmd
            2. obj.func playback.start
        @param {args: List[Any]}:
            传入的参数列表
        @return {}:
            None
        """

        module, func_name = self.__method_parser(method)
        func = eval(f"module.{func_name}", {"module": module})
        return await func(*args, **kwargs)

    def __getattr__(self, module_name: str) -> Any:
        """
        @Create Time:
            2019-09-04 13:50:34
        @Desc:
            1. 获取模块对象
            2. 调用方法形如 mc.dobotlink
        @param {module_name: str}:
            模块对象名字
        @return {}:
            模块对象
        """
        module = self.__module_map.get(module_name, None)
        if module is None:
            raise MessageCenterError.CannotFoundModule(module_name)

        return module
