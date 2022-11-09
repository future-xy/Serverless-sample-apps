# This file creates a TensorRT engine from a BERT ONNX model
# and runs inference on a sample input.

import tensorrt as trt

print(trt.__version__)

TRT_LOGGER = trt.Logger(trt.Logger.WARNING)

MODEL_PATH = "bert-pt-onnx/model_int32.onnx"
ENGINE_PATH = "bert-pt-onnx/model_int32.trt"

# Load the ONNX model
EXPLICIT_BATCH = 1 << (int)(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
with trt.Builder(TRT_LOGGER) as builder, builder.create_network(EXPLICIT_BATCH) as network, trt.OnnxParser(network, TRT_LOGGER) as parser:
    success = parser.parse_from_file(MODEL_PATH)
    for error in range(parser.num_errors):
        print(parser.get_error(error))
    assert success

    # set input shape as (1, 11)
    network.get_input(0).shape = (1, 11)
    network.get_input(1).shape = (1, 11)
    network.get_input(2).shape = (1, 11)
    # network.set_input

    # Build the TensorRT engine
    config = builder.create_builder_config()
    config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 1 << 28)
    serialized_engine = builder.build_serialized_network(network, config)
    with open(ENGINE_PATH, "wb") as f:
        f.write(serialized_engine)