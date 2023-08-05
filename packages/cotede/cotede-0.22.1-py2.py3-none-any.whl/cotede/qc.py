""" Apply Quality Control of CTD profiles
"""

import pkg_resources
from collections import OrderedDict
from datetime import datetime
from os.path import basename
import re
import json
import logging
from typing import Any, Dict, Hashable, Mapping

import numpy as np
from numpy import ma

from cotede.qctests import *
import cotede.qctests
from cotede.misc import combined_flag
from cotede.utils import load_cfg


module_logger = logging.getLogger(__name__)


def standard_name(name):
    if name[:4] == 'TEMP':
        return name.replace('TEMP', 'sea_water_temperature')
    elif name[:4] == 'PSAL':
        return name.replace('PSAL', 'sea_water_salinity')

    else:
        return name


class CoTeDeDataModel(object):
    def __init__(self):
        self.attrs = {}
        self.data = {}

    def __getitem__(self, key):
        return self.data[key]

    def keys(self):
        return self.data.keys()

    @property
    def attributes(self):
        print('attributes will be removed. Use attrs instead!')
        return self.attrs


class ProfileQC(object):
    """Quality Control a CTD profile
    """

    def __init__(self, input, cfg=None, saveauxiliary=True, verbose=True,
            attributes=None):
        """A procedure to QC a hydrographic profile

        Parameters
        ----------
        input: dict-like
            An object with the data to be evaluated that responds like a
            dictionary. For instance, a variable pressure should be acessible
            as input['pressure'], or temperature as input['temperature'].
            This input object could have attrs, with global attributes for
            the whole dataset. For instance, input.attrs['lat'] would give the
            nominal latitude of the dataset input.

        cfg: dict-like or str
            The QC configuration to be used in the current profile. If a
            string, it should be the name of a JSON QC configuration. Check
            the manual for the available options.

        saveauxiliary: bool
            Save features as .features

        verbose: bool
            Show extra information

        attributes: dict-like, optional
            If given, append/overwirte the input.attrs

        Methods
        -------
        keys(self): List of input contents
        """
        # self.logger = logging.getLogger(logger or 'cotede.ProfileQC')

        try:
            self.name = input.filename
        except:
            self.name = None
        self.verbose = verbose

        if attributes is None:
            assert (hasattr(input, 'attrs'))
        assert (hasattr(input, 'keys')) and (len(input.keys()) > 0)

        self.cfg = load_cfg(cfg)
        module_logger.debug("Using cfg: {}".format(self.cfg))

        self.input = input
        if attributes is None:
            self._attrs = input.attrs
        else:
            self._attrs = attributes
        self.flags = {}
        self._features = None
        self.saveauxiliary = saveauxiliary
        saveauxiliary = False
        if saveauxiliary:
            # build_auxiliary is not exactly the best way to do it.
            self.build_features()

        if 'common' in self.cfg:
            self.evaluate_common(self.cfg)

        for v in self.input.keys():
            for c in self.cfg['variables']:
                doit = (hasattr(self.input[v], 'attrs') and
                        ('standard_name' in self.input[v].attrs) and
                        (self.input[v].attrs['standard_name'] == c))
                doit = doit or re.match("(%s)2?$" % c, standard_name(v))
                if doit:
                    module_logger.debug(" %s - evaluating: %s, as type: %s" %
                                            (self.name, v, c))
                    self.evaluate(v, self.cfg['variables'][c])
                    break

    @property
    def attrs(self) -> Dict[Hashable, Any]:
        """Dictionary with attributes of the profile

        Any time of information relevant to the whole profile. For
        instance, this is the place where CoTeDe will search for the
        nominal latitude and longitude of the profile, as well as the
        nominal date and time.

        Dictionary of global attributes on this dataset
        """
        if self._attrs is None:
            self._attrs = {}
        return self._attrs


    @attrs.setter
    def attrs(self, value: Mapping[Hashable, Any]) -> None:
        self._attrs = dict(value)


    @property
    def features(self) -> Dict[Hashable, Any]:
        """Dictionary with the features obtained for each variable

        Each variable evaluated from the input will be an item in features,
        which will contain a dict-like with each feature obtained, which will
        contain a numpy Array with a sequence of values, one for each
        measurement. For example, features could look like:

            {'temp': {
                'gradient': [1, 2, 3],
                'spike': [0.1, 0.2, 0.3]
                },
            'sal': {
                'gradient': [0.4, 0.5, 0.6],
                'spike': [0.04, 0.05, 0.06]
                }
            }
        """
        if self._features is None:
            self._features = {}
        return self._features


    @features.setter
    def features(self, value: Mapping[Hashable, Any]) -> None:
        self._features = dict(value)


    @property
    def flags(self) -> Dict[Hashable, Any]:
        """Dictionary with the flags resulted from the QC tests

        Like the features, each variable evaluated from the input will be an
        item in flags, whicll will contain a dict-like with each test applied,
        which will contain a numpy Array with a sequence of values according
        to the flag values defined in the manual. For example, flags could
        look like:

            {'temp': {
                'gradient': [1, 1, 3],
                'spike': [1, 1, 4]
                },
            'sal': {
                'gradient': [1, 2, 9],
                'spike': [1, 1, 9]
                }
            }
        """
        if self._flags is None:
            self._flags = {}
        return self._flags


    @flags.setter
    def flags(self, value: Mapping[Hashable, Any]) -> None:
        self._flags = dict(value)


    @property
    def data(self):
        return self.input.data

    @property
    def attributes(self):
        """Temporary solution while migrating attributes -> attrs
        """
        return self.attrs

    @property
    def auxiliary(self):
        module_logger.warning('ATENTION: Please use .features instead.'
                              'auxiliary will be eventually removed.')
        return self.features

    def keys(self):
        """ Return the available keys in self.data
        """
        return self.input.keys()

    def __getitem__(self, key):
        """ Return the key array from self.data
        """
        return self.input[key]

    def evaluate_common(self, cfg):
        self.flags['common'] = {}
        if 'common' not in self.features:
            self.features['common'] = {}

        if 'valid_datetime' in self.cfg['common']:
            if 'datetime' in self.attrs.keys() and \
                    type(self.attrs['datetime']) == datetime:
                f = 1
            else:
                f = 3
            self.flags['common']['valid_datetime'] = f

        if 'datetime_range' in self.cfg['common']:
            if 'datetime' in self.attrs.keys() and \
                    (self.attrs['datetime'] >=
                            self.cfg['common']['datetime_range']['minval']) and \
                    (self.attrs['datetime'] <=
                            self.cfg['common']['datetime_range']['maxval']):
                f = 1
            else:
                f = 3
            self.flags['common']['datetime_range'] = f

        if 'location_at_sea' in self.cfg['common']:
            y = LocationAtSea(self.input, cfg['common']['location_at_sea'])

            for f in y.features.keys():
                self.features['common'][f] = y.features[f]
            for f in y.flags:
                self.flags['common'][f] = y.flags[f]

        # if self.saveauxiliary:
        #     self.features['common'] = {}
        #     # Need to improve this. descentPrate doesn't make sense
        #     #   for Argo. That's why the try.
        #     try:
        #         self.features['common']['descentPrate'] = \
        #                 descentPrate(self.input)
        #     except:
        #         pass

    def evaluate(self, v, cfg):

        self.flags[v] = {}

        # Apply common flag for all points.
        if 'common' in self.flags:
            N = self.input[v].shape
            for f in self.flags['common']:
                self.flags[v][f] = self.flags['common'][f] * \
                        np.ones(N, dtype='i1')

        if v not in self.features:
            self.features[v] = {}

        if 'platform_identification' in cfg:
            module_logger.warning(
                    "Sorry I'm not ready to evaluate platform_identification()")

        if 'valid_speed' in cfg:
            # Think about. Argo also has a test valid_speed, but that is
            #   in respect to sucessive profiles. How is the best way to
            #   distinguish them here?
            try:
                if self.saveauxiliary:
                    self.flags[v]['valid_speed'], \
                            self.features[v]['valid_speed'] = \
                            possible_speed(self.input, cfg['valid_speed'])
            except:
                module_logger.warning("Fail on valid_speed")

        if 'pressure_increasing' in cfg:
            module_logger.warning(
                    "Sorry, I'm no ready to evaluate pressure_increasing()")

        if 'grey_list' in cfg:
            module_logger.warning("Sorry I'm not ready to evaluate grey_list()")

        if 'gross_sensor_drift' in cfg:
            module_logger.warning(
                    "Sorry I'm not ready to evaluate gross_sensor_drift()")

        if 'frozen_profile' in cfg:
            module_logger.warning(
                    "Sorry I'm not ready to evaluate frozen_profile()")

        # for c in cfg:
        #     if cfg[c] == None:
        #         cfg[c] = OrderedDict()
        #     print(c)
        #     if ("test" not in cfg[c]):
        #         cfg[c]["test"] = c

        # for criterion in cfg:
        #     assert hasattr(cotede.qctests, criterion['procedure'])
        #     Procedure = eval("cotede.qctests.{}".format(criterion['procedure']))
        for criterion in cfg:
            if (cfg[criterion] is not None) and ('procedure' in cfg[criterion]) and (cfg[criterion]['procedure'] in cotede.qctests.QCTESTS):
                print(criterion)
                Procedure = cotede.qctests.QCTESTS[cfg[criterion]['procedure']]
                print(Procedure)
                if issubclass(Procedure, cotede.qctests.QCCheckVar):
                    y = Procedure(self.input, v, cfg[criterion], autoflag=True)
                elif issubclass(Procedure, cotede.qctests.QCCheck):
                    y = Procedure(self.input, cfg[criterion], autoflag=True)

                if self.saveauxiliary:
                    for f in y.features.keys():
                        self.features[v][f] = y.features[f]
                for f in y.flags:
                    self.flags[v][f] = y.flags[f]

                # except:
                #     module_logger.warning("Fail on density_inversion")

        #if 'spike_depthsmooth' in cfg:
        #    from maud.window_func import _weight_hann as wfunc
        #    cfg_tmp = cfg['spike_depthsmooth']
        #    cfg_tmp['dzwindow'] = 10
        #    smooth = ma.masked_all(self.input[v].shape)
        #    z = ped['pressure']
        #    for i in range(len(self.input[v])):
        #        ind = np.nonzero(ma.absolute(z-z[i]) < \
        #                cfg_tmp['dzwindow'])[0]
        #        ind = ind[ind != i]
        #        w = wfunc(z[ind]-z[i], cfg_tmp['dzwindow'])
        #        smooth[i] = (T[ind]*w).sum()/w.sum()


        #if 'pstep' in cfg:
        #    ind = np.isfinite(self.input[v])
        #    ind = ma.getmaskarray(self.input[v])
        #    if self.saveauxiliary:
        #        self.features[v]['pstep'] = ma.concatenate(
        #                [ma.masked_all(1),
        #                    np.diff(self.input['PRES'][ind])])

        # FIXME: the Anomaly Detection and Fuzzy require some features
        #   to be estimated previously. Generalize this.
        from cotede.utils.config import guess_procedure
        if 'anomaly_detection' in  cfg:
            for c in cfg['anomaly_detection']['features']:
                if c not in self.features[v]:
                    print(c)
                    print(guess_procedure(c))
                    Procedure = cotede.qctests.QCTESTS[guess_procedure(c)]

                    if issubclass(Procedure, cotede.qctests.QCCheckVar):
                        y = Procedure(self.input, v, None, autoflag=False)
                    elif issubclass(Procedure, cotede.qctests.QCCheck):
                        y = Procedure(self.input, None, autoflag=False)
                    for f in y.features.keys():
                        self.features[v][f] = y.features[f]    



            features = {}
            for f in cfg['anomaly_detection']['features']:
                try:
                    features[f] = self.features[v][f]
                except:
                    if f == 'spike':
                        features['spike'] = spike(self.input[v])
                    elif f == 'gradient':
                        features['gradient'] = gradient(self.input[v])
                    elif f == 'constant_cluster_size':
                        features['constant_cluster_size'] = \
                                constant_cluster_size(self.input[v])
                    elif f == 'tukey53H_norm':
                        features['tukey53H_norm'] = tukey53H_norm(self.input[v])
                    elif f == 'rate_of_change':
                        features['rate_of_change'] = rate_of_change(self.input[v])
                    elif (f == 'woa_normbias'):
                        y = WOA_NormBias(self.input, v, {}, autoflag=False)
                        features['woa_normbias'] = \
                                np.abs(y.features['woa_normbias'])
                    elif (f == 'cars_normbias'):
                        y = CARS_NormBias(self.input, v, {}, autoflag=False)
                        features['cars_normbias'] = \
                                np.abs(y.features['cars_normbias'])
                    else:
                        module_logger.error(
                                "Sorry, I can't evaluate anomaly_detection with: %s" % f)

            try:
                prob, self.flags[v]['anomaly_detection'] = \
                        anomaly_detection(features, cfg['anomaly_detection'])

                if self.saveauxiliary:
                    self.features[v]['anomaly_detection'] = prob
            except:
                pass

        if 'morello2014' in cfg:
            self.flags[v]['morello2014'] = morello2014(
                    features=self.features[v],
                    cfg=cfg['morello2014'])

        if 'fuzzylogic' in  cfg:
            features = {}
            for f in cfg['fuzzylogic']['features']:
                try:
                    features[f] = self.features[v][f]
                except:
                    module_logger.error("Can't evaluate fuzzylogic with: %s" % f)

            self.flags[v]['fuzzylogic'] = fuzzylogic(
                    features=features,
                    cfg=cfg['fuzzylogic'])

        self.flags[v]['overall'] = combined_flag(self.flags[v])

    def build_features(self):
        if not hasattr(self, 'features'):
            self.features = {}

        self.features['common'] = {}
        # Need to improve this. descentPrate doesn't make sense
        #   for Argo. That's why the try.
        if ('common' in self.cfg) and ('descentPrate' in self.cfg['common']):
            try:
                self.features['common']['descentPrate'] = \
                        descentPrate(self.input)
            except:
                module_logger.warning("Failled to run descentPrate")


class ProfileQCed(ProfileQC):
    """
    """
    def __init__(self, input, cfg=None):
        """
        """
        self.name = 'ProfileQCed'
        super(ProfileQCed, self).__init__(input, cfg)

    def keys(self):
        """ Return the available keys in self.data
        """
        return self.input.keys()

    def __getitem__(self, key):
        """ Return the key array from self.data
        """
        if key not in self.flags.keys():
            return self.input[key]
        else:
            return ma.masked_array(self.input[key].data,
                    mask=(self.flags[key]['overall']!=1))

        raise KeyError('%s not found' % key)
