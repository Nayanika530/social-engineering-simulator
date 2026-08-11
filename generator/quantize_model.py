from optimum.onnxruntime import ORTModelForCausalLM
from optimum.onnxruntime.configuration import AutoQuantizationConfig
from optimum.onnxruntime import ORTQuantizer
from transformers import AutoTokenizer
print("Loading and converting model to ONNX...")
model = ORTModelForCausalLM.from_pretrained("models/generator/final", export=True)
tokenizer = AutoTokenizer.from_pretrained("models/generator/final")
model.save_pretrained("models/generator_onnx")
tokenizer.save_pretrained("models/generator_onnx")
print("ONNX conversion done, saved to models/generator_onnx")
print("\nQuantizing to INT8...")
quantizer = ORTQuantizer.from_pretrained("models/generator_onnx")
qconfig = AutoQuantizationConfig.avx512_vnni(is_static=False, per_channel=False)
quantizer.quantize(save_dir="models/generator_quantized", quantization_config=qconfig)
print("Quantization done, saved to models/generator_quantized")
