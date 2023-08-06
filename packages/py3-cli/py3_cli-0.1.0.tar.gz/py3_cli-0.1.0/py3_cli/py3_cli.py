import datetime
import time
import os
import re

from termcolor import colored


class CLI:
    def __init__(self) -> None:
        self.__printlog: bool = False
        self.__time: bool = False
        self.__full_log: bool = False
        self.path: str = ''

        self.__worked_cmd: str = ''
        self.__last_cmd: str = ''

        self.__builtins = globals()["__builtins__"]
        self.__builtin_print = self.__builtins["print"]

        self.__flags: dict = {'await': {'cmd': '--await:<int>',
                                        'args': ([('int')]),
                                        'doc': 'Set the waiting time before starting'
                                        }}
        self.__colors: list = ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
        self.__dict_case: dict = {}
        self.__dict_cmd: dict = {}
        self.__case_dict_cmd_: dict = {
            'case create': {'display': {
                'doc_func': self.__case_create.__doc__,
                'cmd_func': 'case create <name:str>',
                'args_func': ([('name', 'str')]),
                'color': 'magenta',
                'prefix': 'CASE'},
                'handler': {
                    'func': self.__case_create,
                    're': 'case create \\w+',
                    'args_position': [2]
                }},
            'case run': {'display': {
                'doc_func': self.__case_run.__doc__,
                'cmd_func': 'case run <name:str>',
                'args_func': ([('name', 'str')]),
                'color': 'magenta',
                'prefix': 'CASE'},
                'handler': {
                    'func': self.__case_run,
                    're': 'case run \\w+',
                    'args_position': [2]
                }},
            'case delete': {'display': {
                'doc_func': self.__case_delete.__doc__,
                'cmd_func': 'case delete <name:str>',
                'args_func': ([('name', 'str')]),
                'color': 'magenta',
                'prefix': 'CASE'},
                'handler': {
                    'func': self.__case_delete,
                    're': 'case delete \\w+',
                    'args_position': [2]
                }},
            'case end': {'display': {
                'doc_func': 'Closes adding commands to the case',
                'cmd_func': 'case end',
                'args_func': ([(None)]),
                'color': 'magenta',
                'prefix': 'CASE'},
                'handler': {
                    'func': None,
                    're': 'case end',
                    'args_position': []
                }}}
        self.__standart_dict_cmd: dict = {
            'clear': {'display': {
                'doc_func': self.__clear.__doc__,
                'cmd_func': 'clear',
                'args_func': ([(None)]),
                'color': 'green',
                'prefix': 'INFO'},
                'handler': {
                    'func': self.__clear,
                    're': 'clear',
                    'args_position': []
                }},
            'help': {'display': {
                'doc_func': self.__help.__doc__,
                'cmd_func': 'help',
                'args_func': ([(None)]),
                'color': 'green',
                'prefix': 'HELP'},
                'handler': {
                    'func': self.__help,
                    're': 'help',
                    'args_position': []
                }},
            'flags': {'display': {
                'doc_func': self.__flag.__doc__,
                'cmd_func': 'flags',
                'args_func': ([(None)]),
                'color': 'green',
                'prefix': 'FLAG'},
                'handler': {
                    'func': self.__flag,
                    're': 'flags',
                    'args_position': []
                }},
            'quit': {'display': {
                'doc_func': self.__quit.__doc__,
                'cmd_func': 'quit',
                'args_func': ([(None)]),
                'color': 'green',
                'prefix': 'INFO'},
                'handler': {
                    'func': self.__quit,
                    're': 'quit',
                    'args_position': []
                }},
            'exit': {'display': {
                'doc_func': self.__exit.__doc__,
                'cmd_func': 'exit',
                'args_func': ([(None)]),
                'color': 'green',
                'prefix': 'INFO'},
                'handler': {
                    'func': self.__exit,
                    're': 'exit',
                    'args_position': []
                }},
            'colors': {'display': {
                'doc_func': self.__color.__doc__,
                'cmd_func': 'colors',
                'args_func': ([None]),
                'color': 'white',
                'prefix': 'COLOR'},
                'handler': {
                    'func': self.__color,
                    're': 'colors',
                    'args_position': []
                }},
            'last command': {'display': {
                'doc_func': self.__last_command.__doc__,
                'cmd_func': '<',
                'args_func': ([None]),
                'color': 'white',
                'prefix': 'INFO'},
                'handler': {
                    'func': self.__last_command,
                    're': '<',
                    'args_position': []
                }},
            'case list': {'display': {
                'doc_func': self.__case_list.__doc__,
                'cmd_func': 'case list',
                'args_func': ([None]),
                'color': 'green',
                'prefix': 'CASE'},
                'handler': {
                    'func': self.__case_list,
                    're': 'case list',
                    'args_position': []
                }}}

    def run(self, full_log: bool = False, time: bool = False, printlog: bool = False, path: str = '') -> None:
        self.__printlog = printlog
        self.__full_log = full_log
        self.__time = time
        self.path = path
        self.__Logger = Logger(self.__time, self.path)
        msg = colored('$', 'blue')

        self.__clear()
        while True:
            command = input(msg)

            if command:
                self.__handler(command)
                self.__last_cmd = command

    def cmd(self, command: str, color='white', prefix='INFO'):
        def wrapper(func):
            start = 0
            try:
                name_func = func.__name__
                doc_func = func.__doc__
                cmd_func = command
                args_func = self.__getArgs(cmd_func)
                re_ = self.__re(command)
                args_position = self.__getPosition(command)
            except AttributeError:
                raise CLIError('You can only use 1 command per 1 function')

            cmd_dict = self.__standart_dict_cmd, self.__case_dict_cmd_, self.__dict_cmd

            for cmd_dict_ in cmd_dict:
                for key in cmd_dict_:
                    if cmd_dict_[key]['handler']['re'] == re_:
                        raise CLIError(f'The command "{cmd_func}" already exists')

            self.__dict_cmd.update({name_func: {'display': {
                    'doc_func': doc_func,
                    'cmd_func': cmd_func,
                    'args_func': args_func,
                    'color': color,
                    'prefix': prefix},
                    'handler': {
                        're': re_,
                        'func': func,
                        'args_position': args_position
                    }}})
        return wrapper

    def __re(self, cmd: str) -> None:
        found__obligatory_args = re.findall('<\w+:\w+>', cmd)
        found_not_obligatory_args = re.findall('<!\w+:\w+>', cmd)

        for arg in found__obligatory_args:
            cmd = cmd.replace(arg, '\w+')

        for arg in found_not_obligatory_args:
            cmd = cmd.replace(arg, '\w+')

        return cmd

    def __getPosition(self, cmd: str) -> list:
        args_position = []
        found_args = re.findall('<\w+:\w+>', cmd)
        command = cmd.split()
        for arg in found_args:
            args_position.append(command.index(arg))

        return args_position

    def __getArgs(self, cmd: str) -> list:
        args_list = []
        found_args = re.findall('<\w+:\w+>', cmd)

        if found_args:
            for arg in found_args:
                args_list.append((re.findall('<\w+:', arg)[0][1:-1], re.findall(':\w+>', arg)[0][1:-1]))

        return args_list

    def __handler(self, command: str) -> None:
        await_ = re.findall('--await:\w+', command)
        if await_:
            print(len(await_))
            if len(await_) <= 1:
                command = command.replace(f' {await_[0]}', '').replace(f'{await_[0]} ', '')
                if await_[0][8:].isdigit():
                    await_ = int(await_[0][8:])
                else:
                    msg = 'Invalid value for await'
                    self.__Logger._warning(msg)
                    return
            else:
                msg = 'Only 1 "--await" flag can be used for the command'
                self.__Logger._warning(msg)
                return
        else:
            await_ = 0

        status_found_cmd, found_cmd, cmd = self.__found_cmd(command)

        if status_found_cmd == 0:
            msg = 'Unknown command'
            self.__Logger._warning(msg)

        elif status_found_cmd == 2:
            msg = 'Command arguments error'
            self.__Logger._warning(msg)

        elif status_found_cmd == 1:
            kwargs = {}
            if cmd[found_cmd]['display']['args_func']:
                args_list = []
                command = command.split()
                for pos in cmd[found_cmd]['handler']['args_position']:
                    args_list.append(command[pos])

                args = self.__type(args_list, cmd[found_cmd]['display']['args_func'])

                kwargs = {value[1]: value[0] for value in args}

            self.__worked_cmd = found_cmd

            if self.__full_log:
                if found_cmd in self.__dict_cmd:
                    msg = 'Command is running'
                    self.__Logger._info(msg, color=self.__Logger.full_log_color, prefix='INFO')

                if self.__printlog:
                    self.__builtins['print'] = self.__print

                    if await_ > 0:
                        msg = f'The command from the case will be launched {await_} second'
                        self.__Logger._info(msg, color=self.__Logger.full_log_color, prefix='INFO')
                        time.sleep(await_)

                    if cmd[found_cmd]['handler']['func']:
                        res_func = cmd[found_cmd]['handler']['func'](**kwargs)
                        self.__builtins["print"] = self.__builtin_print
                    else:
                        msg = 'Cannot execute in this situation'
                        self.__Logger._warning(msg)
                else:
                    if cmd[found_cmd]['handler']['func']:
                        res_func = cmd[found_cmd]['handler']['func'](**kwargs)
                    else:
                        msg = 'Cannot execute in this situation'
                        self.__Logger._warning(msg)

                if found_cmd in self.__dict_cmd:
                    msg = 'Command execution completed'
                    self.__Logger._info(msg, color=self.__Logger.full_log_color, prefix='INFO')
            else:
                if self.__printlog:
                    if cmd[found_cmd]['handler']['func']:
                        self.__builtins['print'] = self.__print
                        res_func = cmd[found_cmd]['handler']['func'](**kwargs)
                        self.__builtins["print"] = self.__builtin_print
                    else:
                        msg = 'Cannot execute in this situation'
                        self.__Logger._warning(msg)
                else:
                    if cmd[found_cmd]['handler']['func']:
                        cmd[found_cmd]['handler']['func'](**kwargs)
                    else:
                        msg = 'Cannot execute in this situation'
                        self.__Logger._warning(msg)

    def __found_cmd(self, command: str) -> tuple:
        cmd_dict = self.__standart_dict_cmd
        found_cmd = ''

        for cmd_ in cmd_dict:
            res = re.findall(cmd_dict[cmd_]['handler']['re'], command)
            if res:
                if len(command.split()) == len(res[0].split()):
                    found_cmd = cmd_
                    return 1, found_cmd, cmd_dict
            else:
                res = re.findall(cmd_dict[cmd_]['handler']['re'].replace(' \\w+', ''), command)
                if res:
                    return 2, found_cmd, cmd_dict

        cmd_dict = self.__case_dict_cmd_

        for cmd_ in cmd_dict:
            res = re.findall(cmd_dict[cmd_]['handler']['re'], command)
            if res:
                if len(command.split()) == len(res[0].split()):
                    found_cmd = cmd_
                    return 1, found_cmd, cmd_dict
            else:
                res = re.findall(cmd_dict[cmd_]['handler']['re'].replace(' \\w+', '').replace('\\w+ ', ''), command)
                if res:
                    return 2, found_cmd, cmd_dict

        cmd_dict = self.__dict_cmd

        for cmd_ in cmd_dict:
            res = re.findall(cmd_dict[cmd_]['handler']['re'], command)
            if res:
                if len(command.split()) == len(res[0].split()):
                    found_cmd = cmd_
                    return 1, found_cmd, cmd_dict
            else:
                res = re.findall(cmd_dict[cmd_]['handler']['re'].replace(' \\w+', '').replace('\\w+ ', ''), command)
                if res:
                    return 2, found_cmd, cmd_dict

        return 0, None, None

    def __found_case_cmd(self, command: str) -> tuple:
        cmd_dict = self.__standart_dict_cmd

        for cmd_ in cmd_dict:
            res = re.findall(cmd_dict[cmd_]['handler']['re'], command)

            if res:
                if len(command.split()) == len(res[0].split()):
                    return 1, command,
            else:
                res = re.findall(cmd_dict[cmd_]['handler']['re'].replace(' \\w+', ''), command)
                if res:
                    return 2, command

        cmd_dict = self.__dict_cmd

        for cmd_ in cmd_dict:
            res = re.findall(cmd_dict[cmd_]['handler']['re'], command)

            if res:
                if len(command.split()) == len(res[0].split()):
                    return 1, command
            else:
                res = re.findall(cmd_dict[cmd_]['handler']['re'].replace(' \\w+', '').replace('\\w+ ', ''), command)
                if res:
                    return 2, command

        cmd_dict = self.__case_dict_cmd_

        for cmd_ in cmd_dict:
            res = re.findall(cmd_dict[cmd_]['handler']['re'], command)

            if res:
                return 3, None
            else:
                res = re.findall(cmd_dict[cmd_]['handler']['re'].replace(' \\w+', '').replace('\\w+ ', ''), command)
                if res:
                    return 3, None

        return 0, None

    def __print(self, *args, **kwargs) -> None:
        dict_cmd = self.__dict_cmd if self.__worked_cmd in self.__dict_cmd else self.__standart_dict_cmd
        color = dict_cmd[self.__worked_cmd]['display']['color']
        prefix = dict_cmd[self.__worked_cmd]['display']['prefix']

        if self.__time:
            date = datetime.datetime.now()
            self.__builtins["print"] = self.__builtin_print
            msg = f'[{datetime.datetime.strftime(date, "%H:%M:%S")}] {prefix}: {args[0]}'
            print(colored(msg, color), **kwargs)
            self.__builtins['print'] = self.__print
        else:
            self.__builtins["print"] = self.__builtin_print
            msg = f'{prefix}: {args[0]}'
            print(colored(msg, color), **kwargs)
            self.__builtins['print'] = self.__print

        if self.path:
            self.__Logger._write_file(msg)

    def __type(self, args_list: list, args_func: list) -> list:
        args = []
        for number, arg in enumerate(args_list):
            try:
                type_ = args_func[number][1]
                arg_name = args_func[number][0]

                if type_ == 'str':
                    args.append((arg, arg_name))
                else:
                    arg_eval = eval(f'{type_}({arg})')
                    args.append((arg_eval, arg_name))
            except NameError and TypeError:
                msg = f'Argument type error'
                self.__Logger._warning(msg)

        return args

    # --- cmd ---

    def __exit(self) -> None:
        """Exit"""

        color = self.__standart_dict_cmd['exit']['display']['color']
        prefix = self.__standart_dict_cmd['exit']['display']['prefix']
        msg = f'Completion of work'
        self.__Logger._info(msg, prefix=prefix, color=color)
        exit()

    def __quit(self) -> None:
        """Quit"""

        color = self.__standart_dict_cmd['quit']['display']['color']
        prefix = self.__standart_dict_cmd['quit']['display']['prefix']
        msg = f'Completion of work'
        self.__Logger._info(msg, prefix=prefix, color=color)

        quit()

    def __clear(self) -> None:
        """Clearing the terminal"""

        os.system('cls||clear')

    def __help(self) -> None:
        """Help for commands"""

        msg = f'"function name" | cmd: "command" | args: "argument list" | doc: "documentation for the function"'
        self.__Logger._info(msg, prefix=self.__standart_dict_cmd['help']['display']['prefix'], color=self.__standart_dict_cmd['help']['display']['color'])

        for cmd in self.__standart_dict_cmd:
            msg = f'"{cmd}" | cmd: {self.__standart_dict_cmd[cmd]["display"]["cmd_func"]} | args: ({self.__standart_dict_cmd[cmd]["display"]["args_func"]}) | doc: "{self.__standart_dict_cmd[cmd]["display"]["doc_func"]}"'
            self.__Logger._info(msg, prefix=self.__standart_dict_cmd['help']['display']['prefix'], color=self.__standart_dict_cmd['help']['display']['color'])

        for cmd in self.__case_dict_cmd_:
            msg = f'"{cmd}" | cmd: {self.__case_dict_cmd_[cmd]["display"]["cmd_func"]} | args: ({self.__case_dict_cmd_[cmd]["display"]["args_func"]}) | doc: "{self.__case_dict_cmd_[cmd]["display"]["doc_func"]}"'
            self.__Logger._info(msg, prefix=self.__standart_dict_cmd['help']['display']['prefix'], color=self.__standart_dict_cmd['help']['display']['color'])

        if self.__dict_cmd:
            for cmd in self.__dict_cmd:
                msg = f'"{cmd}" | cmd: {self.__dict_cmd[cmd]["display"]["cmd_func"]} | args: ({self.__dict_cmd[cmd]["display"]["args_func"]}) | doc: "{self.__dict_cmd[cmd]["display"]["doc_func"]}"'
                self.__Logger._info(msg, prefix=self.__standart_dict_cmd['help']['display']['prefix'], color=self.__standart_dict_cmd['help']['display']['color'])

    def __color(self) -> None:
        """A list of available colors for the output"""

        for color in self.__colors:
            msg = f'name - {color}'
            self.__Logger._info(msg, prefix=self.__standart_dict_cmd['colors']['display']['prefix'], color=color)

    def __last_command(self) -> None:
        """Calling the previous command"""

        if self.__last_cmd:
            self.__handler(self.__last_cmd)
        else:
            msg = f'The previous command was not found'
            self.__Logger._warning(msg)

    def __case_create(self, name: str) -> None:
        """Creating case a command"""

        if name not in self.__dict_case:
            if self.__full_log:
                msg = f'Case successfully created'
                self.__Logger._info(msg, color=self.__Logger.full_log_color, prefix='INFO')

            msg_input = colored('$', 'magenta')
            cmd_list = []

            while True:
                command = input(msg_input)

                res = re.findall(self.__case_dict_cmd_['case end']['handler']['re'], command)

                if res:
                    await_ = re.findall('--await:\w+', command)
                    if await_:
                        if len(await_) <= 1:
                            if await_[0][8:].isdigit():
                                await_ = int(await_[0][8:])
                                time.sleep(await_ if await_ > 0 else 0)
                            else:
                                msg = 'Invalid value for await'
                                self.__Logger._warning(msg)
                                return
                        else:
                            msg = 'Only 1 "--await" flag can be used for the command'
                            self.__Logger._warning(msg)
                            break


                    if self.__full_log:
                        msg = f'Сase is close'
                        self.__Logger._info(msg, color=self.__Logger.full_log_color, prefix='INFO')

                    self.__dict_case.update({name: {'cmd_list': cmd_list}})
                    return
                else:
                    await_ = re.findall('--await:\w+', command)
                    if len(await_) <= 1:
                        if await_:
                            command = command.replace(f' {await_[0]}', '').replace(f'{await_[0]} ', '')
                            if await_[0][8:].isdigit():
                                await_ = int(await_[0][8:])
                            else:
                                msg = 'Invalid value for await'
                                self.__Logger._warning(msg)
                                return
                        else:
                            await_ = 0

                        status_found_cmd, found_cmd = self.__found_case_cmd(command)

                        if status_found_cmd == 0:
                            msg = 'Unknown command'
                            self.__Logger._warning(msg)

                        elif status_found_cmd == 2:
                            msg = 'Command arguments error'
                            self.__Logger._warning(msg)

                        elif status_found_cmd == 3:
                            msg = "You can't run case commands from the case itself"
                            self.__Logger._warning(msg)

                        elif status_found_cmd == 1:
                            cmd_list.append((found_cmd, await_ if await_ > 0 else 0))

                        if self.__full_log and status_found_cmd == 1:
                            msg = f'The command was added successfully'
                            self.__Logger._info(msg, color=self.__Logger.full_log_color, prefix='INFO')
                    else:
                        msg = 'Only 1 "--await" flag can be used for the command'
                        self.__Logger._warning(msg)
                        break

        else:
            msg = f'Case already created'
            self.__Logger._warning(msg)

    def __case_list(self) -> None:
        """Output a list of case"""

        msg = self.__dict_case if self.__dict_case else 'Case list is empty'
        self.__Logger._info(msg, prefix=self.__standart_dict_cmd['case list']['display']['prefix'], color=self.__standart_dict_cmd['case list']['display']['color'])

    def __case_run(self, name: str) -> None:
        """Starting case a command"""

        if name in self.__dict_case:
            case = self.__dict_case[name]

            if self.__full_log:
                msg = f'Case started'
                self.__Logger._info(msg, color=self.__Logger.full_log_color, prefix='INFO')

                for cmd in case['cmd_list']:
                    if self.__full_log:
                        if int(cmd[1]) > 0:
                            msg = f'The command from the case will be launched {int(cmd[1])} second'
                            self.__Logger._info(msg, color=self.__Logger.full_log_color, prefix='INFO')

                    time.sleep(int(cmd[1]))
                    self.__handler(cmd[0])

                if self.__full_log:
                    msg = f'Case completed'
                    self.__Logger._info(msg, color=self.__Logger.full_log_color, prefix='INFO')
        else:
            msg = f'Case not found'
            self.__Logger._warning(msg)

    def __case_delete(self, name) -> None:
        """Deleting a case"""

        if name in self.__dict_case:
            self.__dict_case.pop(name)

            if self.__full_log:
                msg = f'Case successfully deleted'
                self.__Logger._info(msg, color=self.__Logger.full_log_color, prefix='INFO')
        else:
            msg = f'Case not found'
            self.__Logger._warning(msg)

    def case_create(self, name: str, cmd_list: list):
        """Creating cases for running commands"""

        if self.__full_log:
            msg = f'Case successfully created'
            self.__Logger._info(msg, color=self.__Logger.full_log_color, prefix='INFO')

        self.__dict_case.update({name: {'cmd_list': cmd_list}})

    def __flag(self) -> None:
        """Flags for commands"""

        msg = f'"flag name" | cmd: "command" | args: "argument list" | doc: "documentation for the function"'
        self.__Logger._info(msg, prefix=self.__standart_dict_cmd['flags']['display']['prefix'], color=self.__standart_dict_cmd['flags']['display']['color'])

        for flag in self.__flags:
            msg = f'"{flag}" | cmd: {self.__flags[flag]["cmd"]} | args: ({self.__flags[flag]["args"]}) | doc: {self.__flags[flag]["doc"]}'
            self.__Logger._info(msg, prefix=self.__standart_dict_cmd['flags']['display']['prefix'], color=self.__standart_dict_cmd['flags']['display']['color'])


