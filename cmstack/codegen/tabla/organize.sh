#!/bin/bash

if [[ ! $# -eq 2 ]]; then
    echo 'usage: organize.sh <benchmark name> <model size>'
    exit 1
fi

bench=$1
model=$2

FOLDER=${bench}-${model}
MV_DIR=../fpga/hw-imp/include/instructions/${FOLDER}
CONFIG_DIR=../fpga/hw-imp/config/
CP_DIR=hw-imp/include/instructions/${FOLDER}

dotfile=${bench}_${model}.jpeg
dotfile_peid=${bench}_${model}_peid.jpeg
dot -Tjpeg -o ${dotfile} ./artifacts/tabla.dot
dot -Tjpeg -o ${dotfile_peid} ./artifacts/tabla_peid.dot

echo "" >> config.list
echo MEM_INST_INIT \"${CP_DIR}/mem-inst/memInst.txt\" >> config.list
echo COMPUTE_INST_INIT \"${CP_DIR}/compute-inst/\" >> config.list
echo META_DATA_FILE \"${CP_DIR}/meta.txt\" >> config.list
echo WEIGHT_CTRL_INIT \"${CP_DIR}/mem-inst/weightInst.txt\" >> config.list


if [ -d "binary" ]; then
    rm -rf binary/
fi

mkdir binary/
mkdir binary/mem-inst/

mv meminst.json meminst.txt weightInst.txt binary/mem-inst/
mv bin/ binary/bin-inst/
mv inst/ binary/json-inst/
mv hex/ binary/hex-inst/
mv artifacts/ binary/
mv config.list binary/
mv inst_info.txt binary/
mv ${dotfile} ${dotfile_peid} binary/

if [ ! -d "$MV_DIR" ]; then
    mkdir ${MV_DIR}
    mkdir ${MV_DIR}/compute-inst/
    mkdir ${MV_DIR}/mem-inst/
    mkdir ${MV_DIR}/json/
fi

cp binary/mem-inst/{meminst.txt,weightInst.txt} ${MV_DIR}/mem-inst/
cp binary/bin-inst/* ${MV_DIR}/compute-inst/

cp binary/json-inst/* ${MV_DIR}/json/
cp binary/${dotfile} binary/${dotfile_peid} ${MV_DIR}/
cp binary/config.list ${CONFIG_DIR}/
