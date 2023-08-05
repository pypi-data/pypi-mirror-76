# Symmetry detection with Proshade

import sys
import os
# Include complied proshade library, which have need to be changed to automatic check location from CCPEM(TODO)
proshadePath = '/usr/local/share/ProSHADE_0.6.6_stable/build/python'
import proshade
sys.path.append( proshadePath )

# Define ProSHADE vector parsing functions
def parseDVecFromProshade (cSyms):
    vecIt = 0
    myAxis = []
    myAxes = []
    while True:
        if vecIt == len(cSyms):
            break
        if cSyms[vecIt] == -999.999:
            myAxes.append(myAxis)
            myAxis = []
            vecIt = vecIt + 1
        else:
            myAxis.append(cSyms[vecIt])
            vecIt = vecIt + 1
    return myAxes

def parseDVecDVecFromProshade (dSym):
    vecIt = 0
    myAxis = []
    myAxes = []
    mySymmetry = []
    while True:
        if vecIt == len(dSym):
            break
        if dSym[vecIt] == -999.999:
            myAxes.append(myAxis)
            myAxis = []
            vecIt  = vecIt + 1
        elif dSym[vecIt] == -777.777:
            mySymmetry.append(myAxes)
            myAxes = []
            myAxis = []
            vecIt = vecIt + 1
        else:
            myAxis.append(dSym[vecIt])
            vecIt = vecIt + 1
    return mySymmetry

# Get the settings object
setUp = proshade.ProSHADE_settings()

# Settings setup

# Settings regarding resolutions
# TODO: Read in resolution and set the resolution to 4(to be discussed) for higher than 4 angstram maps
setUp.mapResolution = 8.0
setUp.bandwidth = 0
setUp.glIntegOrder = 0
setUp.theta = 0
setUp.phi = 0

# Settings regarding B factors
setUp.bFactorValue = 80.0
setUp.bFactorChange = 0.0

# Setting regarding maps and removing noise
setUp.noIQRsFromMap = 4.0

# Settings regarding concentric shells
setUp.shellSpacing = 0.0
setUp.manualShells = 0

# Settings regarding map with phases
setUp.useCOM = True
setUp.maskBlurFactor = 500.0
setUp.maskBlurFactorGiven = False

#  Settings regarding space around the structure in lattice
setUp.extraSpace = 8.0

#  Settings regarding peak detection
setUp.peakHeightNoIQRs = 3.0
setUp.peakDistanceForReal = 0.30
setUp.peakSurroundingPoints = 1

# Settings regarding tolerances
setUp.aaErrorTolerance = 0.1
setUp.symGapTolerance = 0.3

# Settings regarding the task
setUp.taskToPerform = proshade.Symmetry

# Settings regarding the symmetry type required
setUp.symmetryFold = 0
setUp.symmetryType = ""

# Settings regarding loudness
setUp.verbose = -1

# Get command line info
if len(sys.argv) < 2:
    print ( 'Usage: python getSymmetry.py [filename1] to get symmetry information for structure in [filename1].')
    sys.exit()
else:
    hlpPyStrVec = proshade.StringList(len(sys.argv)-1)
    hlpPyStrVec[0] = str(sys.argv[1])
    # Set the file list
    setUp.structFiles = hlpPyStrVec


# Now run proshade
runProshade = proshade.ProSHADE(setUp)

# Get the results
cyclicSymmetries = runProshade.getCyclicSymmetriesPy()
dihedralSymmetries = runProshade.getDihedralSymmetriesPy()
tetrahedralSymmetries = runProshade.getTetrahedralSymmetriesPy()
octahedralSymmetries = runProshade.getOctahedralSymmetriesPy()
icosahedralSymmetries = runProshade.getIcosahedralSymmetriesPy()
symElemsRecommended = runProshade.getSymmetryElementsPy()
symElemsRequested = runProshade.getSpecificSymmetryElementsPy("C", 4)

print symElemsRecommended
print symElemsRequested


# Printing them
sys.stdout.write('ProSHADE module version: ' + runProshade.getProSHADEVersion() + '\n')
sys.stdout.write('\n')
sys.stdout.flush()

# Cyclic symmetries
sys.stdout.write('Cyclic symmetry axes detected:\n')
sys.stdout.write('-----------------------------------------------------------\n')
sys.stdout.write('Symmetry Fold     x       y       z      Angle      Peak   \n')
sys.stdout.write('  Type                                   (rad)      height \n')
sys.stdout.write('-----------------------------------------------------------\n')

myAxes = parseDVecFromProshade(cyclicSymmetries)
for it in xrange(0, len(myAxes)):
    sys.stdout.write('   C       %d    %+1.3f  %+1.3f  %+1.3f   %+1.3f    %+1.3f' % (myAxes[it][0], myAxes[it][1], myAxes[it][2], myAxes[it][3], 6.282/myAxes[it][0], myAxes[it][4]) + '\n')
sys.stdout.write('\n')
sys.stdout.flush()

# Dihedral symmetries
sys.stdout.write('Dihedral symmetry axes detected:\n')
sys.stdout.write('-----------------------------------------------------------\n')
sys.stdout.write('Symmetry Fold     x       y       z      Angle      Peak   \n')
sys.stdout.write('  Type                                   (rad)      height \n')
sys.stdout.write('-----------------------------------------------------------\n')

