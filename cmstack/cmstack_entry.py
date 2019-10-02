from __future__ import absolute_import
import argparse
import os
from typing import Text
import sys

project_root = os.getcwd().rsplit("/", 1)[0]
sys.path.insert(0, project_root)

from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from cmstack.axelvm.ir import AxelVM
from cmstack.cmlang.antlr_generator.lexer import CMLangLexer
from cmstack.cmlang.antlr_generator.parser import CMLangParser
from cmstack.cmlang.symbols import CMLangListener
from cmstack.hdfg import load_store
from cmstack.hdfg import visualize
from cmstack.hdfg.onnx_hdfg.onnx_cmstack import ONNXCMStack
from cmstack.codegen.loopygen.generator import LoopyGen
from cmstack.codegen.tabla.tabla_translate import TablaTranslation
from cmstack.codegen.tvmgen.tvm_translation import TvmTranslation
from cmstack.codegen.translator import Translator


def serialize_cmlang(cmlang_file, output_cmstack, viz=False):
    input_file = FileStream(cmlang_file)
    lexer = CMLangLexer(input_file)
    stream = CommonTokenStream(lexer)
    parser = CMLangParser(stream)
    tree = parser.cmlang()

    cmlang_graph = CMLangListener(cmlang_file, output_cmstack)
    walker = ParseTreeWalker()
    walker.walk(cmlang_graph, tree)
    output_dir, output_file = os.path.split(cmlang_file)

    outputfile = output_dir + '/' + output_file[:-3] + '.pb'

    load_store.save_program(cmlang_graph.program, outputfile)


def generate_axelvm(input_cmstack,output_axelvm, viz=False):
    avm = AxelVM(input_cmstack)
    avm.generate_axelvm()

def serialize_onnx(input_proto, output_cmstack, viz=False):
    converter = ONNXCMStack(input_proto)
    converter.run()

def visualize_graph(fname):
    visualize.visualize_program(fname, rankdir='TB')

def genccode(input_proto):
    code = LoopyGen(input_proto)

def gentabla(input_proto):
    code = TablaTranslation(input_proto)

def translate(input_proto, config):
    import sys
    code = Translator(input_proto, config, ['map_nodes', 'flatten'])

def main():
    parser = argparse.ArgumentParser(description="CMStack compilation framework")
    parser.add_argument("action",
                        type=Text,
                        help="One of the following: 'cmlang', 'onnx', or 'axelvm' which generates a"
                             " serialized CMstack graph from either "
                             "a CMLang file or an ONNX protobuf file, or generates axelvm "
                             "code from a CMStack file.",
                        choices=["cmlang", "onnx", "axelvm", "visualize", "c", "tabla", "translate"])
    parser.add_argument("--input",
                        type=Text, required=True,
                        help="The input cmlang, onnx protobuf, or cmstack protobuf file")
    parser.add_argument("--tconfig",
                        type=Text, required=False,
                        help="The configuration file for translation")

    parser.add_argument("--output",
                            type=Text, required=False,
                            help="The output cmstack protobuf filename or "
                                 "axelvm filename")

    args = parser.parse_args()

    if args.action == 'cmlang':
        serialize_cmlang(args.input, args.output)
    elif args.action == 'onnx':
        serialize_onnx(args.input, args.output)
    elif args.action == 'axelvm':
        generate_axelvm(args.input, args.output)
    elif args.action == 'visualize':
        visualize_graph(args.input)
    elif args.action == 'c':
        genccode(args.input)
    elif args.action == 'tabla':
        gentabla(args.input)
    elif args.action == 'translate':
        translate(args.input, args.tconfig)


if __name__ == '__main__':
    main()