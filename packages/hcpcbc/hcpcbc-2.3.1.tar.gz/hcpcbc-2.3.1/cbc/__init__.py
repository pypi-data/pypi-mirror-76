# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2012-2020 Thorsten Simons (sw@snomis.eu)
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import argparse
import logging
from logging.handlers import RotatingFileHandler
from json import dump, load
from os import access, F_OK, makedirs
from getpass import getuser
from os.path import normpath, split
import hcpsdk
from cbc.init import Gvars, Ivars
from cbc.template import template
from cbc.tenants import updatetenants
from cbc.cbhandler import Handler
from cbc.charthandler import mkcharts


# Constants for collection granularity
P_HOUR  = hcpsdk.mapi.Chargeback.CBG_HOUR
P_DAY   = hcpsdk.mapi.Chargeback.CBG_DAY
P_TOTAL = hcpsdk.mapi.Chargeback.CBG_TOTAL
P_ALL   = hcpsdk.mapi.Chargeback.CBG_ALL

class HcpcbcError(Exception):
    """
    Raised on generic errors in **hcpcbc**.
    """

    def __init__(self, reason):
        """
        :param reason:  an error description
        """
        self.args = (reason,)


def parseargs():
    """
    args - build the argument parser, parse the command line and
           run the respective functions.
    """
    maindescription = '''
                        %(prog)s downloads the chargeback reports from one or
                        multiple HCP systems, as setup in the config file.
                        It keeps a timestamp of the last successfull
                        download and excludes everything prior to the
                        last time %(prog)s has been run.
                      '''

    mainparser = argparse.ArgumentParser(description=maindescription,
                                         prog=Gvars.Executable)
    mainparser.add_argument('--version', action='version',
                            version="%(prog)s: {0}\n".format(Gvars.Version))
    mainparser.add_argument('-c', dest='chartsonly', action='store_true',
                            help='create charts from existing reports, only '
                                 '(do nothing else)')
    mainparser.add_argument('-f', dest='infile', default=None,
                            help='allow to read/parse a (uncompressed) '
                                 'chargeback data file downloaded from the HCP '
                                 'management console. Make sure the settings '
                                 'in your config file are matches the content '
                                 'of INFILE!')
    mainparser.add_argument('-i', metavar='config.json', dest='ini',
                            default=normpath('./hcpcbc_config.json'),
                            help='path/name of the file containing the '
                                 'configuration (defaults to the current '
                                 'directory)')
    mainparser.add_argument('-u', dest='update', action='store_true',
                            help='update the Tenant list(s) and stop '
                                 'afterwards')
    mainparser.add_argument('--pastdays', dest='pastdays',
                            default=181, type=int,
                            help='start collection x days in the past')

    result = mainparser.parse_args()

    if result.pastdays > 181 or result.pastdays < 1:
        mainparser.error('--pastdays must be: 1 <= pastdays <= 181')
    if result.infile and (result.update or result.chartsonly):
        mainparser.error('-f excludes -u and/or -c')

    return result


def log(stdout, logtofile, debug, logfile, rotatemb, backups):
    """
    Setup logging

    :param stdout:      logging to stdout (bool)
    :param logtofile:   logging to file (bool)
    :param debug:       log in debug mode (bool)
    :param logfile:     name of file to log to
    returns:            the logger object
    """

    if not stdout and not logtofile:
        raise HcpcbcError('Err: at least one logger is needed')
    if logtofile and not logfile:
        raise HcpcbcError('Err: logfile needed')

    if debug:
        # fh = logging.Formatter('%(asctime)s [%(levelname)-6s] %(name)s.'
        #                        '%(module)s.%(funcName)s(%(lineno)d): '
        #                        '%(message)s',
        fh = logging.Formatter('%(asctime)s [%(levelname)-8s] %(name)s'
                               '.%(funcName)s(%(lineno)d): '
                               '%(message)s',
                               '%m/%d %H:%M:%S')
    else:
        fh = logging.Formatter('%(asctime)s [%(levelname)-8s] '
                               '%(message)s',
                               '%m/%d %H:%M:%S')

    logger = logging.getLogger()

    if stdout:
        sh = logging.StreamHandler()
        sh.setFormatter(fh)
        logger.addHandler(sh)
    if logtofile:
        try:
            makedirs(split(logfile)[0], exist_ok=True)
            lh = RotatingFileHandler(logfile,
                                     maxBytes=rotatemb * 1024 * 1024,
                                     backupCount=backups)
        except Exception as e:
            raise HcpcbcError('Err: logfile: {}'.format(e))
        else:
            lh.setFormatter(fh)
            logger.addHandler(lh)

    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logger = logging.getLogger(__name__)
    try:
        logger.debug('logging initialized')
    except KeyError as e:
        raise HcpcbcError(e)

    return logger


