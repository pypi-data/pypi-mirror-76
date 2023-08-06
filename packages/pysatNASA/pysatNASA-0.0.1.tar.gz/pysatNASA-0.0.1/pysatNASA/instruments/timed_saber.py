# -*- coding: utf-8 -*-
"""Supports the Sounding of the Atmosphere using Broadband Emission Radiometry
(SABER) instrument on the Thermosphere Ionosphere Mesosphere Energetics
Dynamics (TIMED) satellite.

Properties
----------
platform : string
    'timed'
name : string
    'saber'
tag : string
    None supported
sat_id : string
    None supported

Note
----
SABER "Rules of the Road" for DATA USE
Users of SABER data are asked to respect the following guidelines

  - Mission scientific and model results are open to all.
  - Guest investigators, and other members of the scientific community or
    general public should contact the PI or designated team member early in an
    analysis project to discuss the appropriate use of the data.
  - Users that wish to publish the results derived from SABER data should
    normally offer co-authorship to the PI, Associate PI or designated team
    members. Co-authorship may be declined. Appropriate acknowledgement of
    institutions, personnel, and funding agencies should be given.
  - Users should heed the caveats of SABER team members as to the
    interpretation and limitations of the data. SABER team members may insist
    that such caveats be published, even if co-authorship is declined. Data
    and model version numbers should also be specified.
  - Pre-prints of publications and conference abstracts should be widely
    distributed to interested parties within the mission and related projects.

Warnings
--------
- Note on Temperature Errors: http://saber.gats-inc.com/temp_errors.php


Authors
-------
J. Klenzing, 4 March 2019

"""

import datetime as dt
import logging
import functools

# CDAWeb methods prewritten for pysat
from pysat.instruments.methods import general as mm_gen
from pysatNASA.instruments.methods import cdaweb as cdw


logger = logging.getLogger(__name__)

platform = 'timed'
name = 'saber'
tags = {'': ''}
sat_ids = {'': ['']}
_test_dates = {'': {'': dt.datetime(2019, 1, 1)}}

fname = ''.join(('timed_l2av207_saber_{year:04d}{month:02d}{day:02d}',
                 '????_v01.cdf'))
supported_tags = {'': {'': fname}}
# use the CDAWeb methods list files routine
list_files = functools.partial(mm_gen.list_files,
                               supported_tags=supported_tags)

# let pysat know that data is spread across more than one file
multi_file_day = True

# Set to False to specify using xarray (not using pandas)
# Set to True if data will be returned via a pandas DataFrame
pandas_format = True

# use the default CDAWeb method
load = cdw.load

# use the default CDAWeb method
basic_tag = {'dir': '/pub/data/timed/saber/level2a_v2_07_cdf',
             'remote_fname': '{year:4d}/{month:02d}/' + fname,
             'local_fname': fname}
supported_tags = {'': {'': basic_tag}}
download = functools.partial(cdw.download, supported_tags, multi_file_day=True)

# support listing files currently on CDAWeb
list_remote_files = functools.partial(cdw.list_remote_files,
                                      supported_tags=supported_tags)


def init(self):
    """Initializes the Instrument object with instrument specific values.

    Runs once upon instantiation.


    """

    rules_url = 'http://saber.gats-inc.com/data_services.php'
    ackn_str = ' '.join(('Please see the Rules of the Road at',
                         rules_url))
    logger.info(ackn_str)
    self.acknowledgements = ackn_str
    self.references = ''

    return


def clean(inst):
    """Routine to return PLATFORM/NAME data cleaned to the specified level

    Cleaning level is specified in inst.clean_level and pysat
    will accept user input for several strings. The clean_level is
    specified at instantiation of the Instrument object.

    'clean' All parameters should be good, suitable for statistical and
            case studies
    'dusty' All paramers should generally be good though same may
            not be great
    'dirty' There are data areas that have issues, data should be used
            with caution
    'none'  No cleaning applied, routine not called in this case.


    Parameters
    ----------
    inst : pysat.Instrument
        Instrument class object, whose attribute clean_level is used to return
        the desired level of data selectivity.

    """

    return
