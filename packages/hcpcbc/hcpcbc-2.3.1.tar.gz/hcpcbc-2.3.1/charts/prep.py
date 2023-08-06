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

import sys
import logging
from csv import DictReader
from os import listdir, lstat
from stat import S_ISDIR, S_ISREG
from os.path import join

from . import ChartsError, M_DAY, M_HOUR, M_ALL, rec, S_SPECIALFOLDERS

logging.getLogger('charts.prep').addHandler(logging.NullHandler())


def prepdata(path, tenant=None, startdate=None, enddate=None, mode=M_DAY):
    """
    Create a data structure holding an HCPs summary chargeback data of all
    available Tenants or Namespaces. Reads a source folder structure created by
    **hcpcbc**.

    struct = {startdate (-> datetime): {"item_a": record (--> rec),
                                        "item_b": record(--> rec),
                                        "item_z": record(--> rec),}}

    Args:
        path:       the path under which the report files are stored
        tenant:     Tenant name or None if working on system level
        startdate:  a datetime object
        enddate:    a datetime object
        mode:       one of [M_DAY, M_HOUR]

    Returns:    the mentioned structure
    """
    logger = logging.getLogger(__name__)
    logger.debug('preparing data from "{}"'.format(path))

    if mode not in [M_DAY, M_HOUR]:
        raise ChartsError('mode must be one of {}'.format([M_DAY, M_HOUR]))

    # create the result structure (dict)
    res = {}

    # Get a list of items (Tenants or Namespaces)
    items = []
    try:
        logger.debug('path = {}'.format(path))
        for entry in listdir(path):
            logger.debug('entry = {}'.format(join(path, entry)))
            entrystat = lstat(join(path, entry))
            if (not tenant and not entry.startswith('.') and S_ISDIR(
                    entrystat.st_mode)):
                # --> working on system level
                items.append(entry)
            elif (tenant and not entry.startswith('.') and S_ISDIR(
                    entrystat.st_mode) and entry not in S_SPECIALFOLDERS):
                # --> working on tenant level
                items.append(entry)
            else:
                logger.debug('invalid entry "{}" in path "{}"'
                             .format(entry, path))
        else:
            logger.debug('path {} is empty...'.format(path))
    except FileNotFoundError as e:
        # if this one is raised, the expected path isn't available.
        raise ChartsError(e)
    except TypeError as e:
        logger.exception('line 88: path={}: {}'.format(path, e))
    except Exception as e:
        logger.exception('line 90: {}: {}'.format(type(e), e))
        raise ChartsError('line 90: {}: {}'.format(type(e), e))

    logger.debug('Items: {}'.format(items))

    # Crawl through all Tenants to collect report data
    for t in items:
        # Get a list of reports
        reports = []
        if not tenant:
            tpath = join(path, t, '__tenant', mode)
        else:
            tpath = join(path, t, mode)
        try:
            logger.debug('tpath = {}'.format(tpath))
            for entry in listdir(tpath):
                logger.debug('entry = {}'.format(join(tpath, entry)))
                entrystat = lstat(join(tpath, entry))
                logger.debug('entry = {}'.format(entry))
                if not entry.startswith('.') and S_ISREG(entrystat.st_mode):
                    reports.append(entry)
            else:
                logger.debug('tpath {} is empty...'.format(tpath))

        except FileNotFoundError:
            logger.debug('folder not available: "{}"'.format(tpath))
            continue
        except Exception as e:
            logger.debug('{}: {}'.format(type(e), e))
            continue

        reports.sort()
        logger.debug('\tReports for {}:'.format(t))
        for rep in reports:
            logger.debug('\t\t{}'.format(rep))

        # loop over the found reports and fill the result structure
        for rep in reports:
            with open(join(tpath, rep)) as csvhdl:
                reader = DictReader(csvhdl)
                for r in reader:
                    if (mode == M_DAY and r['startTime'][11:19] == '00:00:00' \
                                and  r['endTime'][11:19] == '23:59:59') or \
                       (mode == M_HOUR and r['startTime'][14:19] == '00:00' \
                                and  r['endTime'][14:19] == '59:59'):
                        thisrec = rec(r['objectCount'],
                                      r['ingestedVolume'],
                                      r['storageCapacityUsed'],
                                      r['bytesIn'], r['bytesOut'], r['reads'],
                                      r['writes'], r['deletes'],
                                      r['tieredObjects'],
                                      r['tieredBytes'],
                                      r['metadataOnlyObjects'],
                                      r['metadataOnlyBytes'], r['deleted'],
                                      r['valid'])
                        try:
                            res[r['startTime']][t] = thisrec
                        except KeyError:
                            res[r['startTime']] = {}
                            res[r['startTime']][t] = thisrec
                    else:
                        logger.debug('\t\tdropped: {} - {}'
                                     .format(r['startTime'], r['endTime']))

    return res
