#!/usr/bin/env python

"""

preparaeandrun.py

Used to run validation analysis for EBI by using EMDID

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
__date__ = '2018-12-12'




import sys, os
from PATHS import MAP_SERVER_PATH, VASOURCE, VAPATH, CIFSOURCE, VTPSOURCE, ENTSOURCE, FORDISPLAY
import collections
from shutil import copyfile, copyfileobj, copy2, rmtree, move, ignore_patterns, copytree
import pandas as pd
from memory_profiler import memory_usage


class prepareandrun:
    """

        Prepare everything before submit the jobs to run
        This is specifically used on ebi server side

    """


    def __init__(self):

        # Read emdids and specific runs if needed
        self.args = self.read_para()
        self.emdid = self.args.f
        # Create corresponding folders if there are not exist
        self.idsubdirs = self.folders(self.emdid)
        idpaths = self.CreateFolders(self.idsubdirs)
        self.CopyFiles(idpaths)
        subdir = list(self.idsubdirs.values())[0]
        emdid = list(self.idsubdirs.keys())[0]
        fullmap = '{}{}/va/emd_{}.map'.format(MAP_SERVER_PATH, subdir, emdid)
        self.gzipmap(fullmap + '.gz')
        self.mapsize = os.path.getsize(fullmap)

    # def subdir(self):
    #
    #     breakdigits = 2
    #     emdbidmin = 4
    #     print self.emdid
    #     print type(self.emdid)
    #     if len(self.emdid) >= emdbidmin and isinstance(self.emdid, str):
    #         topsubpath = emdid[:breakdigits]
    #         middlesubpath = emdid[breakdigits:-breakdigits]
    #         subpath = os.path.join(topsubpath, middlesubpath, self.emdid)
    #         result = subpath + '/va'
    #         return result


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
        requiredname.add_argument('-f', nargs='*', help='EMDB entry id')
        args = parser.parse_args()
        checkpar = (not args.run) and (not args.f)
        assert not checkpar, 'There has to be arguments for the command. \n \
                usage: prepareandrun.py [-f [F]] [-run [all]/[slices...]]\n'

        return args

    def folders(self, emdids):
        """

            Folders' paths for the entry with its ids

        :return: None
        """



        idsubdirs = collections.OrderedDict()
        breakdigits = 2
        emdbidmin = 4
        for id in emdids:
            if len(id) >= emdbidmin and isinstance(id, str):
                topsubpath = id[:breakdigits]
                middlesubpath = id[breakdigits:-breakdigits]
                subpath = os.path.join(topsubpath, middlesubpath, id)
                idsubdirs[id] = subpath

        return idsubdirs

    @staticmethod
    def CreateFolders(idsubdirs):
        """
            For each subdirs create its corresponding full directory

        :param subdirs: numeric sub-directory
        :return:
        """

        import errno

        idpaths = collections.OrderedDict()
        for id, dir in idsubdirs.items():
            fullpath = MAP_SERVER_PATH + dir + '/va'
            if not os.path.exists(fullpath):
                try:
                    original_umask = os.umask(0)
                    os.makedirs(fullpath, 0o777)
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
                finally:
                    os.umask(original_umask)
            idpaths[id] = fullpath


        return idpaths

    @classmethod
    def CopyFiles(self, idpaths):
        """

                Copy all needed files to the its va folder

        :param emdids: All emdids given in the folder
        :return: None
        """

        for id, path in idpaths.items():
            fullorggzmap, fulloddgzmap, fullevengzmap = self.copymaps(id, path)
            self.gzipmap(fullorggzmap)
            if fulloddgzmap is not None:
                self.gzipmap(fulloddgzmap)
            if fullevengzmap is not None:
                self.gzipmap(fullevengzmap)
            self.copyfsc(id, path)
            self.copyheader(id, path)
            fitmodels = self.FindfittedModel(id, path)
            reccl = None
            fitcifs = None
            if fitmodels is not None:
                fitcifs = fitmodels['fitmodels']
                reccl = fitmodels['reccl']
            if reccl:
                self.copyvtp(id, path, reccl)
            if fitcifs:
                for cif in fitcifs:
                    cifgz = path + '/' + cif + '.gz'
                    entgz = path + '/pdb' + cif[:-4] + '.ent.gz'
                    sourcecif = '{}{}.gz'.format(CIFSOURCE, cif)
                    sourceent = '{}pdb{}.ent.gz'.format(ENTSOURCE, cif[:-4])
                    if os.path.isfile(sourcecif):
                        self.copycif(cif, path)
                        self.gzipmap(cifgz)
                    else:
                        print('!!{} not exist.'.format(sourcecif))
                    if os.path.isfile(sourceent):
                        self.copyent(cif, path)
                        self.gzipmap(entgz)
                    else:
                        print('!!{} not exist'.format(sourceent))


    @staticmethod
    def copyent(cif, path):
        """

            Copy the fitted ent file

        :param id:
        :param path:
        :return:
        """

        srcent = '{}pdb{}.ent.gz'.format(ENTSOURCE, cif[:-4])
        desent = '{}/pdb{}.ent.gz'.format(path, cif[:-4])

        if not os.path.isfile(srcent):
            sys.stderr.write('!!File {} not exist\n'.format(srcent))
        else:
            if os.path.isfile(desent):
                sys.stderr.write('File {} exist and no need to copy\n'.format(desent))
            else:
                copyfile(srcent, desent)

        return None

    @staticmethod
    def copyvtp(id, path, reccl):
        """

            Copy the right vtp file which used to produce the surface view

        :param id:
        :param path:
        :return:
        """

        breakdigits = 2
        emdbidmin = 4
        subpath = None
        if len(id) >= emdbidmin and isinstance(id, str):
            topsubpath = id[:breakdigits]
            middlesubpath = id[breakdigits:-breakdigits]
            subpath = os.path.join(topsubpath, middlesubpath, id)
        srcvtp = '{}{}/vtp/emd_{}_{}.vtp'.format(VTPSOURCE, subpath, id, str(float(reccl)))
        desvtp = '{}/emd_{}_{}.vtp'.format(path, id, str(float(reccl)))

        if not os.path.isfile(srcvtp):
            sys.stderr.write('!!File {} not exist\n'.format(srcvtp))
        else:
            if os.path.isfile(desvtp):
                sys.stderr.write('File {} exist and no need to copy\n'.format(desvtp))
            else:
                copyfile(srcvtp, desvtp)

        return None


    @staticmethod
    def copycif(cif, path):
        """
            Copy cif file with id cif to path folder

        :param cif:
        :param path:
        :return:
        """

        srccif = CIFSOURCE + cif + '.gz'
        descif = path + '/' + cif + '.gz'

        if not os.path.isfile(srccif):
            sys.stderr.write('!!File {} not exist\n'.format(srccif))
        else:
            if os.path.isfile(descif):
                sys.stderr.write('File {} exist and no need to copy\n'.format(descif))
            else:
                copyfile(srccif, descif)

        return None

    @staticmethod
    def copyheader(id, path):
        """

            Copy the header file to its va folder

        :param id: emdid
        :param path: va path
        :return: None
        """

        header = 'header'
        orgheader = 'emd-{}.xml'.format(id)
        srcroot = '{}EMD-{}'.format(VASOURCE, id)
        srcheaderpath ='{}/{}/'.format(srcroot, header)
        srcheader = '{}{}'.format(srcheaderpath, orgheader)

        desheaderpath = '{}/'.format(path)
        desheader = '{}{}'.format(desheaderpath, orgheader)

        if not os.path.isfile(srcheader):
            sys.stderr.write('!!File {} not exist\n'.format(srcheader))
        else:
            if os.path.isfile(desheader):
                sys.stderr.write('File {} exist and no need to copy\n'.format(desheader))
            else:
                copyfile(srcheader, desheader)

        return None


    @staticmethod
    def copyfsc(id, path):
        """

            Copy the fsc file to its va folder

        :return:
        """

        fsc = 'fsc'
        orgfsc = 'emd_{}_fsc.xml'.format(id)
        srcroot = '{}EMD-{}'.format(VASOURCE, id)
        srcfscpath ='{}/{}/'.format(srcroot, fsc)
        srcfsc = '{}{}'.format(srcfscpath, orgfsc)

        desfscpath = '{}/'.format(path)
        desfsc = '{}{}'.format(desfscpath, orgfsc)

        if not os.path.isfile(srcfsc):
            sys.stderr.write('!!File {} not exist\n'.format(srcfsc))
        else:
            if os.path.isfile(desfsc):
                sys.stderr.write('File {} exist and no need to copy\n'.format(desfsc))
            else:
                copyfile(srcfsc, desfsc)

        return None


    @staticmethod
    def copymaps(id, path):
        """

            Base on the emdid and path of destination, copy the density map to the path folder

        :param id: emdid
        :param path: full path of the
        :return:
        """

        import glob

        map = 'map'
        other = 'other'
        masks = 'masks'
        srcroot = '{}EMD-{}/'.format(VASOURCE, id)
        gzorgmap = 'emd_{}.map.gz'.format(id)
        gzoddmap = 'emd_{}_half_map_1.map.gz'.format(id)
        gzevenmap = 'emd_{}_half_map_2.map.gz'.format(id)

        srcmappath = '{}/{}/'.format(srcroot, map)
        srchalfspath = '{}{}/'.format(srcroot, other)
        desmappath = '{}/'.format(path)



        srcmap = '{}{}'.format(srcmappath, gzorgmap)
        desmap = '{}{}'.format(desmappath, gzorgmap)

        maskstr = '{}masks/*_msk*.map'.format(srcroot)
        masks = glob.glob(maskstr)
        for mask in masks:
            copy2(mask, desmappath)

        if os.path.isdir(srchalfspath):
            srcoddmap = '{}{}'.format(srchalfspath, gzoddmap)
            srcevenmap = '{}{}'.format(srchalfspath, gzevenmap)
            desoddmap = '{}{}'.format(desmappath, gzoddmap)
            desevenmap = '{}{}'.format(desmappath, gzevenmap)
            if os.path.isfile(desoddmap):
                print('File {} exist in its folder'.format(srcoddmap))
            else:
                if os.path.isfile(srcoddmap):
                    copyfile(srcoddmap, desoddmap)
                else:
                    desoddmap = None
            if os.path.isfile(desevenmap):
                print('File {} exist in its folder'.format(srcevenmap))
            else:
                if os.path.isfile(srcevenmap):
                    copyfile(srcevenmap, desevenmap)
                else:
                    desevenmap = None
        else:
            desoddmap = desevenmap = None
            print('There is no half maps for this entry.')

        if not os.path.exists(desmappath):
            try:
                os.makedirs(desmappath, 0o7777)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

        if os.path.isfile(desmap):
            print('File {} exist in its folder.'.format(desmap))
        else:
            copyfile(srcmap, desmap)


        return desmap, desoddmap, desevenmap


    @staticmethod
    def gzipmap(fullgzmap):

        import gzip
        nosuffixmap = fullgzmap[:-3]
        if not os.path.isfile(nosuffixmap):
            with gzip.open(fullgzmap, 'rb') as f_in:
                with open(nosuffixmap, 'wb') as f_out:
                    copyfileobj(f_in, f_out)
        else:
            print('File {} exist no need to uncompress.'.format(nosuffixmap))

        return None

    def runcmd(self):
        """

            The command needed to be run by va

        :return:
        """

        import subprocess
        if self.args.run:
            orgcmd = '{}mainva.py -emdid {} -run {}'.format(VAPATH, self.args.f[0], ' '.join(self.args.run))
        else:
            orgcmd = '{}mainva.py -emdid {}'.format(VAPATH, self.args.f[0])

        cmd = orgcmd.split()
        # bsub cmd should be placed here for the server

        predmem = self.memmsg(self.mapsize)
        # bsub -M predmem .....
        print(cmd)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=-1)

        while True:
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                print(output.strip())
            rc = process.poll()

        return None






    def memmsg(self, mapsize):
        """

            Memory usage reminder based on memory prediction

        :return:
        """
        # When there is no emdid given, we use one level above the given "dir" to save the memory prediction file
        # input.csv. If emdid is given, we use the. self.dir is like /abc/cde/ so it needs to used os.path.dirname()
        # twice.
        import psutil
        vout = MAP_SERVER_PATH
        if os.path.isfile(vout + 'input.csv') and os.path.getsize(vout + 'input.csv') > 0:
            mempred = self.mempred(vout + 'input.csv', 2 * mapsize)
            if mempred is None:
                print('No memory prediction.')
                return None
            else:
                print('The memory you may need is {} M'.format(mempred))
                assert mempred < psutil.virtual_memory().total / 1024 / 1024, 'The memory needed to run may exceed the total memory you have on the machine.'
                return mempred
        else:
            print('No memory data available for prediction yet')
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
        from sklearn.linear_model import LinearRegression
        from sklearn.metrics import mean_squared_error, r2_score
        from sklearn.model_selection import train_test_split
        from sklearn.model_selection import cross_val_score, cross_val_predict

        data = pd.read_csv(resultfile, header=0)
        data = data.dropna()
        if data.empty:
            print('No useful data in the dataframe.')
            return None
        else:
            newdata = data.iloc[:, 1:]
            sortdata = newdata.sort_values(newdata.columns[0])
            merdata = sortdata.groupby(sortdata.columns[0], as_index=False).mean()
            x = merdata['maprealsize']
            y = merdata['mem']
            X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
            if X_train.empty or X_test.empty or y_train.empty or y_test.empty or len(x.index) < 30:
                print('Sparse data for memory prediction, result may not accurate.(at least 30 data entries)')
                return None
            else:
                lrmodel = LinearRegression(fit_intercept=False)
                # Perform CV
                scores = cross_val_score(lrmodel, x.values.reshape(-1,1), y, cv=6)
                predictions = cross_val_predict(lrmodel, x.values.reshape(-1,1), y, cv=6)

                lrmodel.fit(X_train.values.reshape(-1, 1), y_train)
                lrpredict = lrmodel.predict(X_test.values.reshape(-1, 1))
                print('6-Fold CV scores:{}'.format(scores))
                print('CV accuracy: {}'.format(r2_score(y, predictions)))
                # print 'Score:%s' % (lrmodel.score(X_test.values.reshape(-1,1), y_test))
                print('Linear model coefficients: {}'.format(lrmodel.coef_))
                print('MSE: {}'.format(mean_squared_error(y_test, lrpredict)))
                print('Variance score(test accuracy): {}'.format(r2_score(y_test, lrpredict)))
                y_pred = lrmodel.predict([[inputfilesize]])

                return y_pred


    @staticmethod
    def savepeakmemory(filename, maxmem):
        """

            Data collected and to be used for prediction for memory usage
            Memory saved as a comma separate CSV file.


        :param filename: String for file which used to collect data
        :param maxmem: Float number which gives peak memory usage of the finished job
        :return: None

        """

        columnname = 'mem'
        # dir = MAP_SERVER_PATH if self.emdid is not None else os.path.dirname(os.path.dirname(self.workdir))
        # filename = dir + 'input.csv'
        memresultfile = filename
        df = pd.read_csv(filename, header=0, sep=',', skipinitialspace=True)
        df[columnname][len(df.index) - 1] = maxmem
        df.to_csv(memresultfile, sep=',', index=False)




    @staticmethod
    def FindfittedModel(id, path):
        """

            Parser the header file to find all fitted model

        :param emdid:
        :return:
        """

        import xml.etree.ElementTree as ET
        headerfile = '{}/emd-{}.xml'.format(path, id)
        headerdict = {}
        if os.path.isfile(headerfile):
            tree = ET.parse(headerfile)
            root = tree.getroot()

            # Fitted models
            deposition = root.find('deposition')
            title = deposition.find('title').text
            fitlist = deposition.find('fittedPDBEntryIdList')
            fitmodel = []
            modelcount = 0
            fitpid = []
            if fitlist is not None:
                for child in fitlist.iter('fittedPDBEntryId'):
                    fitmodel.append(child.text + '.cif')
                    fitpid.append(child.text)


            # check when there is fitted models for tomography data, do not count the fitted model
            # for calculating atom inclusion, residue inclusion or map model view
            processing = root.find('processing')
            method = processing.find('method').text
            headerdict['fitmodels'] = None if method == 'tomography' else fitmodel

            # Recommended contour level
            map = root.find('map')
            contourtf = map.find('contourLevel')
            reccl = None
            if contourtf is not None:
                reccl = "{0:.6f}".format(float(map.find('contourLevel').text))


            headerdict['fitmodels'] = fitmodel
            headerdict['fitpid'] = fitpid
            headerdict['reccl'] = reccl

            return headerdict


    @staticmethod
    def notimediff(srcfile, desfile):
        """

            compare the time diff between two files

        :param file: file to be checked
        :return: True: older file False: newly created file
        """
        if int(os.path.getmtime(srcfile)) == int(os.path.getmtime(desfile)):
            return True
        else:
            return False

    def copyfiles_todisplay(self):
        """

            copy all json and image files to the folder which will be used for display purpose

        :param self:
        :return:
        """

        srcdir = '{}{}/va'.format(MAP_SERVER_PATH, list(self.idsubdirs.values())[0])
        desdir = '{}{}/va'.format(FORDISPLAY,  list(self.idsubdirs.values())[0])
        try:
            os.makedirs(desdir)
        except OSError:
            if not os.path.isdir(desdir):
                raise

        if os.path.isdir(desdir):
            rmtree(desdir)
        copytree(srcdir, desdir, ignore=ignore_patterns('*.map', '*.gz'))
        # desfiles = os.listdir(desdir)
        # for file in os.listdir(srcdir):
        #
        #     src = '{}/{}'.format(srcdir, file)
        #     des = '{}/{}'.format(desdir, file)



            # if file.endswith(('.json', '.jpeg', '.png', '.ent', '.cif', '.map', '.vtp', '.xml')) and (file not in desfiles or self.notimediff(src, des) is False):
            #     copy2(src, desdir)
            # if os.path.isdir(src):
            #     if os.path.isdir(des):
            #         rmtree(des)
            #     dest = move(src, des)


def main():

    myobj = prepareandrun()
    myobj.runcmd()
    myobj.copyfiles_todisplay()

if __name__ == '__main__':
    main()
    # datafile = MAP_SERVER_PATH + 'input.csv'
    # prepareandrun.savepeakmemory(datafile, mem)
    # print 'Memory usage peak: %s.' % mem