mySymmetry = parseDVecDVecFromProshade(dihedralSymmetries)
for sym in xrange(0, len(mySymmetry)):
    myAxes = mySymmetry[sym]
    sys.stdout.write('   D       %d    %+1.3f  %+1.3f  %+1.3f   %+1.3f    %+1.3f' % (myAxes[0][0], myAxes[0][1], myAxes[0][2], myAxes[0][3], 6.282/myAxes[0][0], myAxes[0][4]) + '\n')
    for subAx in xrange(1, len(mySymmetry[sym])):
        sys.stdout.write('           %d    %+1.3f  %+1.3f  %+1.3f   %+1.3f    %+1.3f' % (myAxes[subAx][0], myAxes[subAx][1], myAxes[subAx][2], myAxes[subAx][3], 6.282/myAxes[subAx][0], myAxes[subAx][4]) + '\n')
sys.stdout.write('\n')
sys.stdout.flush()

# Tetrahedral symmetries
sys.stdout.write('Tetrahedral symmetry axes detected:\n')
sys.stdout.write('-----------------------------------------------------------\n')
sys.stdout.write('Symmetry Fold     x       y       z      Angle      Peak   \n')
sys.stdout.write('  Type                                   (rad)      height \n')
sys.stdout.write('-----------------------------------------------------------\n')

myAxes = parseDVecFromProshade(tetrahedralSymmetries)
for it in xrange(0, len(myAxes)):
    sys.stdout.write('   T       %d    %+1.3f  %+1.3f  %+1.3f   %+1.3f    %+1.3f' % (myAxes[it][0], myAxes[it][1], myAxes[it][2], myAxes[it][3], 6.282/myAxes[it][0], myAxes[it][4]) + '\n')
sys.stdout.write('\n')
sys.stdout.flush()

# Octahedral symmetries
sys.stdout.write('Octahedral symmetry axes detected:\n')
sys.stdout.write('-----------------------------------------------------------\n')
sys.stdout.write('Symmetry Fold     x       y       z      Angle      Peak   \n')
sys.stdout.write('  Type                                   (rad)      height \n')
sys.stdout.write('-----------------------------------------------------------\n')

myAxes = parseDVecFromProshade(octahedralSymmetries)
for it in xrange(0, len(myAxes)):
    sys.stdout.write('   O       %d    %+1.3f  %+1.3f  %+1.3f   %+1.3f    %+1.3f' % (myAxes[it][0], myAxes[it][1], myAxes[it][2], myAxes[it][3], 6.282/myAxes[it][0], myAxes[it][4]) + '\n')
sys.stdout.write('\n')
sys.stdout.flush()

# Icosahedral symmetries
sys.stdout.write('Icosahedral symmetry axes detected:\n')
sys.stdout.write('-----------------------------------------------------------\n')
sys.stdout.write('Symmetry Fold     x       y       z      Angle      Peak   \n')
sys.stdout.write('  Type                                   (rad)      height \n')
sys.stdout.write('-----------------------------------------------------------\n')

myAxes = parseDVecFromProshade(icosahedralSymmetries)
for it in xrange(0, len(myAxes)):
    sys.stdout.write('   I       %d    %+1.3f  %+1.3f  %+1.3f   %+1.3f    %+1.3f' % (myAxes[it][0], myAxes[it][1], myAxes[it][2], myAxes[it][3], 6.282/myAxes[it][0], myAxes[it][4]) + '\n')
sys.stdout.write('\n')
sys.stdout.flush()

# Recommended (simple highest peak approach, this will be improved in the future, do not take the work 'recommended' too seriously) symmetry elements
sys.stdout.write('Recommended symmetry elements table:                       \n')
sys.stdout.write('-----------------------------------------------------------\n')
sys.stdout.write('Symmetry          x          y          z          Angle   \n')
sys.stdout.write('  Type                                             (rad)   \n')
sys.stdout.write('-----------------------------------------------------------\n')

myElems = parseDVecFromProshade(symElemsRecommended)
if len(myElems) > 0:
    sys.stdout.write('   E           %+1.3f     %+1.3f     %+1.3f       %+1.3f' % (myElems[0][1], myElems[0][2], myElems[0][3], myElems[0][4]) + '\n')
    for elem in xrange(1, len(myElems)):
        sys.stdout.write('   C%d          %+1.3f     %+1.3f     %+1.3f       %+1.3f' % (myElems[elem][0], myElems[elem][1], myElems[elem][2], myElems[elem][3], myElems[elem][4]) + '\n')
sys.stdout.write('\n')
sys.stdout.flush()

# Requested symmetry elements
sys.stdout.write('Requested symmetry elements table:                       \n')
sys.stdout.write('-----------------------------------------------------------\n')
sys.stdout.write('Symmetry          x          y          z          Angle   \n')
sys.stdout.write('  Type                                             (rad)   \n')
sys.stdout.write('-----------------------------------------------------------\n')

myElems = parseDVecFromProshade(symElemsRequested)
if len(myElems) > 0:
    sys.stdout.write('   E           %+1.3f     %+1.3f     %+1.3f       %+1.3f' % (myElems[0][1], myElems[0][2], myElems[0][3], myElems[0][4]) + '\n')
    for elem in xrange(1, len(myElems)):
        sys.stdout.write('   C%d          %+1.3f     %+1.3f     %+1.3f       %+1.3f' % ( myElems[elem][0], myElems[elem][1], myElems[elem][2], myElems[elem][3], myElems[elem][4]) + '\n')
sys.stdout.write('\n')
sys.stdout.flush()


