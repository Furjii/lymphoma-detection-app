import numpy as np
import tensorflow as tf
from PIL import Image
import os

class LymphomaDetector:
    def __init__(self, model_path='model/model0.h5', labels=None):
        """
        Initialize the Lymphoma Detector.
        
        Args:
            model_path (str): Path to the H5 model file
            labels (list): List of class labels
        """
        self.labels = labels if labels is not None else ['CLL', 'FL', 'MCL']
        
        try:
            # Fix for layer names containing '/' character
            self._fix_layer_names()
            
            # Load the Keras model
            self.model = tf.keras.models.load_model(model_path)
            print(f"Model loaded from: {model_path}")
            print(f"Model input shape: {self.model.input_shape}")
            print(f"Model output shape: {self.model.output_shape}")
        except Exception as e:
            print(f"Error loading model from {model_path}: {e}")
            # Try alternative loading method
            try:
                print("Trying alternative loading method...")
                self.model = self._load_model_alternative(model_path)
                print(f"Model loaded successfully using alternative method")
                print(f"Model input shape: {self.model.input_shape}")
                print(f"Model output shape: {self.model.output_shape}")
            except Exception as e2:
                print(f"Alternative loading also failed: {e2}")
                raise

    def _fix_layer_names(self):
        """Fix layer names that contain '/' character"""
        import keras.layers
        
        # Store original __init__ method
        if not hasattr(keras.layers.Layer, '_original_init'):
            keras.layers.Layer._original_init = keras.layers.Layer.__init__
            
            def patched_init(self, *args, **kwargs):
                if 'name' in kwargs and isinstance(kwargs['name'], str) and '/' in kwargs['name']:
                    kwargs['name'] = kwargs['name'].replace('/', '_')
                return keras.layers.Layer._original_init(self, *args, **kwargs)
            
            keras.layers.Layer.__init__ = patched_init

    def _load_model_alternative(self, model_path):
        """Alternative method to load model with custom objects"""
        try:
            # Try loading with compile=False
            model = tf.keras.models.load_model(model_path, compile=False)
            return model
        except Exception as e:
            print(f"Compile=False method failed: {e}")
            
            # Try with custom objects
            custom_objects = {}
            model = tf.keras.models.load_model(model_path, custom_objects=custom_objects, compile=False)
            return model

    def preprocess_image(self, image_path):
        """
        Preprocess the image for the model.
        
        Args:
            image_path (str): Path to the input image
            
        Returns:
            np.ndarray: Preprocessed image array
        """
        try:
            # Open the image (supports TIFF format as well)
            img = Image.open(image_path).convert('RGB')
            
            # Resize the image to the input shape of the model (get from model input)
            input_shape = self.model.input_shape
            target_size = (input_shape[1], input_shape[2]) if input_shape[1] is not None else (224, 224)
            img = img.resize(target_size)
            
            # Convert the image to a numpy array
            img_array = np.array(img).astype(np.float32)
            
            # Normalize the image (to [0, 1])
            img_array = img_array / 255.0
            
            # Add batch dimension (for batch processing compatibility)
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
        except Exception as e:
            print(f"Error preprocessing image {image_path}: {e}")
            raise

    def predict(self, image_path):
        """
        Perform inference on an image.
        
        Args:
            image_path (str): Path to the input image
            
        Returns:
            tuple: (predicted_label, confidence_percentage)
        """
        try:
            # Preprocess the image
            input_data = self.preprocess_image(image_path)
            
            # Run inference with the model
            predictions = self.model.predict(input_data)
            
            # Get the prediction probabilities (batch size = 1)
            probabilities = predictions[0]
            
            # Get the predicted class index and confidence
            predicted_index = np.argmax(probabilities)
            confidence = probabilities[predicted_index]
            
            # Convert confidence to percentage and cap at 100%
            confidence_percentage = min(max(confidence * 100, 1), 100)
            
            # Format confidence to two decimal places
            confidence_percentage = round(confidence_percentage, 2)
            
            # Get the predicted label
            predicted_label = self.labels[predicted_index]
            
            return predicted_label, confidence_percentage
        except Exception as e:
            print(f"Error making prediction for image {image_path}: {e}")
            raise