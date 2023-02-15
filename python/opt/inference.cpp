// This script loads a TorchScript model and runs inference on a given input.

#include <torch/script.h> // One-stop header.

#include <iostream>
#include <vector>

// It's difficult to read json files in C++, so we'll use hard-coded input
// {"instances": [{"input_ids": [2, 25216, 47, 236, 16], "attention_mask": [1, 1, 1, 1, 1]}]}

int main(int argc, const char* argv[]) {
  if (argc != 2) {
    std::cerr << "usage: inference <model_path>" << std::endl;
    return -1;
  }

  // Deserialize the ScriptModule from a file using torch::jit::load().
  torch::jit::script::Module module = torch::jit::load(argv[1]);

  // Create a vector of inputs.
  // input_ids = [2, 25216, 47, 236, 16]
  // attention_mask = [1, 1, 1, 1, 1]
  std::vector<torch::jit::IValue> inputs;
  inputs.push_back(torch::tensor({2, 25216, 47, 236, 16}).reshape({1, 5}));
  inputs.push_back(torch::tensor({1, 1, 1, 1, 1}).reshape({1, 5}));

  // Execute the model and turn its output into a tensor.
  torch::jit::IValue output = module.forward(inputs);

  // Print the output.
  std::cout << output << std::endl;

  return 0;
}