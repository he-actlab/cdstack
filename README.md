# Welcome to CMStack!

CMStack is a high-level language and compiler which produces an IR for translation to hetereogenous hardware.

### COMPILER

### Dependencies  
If you would like to generate the lexer and parser, please refer to the "To generate lexer and parser directly" section below. Otherwise, you only need Python 3.4.3 or higher, in order to successfully run the compiler. If you would like to view the graphical representations of the compiler-generated dataflow graphs, Graphviz - graph visualization software - is needed. Please refer to the respective online resources in order to install them on your environment.

In addition, code generation depends on [loopy](https://github.com/inducer/loopy) as a submodule. After cloning this repository, you will need to run the following commands in order to install loopy:

1. git submodule update --init --recursive
2. cd loopy/
3. pip3 install -r requirements.txt --user
4. python3 setup.py install --user

If you run into any issues installing loopy, refer to their documentation [here](https://documen.tician.de/loopy/misc.html#option-1-from-source-no-pyopencl-integration)


### How to invoke the compiler to produce protobuf files  
To run the compiler on cdlang code, run the following command:

```
$ python3 cmstack/cmstack_entry.py cmlang --input <path/to/cdlang/file.cm>
```

To run the compiler using an onnx protobuf file as input, run the following command:

```
$ python3 cmstack/cmstack_entry.py onnx --input <path/to/onnx/model.onnx>
```

Both of these commands generate a protobuf intermediate representation of the rDFG.

### How to generate c code using the rDFG

In order to generate C code using the rDFG, you can run the following command:

```
$ python3 cmstack/cmstack_entry.py c --input <path/to/rdfg.pb> > <cfilename>.c
```


### Developers

This compiler was developed by Sean Kinzer, a PhD student at UC San Diego. For any inquiries, please contact skinzer@eng.ucsd.edu.
