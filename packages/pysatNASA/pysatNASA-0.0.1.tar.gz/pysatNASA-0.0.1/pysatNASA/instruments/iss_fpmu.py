# -*- coding: utf-8 -*-
"""Supports the Floating Potential Measurement Unit
(FPMU) instrument onboard the International Space
Station (ISS). Downloads data from the NASA
Coordinated Data Analysis Web (CDAWeb).

Properties
----------
platform
    'iss'
name
    'fpmu'
tag
    None Supported
sat_id
    None supported

Warnings
--------
- Currently clean only replaces fill values with Nans.
- Module not written by FPMU team.

"""

import datetime as dt
import functools
import logging
import numpy as np

from pysat.instruments.methods import general as mm_gen
from pysatNASA.instruments.methods import cdaweb as cdw

logger = logging.getLogger(__name__)

platform = 'iss'
name = 'fpmu'
tags = {'': ''}
sat_ids = {'': ['']}
_test_dates = {'': {'': dt.datetime(2017, 10, 1)}}

# support list files routine
# use the default CDAWeb method
fname = 'iss_sp_fpmu_{year:04d}{month:02d}{day:02d}_v01.cdf'
supported_tags = {'': {'': fname}}
list_files = functools.partial(mm_gen.list_files,
                               supported_tags=supported_tags)
# support load routine
# use the default CDAWeb method
load = cdw.load

# support download routine
# use the default CDAWeb method
basic_tag = {'dir': '/pub/data/international_space_station_iss/sp_fpmu',
             'remote_fname': '{year:4d}/' + fname,
             'local_fname': fname}
supported_tags = {'': {'': basic_tag}}
download = functools.partial(cdw.download, supported_tags)

# support listing files currently on CDAWeb
list_remote_files = functools.partial(cdw.list_remote_files,
                                      supported_tags=supported_tags)


def init(self):
    """Initializes the Instrument object with instrument specific values.

    Runs once upon instantiation.

    """

    ackn_str = ' '.join(('Data provided through NASA CDAWeb.  Contact',
                         'Rob.Suggs@nasa.gov for support and use.'))
    logger.info(ackn_str)
    self.acknowledgements = ackn_str
    self.references = ' '.join(('V. N. Coffey et al., "Validation of the',
                                'Plasma Densities and Temperatures From',
                                'the ISS Floating Potential Measurement',
                                'Unit," in IEEE Transactions on Plasma',
                                'Science, vol. 36, no. 5, pp. 2301-2308,',
                                'Oct. 2008,',
                                'doi: 10.1109/TPS.2008.2004271.\n',
                                'A. Barjatya, C.M. Swenson, D.C.',
                                'Thompson, and K.H. Wright Jr., Data',
                                'analysis of the Floating Potential',
                                'Measurement Unit aboard the',
                                'International Space Station, Rev. Sci.',
                                'Instrum. 80, 041301 (2009),',
                                'https://doi.org/10.1063/1.3116085'))

    return


def clean(inst):
    """Return FPMU data cleaned to the specified level.

    Parameters
    ----------
    inst : pysat.Instrument
        Instrument class object, whose attribute clean_level is used to return
        the desired level of data selectivity.

    """

    inst.data.replace(-999., np.nan, inplace=True)  # Te
    inst.data.replace(-9.9999998e+30, np.nan, inplace=True)  # Ni

    return None
