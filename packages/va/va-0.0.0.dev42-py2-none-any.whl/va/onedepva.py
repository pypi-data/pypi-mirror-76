#!/usr/bin/env python

"""

onedepva.py

Used to run validation analysis for onedep system

Copyright [2013] EMBL - European Bioinformatics Institute
Licensed under the Apache License, Version 2.0 (the
"License"); you may not use this file except in
compliance with the License. You may obtain a copy of
the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the License for the
specific language governing permissions and limitations
under the License.

"""

__author__ = 'Zhe Wang'
__email__ = 'zhe@ebi.ac.uk'
__date__ = '2019-03-31'




import os
from PATHS import VAPATH
import glob
import sys
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

class onedepva:
    """

        Prepare everything before submit the jobs to run
        This is specifically used on ebi server side

    """


    def __init__(self):

        self.args = self.read_para()
        self.dir = self.args.d
        self.cl = self.args.c
        self.map, self.halfodd, self.halfeven = self.maps()
        self.mapsize = os.path.getsize(self.dir + '/' + self.map)


    def read_para(self):
        """

            Read arguments


        """
        import argparse, sys

        assert len(sys.argv) > 1, ('There has to be arguments for the command.\n \
               Usage: prepareandrun.py [-f [F]] [-run [all]/[slices...]]\n')

        parser = argparse.ArgumentParser(description='Create folders for entries')
        #parser = mainparser.add_mutually_exclusive_group(required = True)
        parser.add_argument('-run', nargs='*', help='Run customized validation analysis.', default='')
        requiredname = parser.add_argument_group('required arguments')
        requiredname.add_argument('-d', nargs='?', help='Deposited entry folder')
        requiredname.add_argument('-c', nargs='?', help='Recommended contour level')
        args = parser.parse_args()
        checkpar = (isinstance(args.run, type(None)) and isinstance(args.f, type(None)))
        if checkpar:
            print 'There has to be arguments for the command. \n \
                  usage: onedepva.py [-d [D] -c [C]] [-run [all]/[slices...]]\n'
            sys.exit()
        return args


    def fittedcifs(self):
        """
            Find all the fitted models for the map in the working folder

        :return: List of cif files with full paths
        """

        cif = self.dir + '/*.cif'
        cifs = glob.glob(cif)
        result = ''
        for cif in cifs:
            if cif is not None:
                result += cif.split('/')[-1]
        return result




    def maps(self):
        """
            Find all half maps for in the working folder

        :return:
        """

        mapre = self.dir + '/*.map'
        maps = glob.glob(mapre)
        halfmaps = []
        strhalf = 'half'
        for map in maps:
            mapname = map.split('/')[-1]
            if strhalf in mapname:
                halfmaps.append(map)
        numfiles = len(halfmaps)
        if numfiles == 2:
            ohalfodd, ohalfeven = halfmaps
        else:
            halfodd = None
            halfeven = None
            print 'Two half maps needed to calculate FSC.'

        # Find map string without any of the excluedstr which might be the target density map
        excluedstr = ['half', 'msk', 'mask']
        targetmap = [map for map in maps if not any(exstr in map for exstr in excluedstr)]
        if not targetmap:
            print 'Target map is missing. Please check the folder.'
        elif len(targetmap) > 1:
            print 'There should be only one target map. But multiple one found here.'
        else:
            omap = targetmap[0]

        map = omap.split('/')[-1]
        halfodd = ohalfodd.split('/')[-1]
        halfeven = ohalfeven.split('/')[-1]

        return map, halfodd, halfeven



    def runcmd(self):
        """

            The command needed to be run by va

        :return:
        """

        import subprocess

        cifs = self.fittedcifs()
        if cifs is None:
            incif = None
        elif len(cifs) == 1:
            incif = cifs[0]
        else:
            incif = cifs.join(' ')
        if self.args.run:
            orgcmd = '{}mainva.py -m {} -f {} -hmodd {} -hmeven {} -cl {} -d {} -run {}'.format(VAPATH, self.map,
                        incif, self.halfodd, self.halfeven, self.args.c, self.args.d, ' '.join(self.args.run))
        else:
            orgcmd = '{}mainva.py -m {} -f {} -hmodd {} -hmeven {} -cl {} -d {}'.format(VAPATH, self.map,
                        incif, self.halfodd, self.halfeven, self.args.c, self.args.d)

        cmd = orgcmd.split()
        # bsub cmd should be placed here for the server

        predmem = self.memmsg(self.mapsize)
        # bsub -M predmem .....
        print predmem
        print cmd
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=-1)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print output.strip()
            rc = process.poll()
        return rc


    def memmsg(self, mapsize):
        """

            Memory usage reminder based on memory prediction

        :return:
        """
        # When there is no emdid given, we use one level above the given "dir" to save the memory prediction file
        # input.csv. If emdid is given, we use the. self.dir is like /abc/cde/ so it needs to used os.path.dirname()
        # twice.
        import psutil
        vout = self.dir
        if os.path.isfile(vout + 'input.csv'):
            mempred = self.mempred(vout + 'input.csv', 2 * mapsize)
            print 'The memory you may need is %s M' % mempred
            assert mempred < psutil.virtual_memory().total / 1024 / 1024, 'The memory needed to run may exceed the total memory you have on the machine.'
            return mempred
        else:
            print 'No memory data available for prediction yet'
            return None

    @staticmethod
    def mempred(resultfile, inputfilesize):
        """

            Produce memory prediction results using linear regression
            based on the data from previous entries.


        :param resultfile: Previous memory usage information in CSV file
        :param inputfilesize: The input density map size
        :return: 0 or y_pred (the predicted memory usage)

        """
        import pandas as pd
        from sklearn.linear_model import LinearRegression
        from sklearn.metrics import mean_squared_error, r2_score
        from sklearn.model_selection import train_test_split
        from sklearn.model_selection import cross_val_score, cross_val_predict

        data = pd.read_csv(resultfile, header=0)
        data = data.dropna()
        newdata = data.iloc[:, 1:]
        sortdata = newdata.sort_values(newdata.columns[0])
        merdata = sortdata.groupby(sortdata.columns[0], as_index=False).mean()
        x = merdata['maprealsize']
        y = merdata['mem']
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
        if X_train.empty or X_test.empty or y_train.empty or y_test.empty or len(x.index) < 30:
            print 'Sparse data for memory prediction, result may not accurate.'
            return 0.
        else:
            lrmodel = LinearRegression(fit_intercept=False)
            # Perform CV
            print len(x.index)
            scores = cross_val_score(lrmodel, x.values.reshape(-1,1), y, cv=6)
            predictions = cross_val_predict(lrmodel, x.values.reshape(-1,1), y, cv=6)

            lrmodel.fit(X_train.values.reshape(-1, 1), y_train)
            lrpredict = lrmodel.predict(X_test.values.reshape(-1, 1))
            print '6-Fold CV scores:%s' % scores
            print 'CV accuracy: %s' % (r2_score(y, predictions))
            # print 'Score:%s' % (lrmodel.score(X_test.values.reshape(-1,1), y_test))
            print 'Linear model coefficients: %s' % (lrmodel.coef_)
            print 'MSE: %s' % (mean_squared_error(y_test, lrpredict))
            print 'Variance score(test accuracy): %s' % (r2_score(y_test, lrpredict))
            y_pred = lrmodel.predict(inputfilesize)

            return y_pred


def main():

    myobj = onedepva()
    myobj.runcmd()


if __name__ == '__main__':
    main()
