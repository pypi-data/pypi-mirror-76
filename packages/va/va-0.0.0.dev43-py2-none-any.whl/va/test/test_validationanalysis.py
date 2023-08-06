#!/usr/bin/env python
"""

test_validationanalysis.py

Test that the validationanalysis is working
when the map, model, contour level and half maps are given

Copyright [2015] EMBL - European Bioinformatics Institute
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
__date__ = '2018-08-24'



import unittest
from TEMPy.MapParser import MapParser
from TEMPy.StructureParser import mmCIFParser
from va.validationanalysis import ValidationAnalysis
import json
import os
from va.test import TEST_DATA_PATH


class TestValidationAnalysis(unittest.TestCase):
    """

        Unittest class of ValidationAnalysis

    """


    def setUp(self):
        """

            Initialization of the test model. Test data examples are saved in text_data folder

        """
        unittest.TestCase.setUp(self)
        self.pid = None
        fullmodelname = TEST_DATA_PATH + '8117_5irx.cif'
        self.modelfile = mmCIFParser.read_mmCIF_file(self.pid, fullmodelname, hetatm=True)
        self.mapfile = MapParser.readMRC(TEST_DATA_PATH + '/emd_8117.map')
        self.hmeven = MapParser.readMRC(TEST_DATA_PATH + '/emd_8117_half_map_1.map')
        self.hmodd = MapParser.readMRC(TEST_DATA_PATH + '/emd_8117_half_map_2.map')
        self.cl = 3.5
        self.emdid = None
        self.outfolder = TEST_DATA_PATH + 'test_output/'
        self.method = 'singleParticle'
        self.resolution = 2.95
        self.vaobj = ValidationAnalysis(self.mapfile, self.modelfile, self.pid, self.hmeven, self.hmodd,
                                        self.cl, self.emdid, self.outfolder, self.method, self.resolution)



    def test_orthogonal_projections(self):
        """

            Test orthogonal projections if the generate test images identical to the reference images

        """

        self.vaobj.orthogonal_projections()
        xcomp = open(self.outfolder + 'emd_8117_xprojection.jpeg','rb').read() == open(TEST_DATA_PATH + 'emd_8117_xprojection.jpeg','rb').read()
        self.assertTrue(xcomp)
        ycomp = open(self.outfolder + 'emd_8117_yprojection.jpeg','rb').read() == open(TEST_DATA_PATH + 'emd_8117_yprojection.jpeg','rb').read()
        self.assertTrue(ycomp)
        zcomp = open(self.outfolder + 'emd_8117_zprojection.jpeg','rb').read() == open(TEST_DATA_PATH + 'emd_8117_zprojection.jpeg','rb').read()
        self.assertTrue(zcomp)



    def test_density_distribution(self):
        """

            Test density_distribution method. Check the existence of corresponding
            json file and if that match the reference

        """
        self.vaobj.density_distribution()

        filestatus = os.path.exists(self.outfolder + 'emd_8117_density_distribution.json')
        self.assertTrue(filestatus)

        with open(self.outfolder + 'emd_8117_density_distribution.json') as json_data:
            x = json.load(json_data)

        with open(TEST_DATA_PATH + 'emd_8117_density_distribution.json') as json_data:
            y = json.load(json_data)
        a, b = json.dumps(x, sort_keys=True), json.dumps(y, sort_keys=True)
        self.assertTrue(a == b)



    def test_atom_inclusion(self):
        """

            Test atom_inclusion method. Check if atom_inclusion.json and residue_inclusion.json
            exist and if they match to the references.

        """
        self.vaobj.atom_inclusion()
        atomfilestatus = os.path.exists(self.outfolder + '8117_5irx.cif_emd_8117_atom_inclusion.json')
        self.assertTrue(atomfilestatus)
        residuefilestatus = os.path.exists(self.outfolder + '8117_5irx.cif_emd_8117_residue_inclusion.json')
        self.assertTrue(residuefilestatus)

        # Check if atom_inclusion.json and residue_inclusion.json match the references
        with open(self.outfolder + '8117_5irx.cif_emd_8117_atom_inclusion.json') as json_data:
            x = json.load(json_data)

        with open(TEST_DATA_PATH + '8117_5irx.cif_emd_8117_atom_inclusion.json') as json_data:
            y = json.load(json_data)
        a, b = json.dumps(x, sort_keys=True), json.dumps(y, sort_keys=True)
        self.assertTrue(a == b)

        with open(self.outfolder + '8117_5irx.cif_emd_8117_residue_inclusion.json') as json_data:
            x = json.load(json_data)

        with open(TEST_DATA_PATH + '8117_5irx.cif_emd_8117_residue_inclusion.json') as json_data:
            y = json.load(json_data)
        a, b = json.dumps(x, sort_keys=True), json.dumps(y, sort_keys=True)
        self.assertTrue(a == b)



    def test_volumecontour(self):
        """

            Test volumecontour method

        """

        self.vaobj.volumecontour()
        volumefilestatus = os.path.exists(self.outfolder + 'emd_8117_volume_contour.json')
        self.assertTrue(volumefilestatus)

        with open(self.outfolder + 'emd_8117_volume_contour.json') as json_data:
            x = json.load(json_data)

        with open(TEST_DATA_PATH + 'emd_8117_volume_contour.json') as json_data:
            y = json.load(json_data)
        a, b = json.dumps(x, sort_keys=True), json.dumps(y, sort_keys=True)
        self.assertTrue(a == b)


    def test_central_slice(self):
        """

            Test central_slice method.

        """

        self.vaobj.central_slice()
        xcomp = open(self.outfolder + 'emd_8117_xcentral_slice.jpeg','rb').read() == open(TEST_DATA_PATH + 'emd_8117_xcentral_slice.jpeg','rb').read()
        self.assertTrue(xcomp)
        ycomp = open(self.outfolder + 'emd_8117_ycentral_slice.jpeg','rb').read() == open(TEST_DATA_PATH + 'emd_8117_ycentral_slice.jpeg','rb').read()
        self.assertTrue(ycomp)
        zcomp = open(self.outfolder + 'emd_8117_zcentral_slice.jpeg','rb').read() == open(TEST_DATA_PATH + 'emd_8117_zcentral_slice.jpeg','rb').read()
        self.assertTrue(zcomp)


    def test_raps(self):
        """

            Test raps method

        """
        self.vaobj.raps()
        rapsfilestatus = os.path.exists(self.outfolder + 'emd_8117_raps.json')
        self.assertTrue(rapsfilestatus)

        with open(self.outfolder + 'emd_8117_raps.json') as json_data:
            x = json.load(json_data)

        with open(TEST_DATA_PATH + 'emd_8117_raps.json') as json_data:
            y = json.load(json_data)
        a, b = json.dumps(x, sort_keys=True), json.dumps(y, sort_keys=True)
        self.assertTrue(a == b)

    def test_fsc(self):
        """

            Test fsc method

        """

        self.vaobj.fsc(self.hmeven, self.hmodd)
        xcomp = open(self.outfolder + 'emd_8117_fsc.png','rb').read() == open(TEST_DATA_PATH + 'emd_8117_fsc.png','rb').read()
        self.assertTrue(xcomp)

        with open(self.outfolder + 'emd_8117_fsc.json') as json_data:
            x = json.load(json_data)

        with open(TEST_DATA_PATH + 'emd_8117_fsc.json') as json_data:
            y = json.load(json_data)
        a, b = json.dumps(x, sort_keys=True), json.dumps(y, sort_keys=True)
        self.assertTrue(a == b)

    # Need to be changed and rewrite
    # def test_mempred(self):
    #     """
    #
    #         Test mempred method
    #
    #     """
    #
    #     test = ValidationAnalysis.mempred(self.outfolder + 'input.csv', 2000000)
    #     self.assertIsInstance(test, float)

if __name__ == '__main__':
    unittest.main()





