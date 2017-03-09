import sys
import os.path
import sqlrst

inputFile = sys.argv[1]
outputFile = sys.argv[2]
if not os.path.isfile(inputFile):
    print('No such file : %s' % inputFile)
    exit(1)
sqlrst.sqlRstFile2RstFile(sys.argv[1], sys.argv[2])