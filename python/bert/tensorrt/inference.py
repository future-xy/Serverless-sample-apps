# This file creates a TensorRT engine from a BERT ONNX model
# and runs inference on a sample input.

import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit

import numpy as np
# import time

print(trt.__version__)

TRT_LOGGER = trt.Logger(trt.Logger.WARNING)

ENGINE_PATH = "bert-pt-onnx/model_int32.trt"

# [101, 8065, 2493, 2024, 2025, 2204, 2012, 2725, 103, 1012, 102]
input_ids = np.array([[101, 8065, 2493, 2024, 2025, 2204, 2012, 2725, 103, 1012, 102]])
attention_mask = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
token_type_ids = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

# Run inference with TensorRT on device 0
TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
with trt.Runtime(TRT_LOGGER) as runtime, open(ENGINE_PATH, "rb") as f, runtime.deserialize_cuda_engine(f.read()) as engine, engine.create_execution_context() as context:
    stream = cuda.Stream()
    # print(stream)   
    # inputs, outputs, bindings = allocate_buffers(engine)
    h_input_ids = cuda.register_host_memory(np.ascontiguousarray(input_ids.ravel(), dtype=np.int32))
    h_attention_mask = cuda.register_host_memory(np.ascontiguousarray(attention_mask.ravel(), dtype=np.int32))
    h_token_type_ids = cuda.register_host_memory(np.ascontiguousarray(token_type_ids.ravel(), dtype=np.int32))

    input_nbytes = h_input_ids.nbytes
    output_nbytes = trt.volume(engine.get_binding_shape(3)) * engine.max_batch_size * np.dtype(np.float32).itemsize

    # print("input_nbytes: ", input_nbytes)
    # print("output_nbytes: ", output_nbytes)

    d_input_ids = cuda.mem_alloc(input_nbytes)
    d_attention_mask = cuda.mem_alloc(input_nbytes)
    d_token_type_ids = cuda.mem_alloc(input_nbytes)
    d_output = cuda.mem_alloc(output_nbytes)
    h_output = cuda.pagelocked_empty(2, np.float32)

    bindings = [int(d_input_ids), int(d_attention_mask), int(d_token_type_ids), int(d_output)]

    cuda.memcpy_htod_async(d_input_ids, h_input_ids, stream)
    cuda.memcpy_htod_async(d_attention_mask, h_attention_mask, stream)
    cuda.memcpy_htod_async(d_token_type_ids, h_token_type_ids, stream)
    # Run inference.
    context.execute_async_v2(bindings=bindings, stream_handle=stream.handle)
    # time.sleep(10)
    # Synchronize the stream
    stream.synchronize()
    # Transfer predictions back from the GPU.
    cuda.memcpy_dtoh_async(h_output, d_output, stream)
    # Return only the host outputs.
    print(h_output)