def createtemplate(file):
    """
    Create a template ini file

    :param file:    the filename to be created as template
    :raises:        *hcpcbcError*
    """
    print('A configuration file is not available.')
    answer = input('Do you want me to create a template for you (y/n)? ')

    if answer in ['y', 'Y', 'yes', 'Yes', 'YES']:
        try:
            with open(file, 'w') as outhdl:
                dump(template, outhdl, indent=4, sort_keys=True)
        except Exception as e:
            raise HcpcbcError(e)
    else:
        raise HcpcbcError('user denied creation')


class Config(object):
    """
    Read and update the configuration .ini file
    """

    def __init__(self, configfile):
        """
        :param configfile:  the configuration file from args
        :raises:            *HcpcbcError*
        """
        self.configfile = configfile

        if not access(self.configfile, F_OK):
            try:
                createtemplate(self.configfile)
            except HcpcbcError as e:
                raise HcpcbcError('Creation of template config file "{}" '
                                  'failed\n\thint: {}'
                                  .format(self.configfile, e))
            else:
                raise HcpcbcError('Creation of template config file "{}" '
                                  'was successfull\n\tYou need to edit it '
                                  'to fit your needs!'.format(self.configfile))

        # Load the configuration dict from configfile
        try:
            with open(self.configfile, 'r') as inhdl:
                Ivars.conf = load(inhdl)
        except Exception as e:
            raise HcpcbcError('Parsing the config file "{}" failed:\n'
                              '\thint: {}'.format(self.configfile, e))

        # Configure logging and make some checks
        try:
            log(Ivars.conf['9 logging']['1 log to stdout'],
                Ivars.conf['9 logging']['2 log to file'],
                Ivars.conf['9 logging']['6 debug'],
                Ivars.conf['9 logging']['3 logfile'],
                Ivars.conf['9 logging']['4 rotate MB'],
                Ivars.conf['9 logging']['5 backups'])

            # check for at least one store enabled
            if not Ivars.conf['3 stores']['2 local']['1 enable'] and not \
            Ivars.conf['3 stores']['3 compliant']['1 enable']:
                raise HcpcbcError('having no store enabled renders hcpcbc '
                                  'useless')

            # check for local store enabled if charts are asked for
            if Ivars.conf['4 charts']['1 enable'] and not \
            Ivars.conf['3 stores']['2 local']['1 enable']:
                raise HcpcbcError('can\'t create charts without local store '
                                  'enabled')

            if Ivars.conf['4 charts']['1 enable'] and not \
            Ivars.conf['4 charts']['a linear'] and not Ivars.conf['4 charts'][
                'b log']:
                raise HcpcbcError('with charts enable, at least one of linear '
                                  'and log needs to be true')

        except (KeyError, HcpcbcError) as e:
            raise HcpcbcError('Parsing the config file "{}" failed:\n'
                              '\thint: {}'.format(self.configfile, e))
        else:
            logger = logging.getLogger(__name__ + '.Config')
            logger.info('started run (user "{}")'.format(getuser()))


    def save(self):
        """
        Write the configuration dict file back to disk

        :raises:    *HcpcbcError*
        """
        try:
            with open(self.configfile, 'w') as confhdl:
                dump(Ivars.conf, confhdl, indent=4, sort_keys=True)
        except Exception as e:
            raise HcpcbcError('re-write of config file "{}" failed\n'
                              '\thint: {}'.format(self.configfile, e))
