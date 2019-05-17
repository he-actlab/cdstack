#!/bin/bash

OUT_FILENAME=out.jpeg
DOT_FILENAME=dottest.dot

dot -T jpeg -o ${OUT_FILENAME} ${DOT_FILENAME}
open ${OUT_FILENAME}
