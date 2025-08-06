# TerraRecon Models Directory

This directory contains pre-trained AI model files used for person detection in the TerraRecon project.

## Files
- **dnn_prototxt.txt**: Defines the neural network architecture (e.g., MobileNet-SSD or YOLO) in Caffe format. Used by `vision_processing.py` for person detection.
- **dnn_caffemodel.caffemodel**: Contains the trained weights for the neural network, paired with `dnn_prototxt.txt`.

## Obtaining Model Files
The project document does not include the actual contents of these files. To use TerraRecon:
1. Download a compatible pre-trained model, such as MobileNet-SSD, from a trusted source:
   - Example: [OpenCV DNN testdata](https://github.com/opencv/opencv_extra/tree/master/testdata/dnn)
   - Recommended files: `MobileNetSSD_deploy.prototxt` and `MobileNetSSD_deploy.caffemodel`
2. Rename the files to `dnn_prototxt.txt` and `dnn_caffemodel.caffemodel`, respectively.
3. Place them in the `models/` directory.
4. Ensure the file paths in `src/config.py` match these filenames.

## Usage
The models are loaded in `src/vision_processing.py` using OpenCV's DNN module:
```python
person_net = cv2.dnn.readNetFromCaffe(DNN_MODEL_PROTOTXT, DNN_MODEL_CAFFEMODEL)
```
These models enable real-time person detection, which is combined with face recognition for threat identification.

## Notes
- Ensure the `.prototxt` and `.caffemodel` files correspond to the same model architecture.
- The models must be compatible with OpenCV's DNN module and the Caffe framework.
- Update `src/config.py` if using different model filenames.