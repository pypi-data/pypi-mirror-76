# -*- coding: utf-8 -*-
# Created by Nicolae Gaidarji at 08.07.2020
import os
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0


class CFG:
    """
    Crearea fisierului cu setari *.ini

    Creating the *.ini settings file

    ex:
        config = CFG(CurentPath + '\\setup.ini')

        config.conf.add_section('DB TNS')
        config.create_cfg_file()
    """
    def __init__(self, file):
        self.conf = ConfigParser()
        self.writepath = file
        self.msg_except = None

    def create_cfg_file(self):
        if os.path.exists(self.writepath):
            self.conf.read(self.writepath)
        else:
            self.write_cfg_filee()

    def write_cfg_filee(self):
        self.msg_except  = None
        try:
            with open(self.writepath, 'w') as f:
                self.conf.write(f)
        except Exception as ex:
            self.msg_except = str(ex)

