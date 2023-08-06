'''
TestBase class for test case in the scripts
'''
import os
from genie.conf import Genie
import test_framework.testbase.stcsession as stcsession
import test_framework.testbase.snesession as snesession
import test_framework.testbase.spirent_logger as spirent_logger
from test_framework.testbase.settings import *

class TestBase():

    """
    Base class for test scripts.

    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    def __init__(self, test_input):
        if not test_input or not test_input.outdir:
            raise RuntimeError("Must specify output directory")

        if not test_input.testbed:
            raise RuntimeError("Must specify testbed filename")

        self.logger = spirent_logger.Logger(test_input.script_module, test_input.outdir, test_input.testcase_id)

        tb_path = os.path.join(test_input.outdir, test_input.testbed)
        if not os.path.exists(test_input.outdir) or not os.path.exists(tb_path):
            raise RuntimeError("no such file: " + tb_path)

        try:
            self.testbed = Genie.init(tb_path)
            self.logger.info(object=TESTBED_OBJECT, event="initialized")
        except Exception as excep:
            raise RuntimeError("Genie init failed - {}".format(excep))

        session_name = 'testpack001'
        if isinstance(self.testbed.custom.get('global_config'), type({})):
            if self.testbed.custom['global_config'].get('session_name_lab_server') not in ("None", None):
                session_name = self.testbed.custom['global_config']['session_name_lab_server']
        self.stc = stcsession.StcSession(self.testbed, self.logger, session_name=session_name, debug_level=1)
        self.sne = None
        self.test_input = test_input
        self.set_dut = getattr(test_input, 'set_dut', 'false').lower()
        if self.set_dut == 'true':
            next_flag = 'n'
            continue_flag = 'n'
            while (continue_flag.lower() != 'y'):
                if (next_flag.lower() == 'y'):
                    self.logger.console('\nWill start to execute the scirpt, go ahead? [Y/N]: ')
                    continue_flag = input('')
                    next_flag = 'n'
                else:
                    self.logger.console('\nPlease input "y" to run script after the DUT configuration is ready: ')
                    next_flag = input('')

    def setup(self):
        '''setup method'''

        self.stc.start()

        sne_devices = self.testbed.find_devices(os=SPIRENT_OS, type=SNE_TYPE)
        if sne_devices:
            self.sne = snesession.SneSession(sne_devices, self.logger, self.test_input.outdir)

    def cleanup(self):
        '''cleanup method'''
        if self.stc is not None:
            self.logger.console("Downloading stc logs...")
            try:
                self.stc.download_all_files(self.test_input.outdir)
                self.logger.console("done\n")
            except Exception as excep:
                self.logger.error(object=STC_OBJECT, event="download_all_files", exception=str(excep))
            self.logger.console("Releasing stc ports...")
            try:
                self.stc.end()
                self.logger.console("done\n")
            except Exception as excep:
                self.logger.error(object=STC_OBJECT, event="end_stc", exception=str(excep))

        if self.sne is not None:
            try:
                self.sne.end()
            except Exception as excep:
                self.logger.error(object=SNE_OBJECT, event="end_sne", exception=str(excep))

        if self.logger is not None:
            self.logger.shutdown()

    def save_stc_config(self):
        '''save stc config'''
        config_name = self.test_input.testcase_id + '.xml'
        self.stc.perform('saveasxml', filename=config_name)

    def raise_failure(self):
        '''raise failure info when fail'''
        failure_info = self.test_input.testcase_id + ' failed.'
        raise RuntimeError(failure_info)

    def save_stc_results(self, **args):
        '''save stc results'''
        result_file_name = self.test_input.testcase_id + '.db'
        if args:
            for key, value in args.items():
                if key == 'result_file_name':
                    result_file_name = value
        self.logger.console_info("Save results...")
        self.stc.perform('SaveResults', SaveDetailedResults=True, ResultFileName=result_file_name)
        self.logger.console_info("done")
