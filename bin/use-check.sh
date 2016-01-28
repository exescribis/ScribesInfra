# Check a scenario or a state against the model.
# Should be executed in the directory containing the .use file
# Examples:
#     use-check scenario CyberGarage Scn001Alicia
#     use-check state CyberGarage State003Feb12 -q
#

SOILKIND=$1
CASE_STUDY=$2
SOIL=$3
OPTIONS=$4

echo quit | use -nogui -nr ${CASE_STUDY}.use $OPTION ${SOILKIND?}/${CASE_STUDY}${SOIL}.soil

