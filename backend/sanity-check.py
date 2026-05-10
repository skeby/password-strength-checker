# run this in the backend/ directory
import onnxruntime as ort
import numpy as np

session = ort.InferenceSession("../frontend/public/model/password-model.onnx")
input_name = session.get_inputs()[0].name

# dummy feature vector — 16 zeros
dummy = np.zeros((1, 16), dtype=np.float32)
result = session.run(None, {input_name: dummy})
print("Output:", result)   # should print a number, not crash