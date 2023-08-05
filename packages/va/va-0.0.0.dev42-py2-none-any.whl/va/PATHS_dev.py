"""
PATHS.py


PATHS is used to input and output directories of validation
analysis.

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
__date__ = '2018-07-24'


# General input
# #VAINPUT_DIR = '/Users/zhe/Downloads/testproj/8117_18M/'
# # Local test directory
# #VAINPUT_DIR = '/Users/zhe/Downloads/alltempmaps/'
# #VAOUTPUT_DIR = '/Users/zhe/Downloads/valocaltestresults/'
# VAINPUT_DIR = '/nfs/msd/work2/emdb/development/staging/em/'
# VAOUTPUT_DIR = '/nfs/msd/work2/emdb/development/staging/em/'
# #HEADER_PATH = '/nfs/ftp/pub/databases/emdb/structures/'
# HEADER_PATH = '/nfs/msd/work2/emdb/development/staging/em/'


# From database

# ENT file source path

ENTSOURCE = '/nfs/msd/work2/ftp/pdb/data/structures/all/pdb/'

# VTP file source path
VTPSOURCE = '/nfs/pdbe_staging/pdbe_data/development/staging/em/'

# CIF file source path
CIFSOURCE = '/nfs/msd/work2/ftp/pdb/data/structures/all/mmCIF/'

# MAP_SERVER_PATH = '/nfs/ftp/pub/databases/emdb/structures/'
MAP_SERVER_PATH = '/nfs/msd/work2/emdb/development/staging/em/'

# Chimera path
# CHIMERA = '/nfs/public/rw/pdbe/httpd-em/software/chimera_headless/bin/chimera'
CHIMERA = '/nfs/public/rw/pdbe/httpd-em/software/chimerax/opt/UCSF/ChimeraX/bin/ChimeraX'

# Original or old Chimera
OCHIMERA = '/nfs/msd/em/software/chimera2/bin/chimera'

# For ebi server to copy data for VA
# VASOURCE = '/nfs/msd/em/ftp_rsync/staging/structures/'
VASOURCE = '/nfs/msd/em/ftp_rsync/current/structures/'

# VAPATH
VAPATH = '/nfs/msd/em/software/ValidationAnalysis/Validation-Analysis/va/'

# Jsons and images are copied to here for display purpose
FORDISPLAY = '/nfs/nobackup/msd/em_va/development/'

# Proshade path
PROSHADEPATH = '/nfs/public/rw/pdbe/httpd-em/software/ccpem-1.4.1/bin/proshade'

# Meshmaker path
MESHMAKERPATH = '/nfs/msd/em/software/meshmakertest/meshmaker/build/meshmaker'


