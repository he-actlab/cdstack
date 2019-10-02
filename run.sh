#!/usr/bin/env bash
#python3 cmstack_entry.py visualize --input test/examples/test_example.pb

#python3  cmstack_entry.py cmlang --input test/examples/test_example.cm
#python3 cmstack_entry.py c --input test/examples/test_example.pb
#python3 cmstack_entry.py tabla --input test/examples/test_example.pb
#make clean -C test/examples/test_example_ccode/
#make -C test/examples/test_example_ccode/

#python3 cmstack_entry.py onnx --input test/onnx_examples/mnist/model.onnx
#python3 cmstack_entry.py visualize --input test/onnx_examples/mnist/model.pb

##### TABLA HW TESTS ###################
#python3 cmstack_entry.py cmlang --input test/examples/test_example.cm
#python3 cmstack_entry.py axelvm --input test/examples/test_example.pb

#python3 cmstack_entry.py cmlang --input test/tabla_benchmarks/linear_regression/linear.cm
#python3 cmstack_entry.py c --input test/tabla_benchmarks/linear_regression/linear.pb


#python3 cmstack_entry.py tabla --input test/tabla_benchmarks/linear_regression/linear.pb
#make clean -C test/tabla_benchmarks/linear_regression/linear_ccode/
#make -C test/tabla_benchmarks/linear_regression/linear_ccode/

#python3 cmstack_entry.py cmlang --input test/tabla_benchmarks/recommender/recommender.cm
#python3 cmstack_entry.py visualize --input test/tabla_benchmarks/recommender/recommender.pb
#python3 cmstack_entry.py c --input test/tabla_benchmarks/recommender/recommender.pb
#python3 cmstack_entry.py tabla --input test/tabla_benchmarks/recommender/recommender.pb

#python3 cmstack_entry.py cmlang --input test/tabla_benchmarks/classification/classification.cm
#python3 cmstack_entry.py c --input test/tabla_benchmarks/classification/classification.pb
#python3 cmstack_entry.py tabla --input test/tabla_benchmarks/classification/classification.pb

#python3 cmstack_entry.py cmlang --input test/examples/kmeans_paper.cm
#python3 cmstack_entry.py visualize --input test/examples/test_example.pb
#python3 cmstack_entry.py c --input test/examples/kmeans_paper.pb
#make clean -C test/examples/test_example_ccode/
#make -C test/examples/test_example_ccode/

##### TVM HW TESTS ###################

#python3 cmstack_entry.py cmlang --input test/tvm_benchmarks/lenet/lenet.cm
#python3 cmstack_entry.py c --input test/tvm_benchmarks/lenet/lenet.pb
#python3 cmstack_entry.py translate --input test/tvm_benchmarks/lenet/lenet.pb --tconfig codegen/tvmgen/tvm_config.json


#python3 cmstack_entry.py cmlang --input test/tvm_benchmarks/resnet18/resnet18.cm
#python3 cmstack_entry.py translate --input test/tvm_benchmarks/resnet18/resnet18.pb --tconfig codegen/tvmgen/tvm_config.json

#python3 cmstack_entry.py cmlang --input test/tvm_benchmarks/yolodnn/yolodnn.cm
#python3 cmstack_entry.py c --input test/tvm_benchmarks/yolodnn/yolodnn.pb
#python3 cmstack_entry.py tvm --input test/tvm_benchmarks/yolodnn/yolodnn.pb

#python3 cmstack_entry.py cmlang --input test/tvm_benchmarks/yolodnn/yolodnn.cm
#python3 cmstack_entry.py translate --input test/tvm_benchmarks/yolodnn/yolodnn.pb --tconfig codegen/tvmgen/tvm_config.json


#python3 cmstack_entry.py cmlang --input test/tvm_benchmarks/yolodnn/yolodnn_dnnweaver.cm
#python3 cmstack_entry.py translate --input test/tvm_benchmarks/yolodnn/yolodnn_dnnweaver.pb --tconfig codegen/dnnweavergen/dnnweaver_config.json
#python3 cmstack_entry.py axelvm --input test/tvm_benchmarks/yolodnn/yolodnn_dnnweaver.pb



### Code Gen Tests #########

python3 cmstack_entry.py cmlang --input test/tabla_benchmarks/linear_regression/linear_test.cm
python3 cmstack_entry.py c --input test/tabla_benchmarks/linear_regression/linear_test.pb


#python3 cmstack_entry.py cmlang --input test/tvm_benchmarks/lenet/lenet.cm
#python3 cmstack_entry.py c --input test/tvm_benchmarks/lenet/lenet.pb