class Logger:
    def __init__(self, time: bool, path: str) -> None:
        self.builtins = globals()["__builtins__"]
        self.builtin_print = self.builtins["print"]
        self.full_log_color: str = 'cyan'
        self.info_color: str = 'white'
        self.warning_color: str = 'yellow'
        self.path = path
        self.time = time

    def _info(self, msg: str, color: str = 'white', prefix: str = 'INFO') -> None:
        self.builtins["print"] = self.builtin_print

        if self.time:
            date = datetime.datetime.now()
            msg = f'[{datetime.datetime.strftime(date, "%H:%M:%S")}] {prefix}: {msg}'
            print(colored(msg, color))
        else:
            msg = colored(f'{prefix}: {msg}', color)
            print(msg)

        if self.path:
            self._write_file(msg)

    def _warning(self, msg: str) -> None:
        self.builtins["print"] = self.builtin_print

        if self.time:
            date = datetime.datetime.now()
            msg = f'[{datetime.datetime.strftime(date, "%H:%M:%S")}] WARNING: {msg}'
            print(colored(msg, self.warning_color))
        else:
            msg = colored(f'WARNING: {msg}', self.warning_color)
            print(msg)

        if self.path:
                self._write_file(msg)

    def _write_file(self, msg):
        try:
            with open(f'{self.path}/py3_cli.log', 'a') as file:
                file.write(msg + '\n')
        except:
            raise CLIError('Log recording error')
            exit()


class CLIError(Exception):
    def __init__(self, text):
        self.txt = text
