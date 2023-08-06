"""
Logger for testpack
"""
import json
import logging
import os
import sys
from datetime import datetime, timezone

class Logger(logging.LoggerAdapter):

    """
    Logger adapter class for Testpack test scripts. Produces structured logs adhering to
    JSON schema recommended by STC evolution project.

    """

    def __init__(self, module_name, test_out_dir, testcase_id):
        handler = logging.FileHandler(os.path.join(test_out_dir, 'test.log.json'), mode='w')
        handler.setFormatter(logging.Formatter('%(message)s'))
        logr = logging.getLogger(module_name)
        logr.addHandler(handler)
        super().__init__(logr, {'testcase_id': testcase_id})

    def shutdown(self):
        '''shutdown'''
        self.debug("Logger shutdown")
        logging.shutdown()

    def debug(self, msg, **args):
        if super().isEnabledFor(logging.DEBUG):
            super().debug(self.log_message(msg, 'DEBUG', **args))

    def info(self, msg='', **args):
        if super().isEnabledFor(logging.INFO):
            super().info(self.log_message(msg, 'INFO', **args))

    def warning(self, msg='', **args):
        super().warning(self.log_message(msg, 'WARN', **args))

    def error(self, msg='', **args):
        super().error(self.log_message(msg, 'ERROR', **args))

    def critical(self, msg='', **args):
        super().critical(self.log_message(msg, 'FATAL', **args))

    def exception(self, msg='', **args):
        super().exception(self.log_message(msg, 'ERROR', **args))

    def console(self, msg):
        '''Show message on console'''
        sys.__stdout__.write(msg)
        sys.__stdout__.flush()

    def log_message(self, msg, level, **args):
        '''log_message'''
        logrec = LogEntry(self.extra['testcase_id'], level, msg, **args)
        return json.dumps(logrec.extra, default=str)

    def console_info(self, msg, end=False):
        '''
        When end flag is true, add a blank line after this msg
        When msg's lowercase is equal 'done', add a blank line after this msg
        '''
        if end:
            self.console(msg + '\n')
        elif msg.lower() == 'done':
            self.console(msg + '\n')
        else:
            self.console(msg)
        self.info(msg)

    def console_error(self, msg, start=True):
        '''when start flag is true, add a blank line before this msg'''
        if start:
            self.console('\n' + msg)
        else:
            self.console(msg)
        self.error(msg)

class LogEntry:
    """
    A LogEntry represents an event being logged
    """
    def __init__(self, testcase_id, level, msg, **args):
        self.extra = {"logger":testcase_id, "level":level, "timestamp":datetime.now(timezone.utc)}
        if msg != '':
            self.extra["message"] = msg
        for key, value in args.items():
            self.extra[key] = value
