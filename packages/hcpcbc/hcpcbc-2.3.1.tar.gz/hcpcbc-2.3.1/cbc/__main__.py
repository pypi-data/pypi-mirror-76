#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2012-2020 Thorsten Simons (sw@snomis.eu)
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Sos of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyrighftware without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copiet notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import sys
import logging
from getpass import getuser
from os import makedirs
from tempfile import TemporaryDirectory
from pprint import pprint

import cbc


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    # collect the command line options
    opts = cbc.parseargs()

    # Read and parse the config file
    try:
        conf = cbc.Config(opts.ini)
    except cbc.HcpcbcError as e:
        sys.exit(e)

    logger = logging.getLogger(__name__)

    # update the config with a fresh list of available tenants, unless we read
    # from a file downloaded from MUI
    if not opts.infile:
        if not opts.chartsonly :
            try:
                if not cbc.updatetenants():
                    logger.critical('wasn\'t able to access any HCP system - aborting')
                    sys.exit(1)
            except Exception as e:
                logger.exception('updatetenants() failed\n\thint: {}'.format(e))
                sys.exit(1)
    else:
        logger.info('skipping the Tenant list(s) update')


    # if the -u flag has been set, update the Tenant list(s), only!
    if not opts.update:

        # Create a temporary store
        try:
            makedirs(cbc.Ivars.conf['3 stores']['1 temporary']['1 tempdir'],
                     exist_ok=True)
            tmpstore = TemporaryDirectory(
                    dir=cbc.Ivars.conf['3 stores']['1 temporary'][
                        '1 tempdir'],
                    suffix='.cbc')
        except KeyError as e:
            logger.error(
                    'parsing the config file failed:\n\thint: {}'.format(e))
            sys.exit(1)

        logger.debug('Using temporary store at "{}"'.format(tmpstore.name))

        try:
            # make sure we don't collect new reports if the '-c' flag is given
            if opts.chartsonly:
                logger.info('skipping report download')
            else:
                #   Loop over all configured HCP systems
                handlers = {}  # used to store all the handlers we'll create
                for target, idx in zip(cbc.Ivars.conf['1 targets'],
                                       range(0,
                                             len(cbc.Ivars.conf[
                                                     '1 targets']))):
                    # make sure we don't process targets that don't have any Tenants
                    if target['9 tenants']:
                        logger.info('working on target "{}" (idx={})'
                                    .format(target['1 fqdn'], idx))
                        handlers[target['1 fqdn']] = {}

                        # Now, let's create hcpsdk.cbhandler.Handler() objects for
                        # each Tenant
                        for tenant in target['9 tenants'].keys():
                            # skip Tenants that are disabled from collection
                            if not target['9 tenants'][tenant][
                                '0 enable collection']:
                                logger.info(
                                        '\tskipping Tenant "{}"'.format(
                                            tenant))
                                continue
                            else:
                                logger.info(
                                        '\tcollecting from Tenant "{}"'.format(
                                                tenant))

                            handler = cbc.Handler(idx, tenant, tmpstore,
                                                  opts.pastdays, nocon=True if opts.infile else False)
                            # make sure we catch the case where we don't have
                            # access to the Tenant...
                            try:
                                if not opts.infile:
                                    handler.download()
                                else:
                                    handler.readfile(opts.infile)
                            except cbc.HcpcbcError as e:
                                logger.warning(e)
                            else:
                                handler.dissect()
                                if cbc.Ivars.conf['3 stores']['2 local'][
                                    '1 enable']:
                                    handler.transferlocal()
                                if cbc.Ivars.conf['3 stores']['3 compliant'][
                                    '1 enable']:
                                    handler.transfercompliant()
                            finally:
                                handler.close()
                    else:
                        logger.warning(
                            'target "{}" (idx={}) has no Tenants listed'
                            .format(target['1 fqdn'], idx))

            # now create charts from the data available
            try:
                if cbc.Ivars.conf['4 charts'][
                    '1 enable'] or opts.chartsonly:
                    cbc.mkcharts(tmpstore.name)
            except Exception as f:
                logger.error('\tchart creation failed\n\thint: {}'.format(f))

        except KeyError as e:
            logger.error(
                    'parsing the config file failed:\n\thint: {}'.format(e))

        # remove the temporary store
        tmpstore.cleanup()

    # re-save the configfile
    try:
        conf.save()
    except cbc.HcpcbcError as e:
        logger.error('failed to re-write the configfile\n\thint: {}'
                     .format(getuser(), e))

    logger.info('finished run (user "{}")\n'.format(getuser()))


if __name__ == '__main__':
    main()
