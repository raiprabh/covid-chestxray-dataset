import pydicom
import matplotlib.pyplot as plt

dataset = pydicom.dcmread('./c64d5667-a776-4f95-9e21-bfabafb07740.dcm')

print(dataset.pixel_array.shape)