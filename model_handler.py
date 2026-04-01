import tensorflow as tf
import numpy as np
import logging

class ModelHandler:
    def __init__(self, model_path="tf_model.h5"):
        self.model_path = model_path
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the TensorFlow model"""
        try:
            self.model = tf.keras.models.load_model(self.model_path)
            logging.info(f"Model loaded successfully from {self.model_path}")
            return True
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            return False
    
    def get_model_info(self):
        """Get model information"""
        if self.model is None:
            return {"status": "Model not loaded"}
        
        info = {
            "status": "Model loaded successfully",
            "input_shape": str(self.model.input_shape),
            "output_shape": str(self.model.output_shape),
            "layers": len(self.model.layers),
            "parameters": self.model.count_params()
        }
        return info
    
    def predict(self, input_data):
        """Make prediction using the model"""
        if self.model is None:
            return {"error": "Model not loaded"}
        
        try:
            # Ensure input is in the right format
            if isinstance(input_data, str):
                # For text input, convert to numerical representation
                # This is a placeholder - replace with your actual preprocessing
                input_array = self.preprocess_text(input_data)
            else:
                input_array = np.array(input_data)
            
            # Make prediction
            prediction = self.model.predict(input_array)
            return {"prediction": prediction.tolist(), "success": True}
        
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def preprocess_text(self, text):
        """Preprocess text input for the model"""
        # This is a placeholder function
        # Replace with your actual text preprocessing logic
        # For now, we'll create a dummy numerical representation
        
        # Convert text to a simple numerical representation
        # This should be replaced with proper tokenization/embedding
        text_length = len(text)
        word_count = len(text.split())
        
        # Create a feature vector (adjust size based on your model's input shape)
        features = np.array([[
            text_length / 100.0,  # Normalized text length
            word_count / 20.0,    # Normalized word count
            len(set(text.lower())) / 26.0,  # Character diversity
            text.count('?') + text.count('!'),  # Question/exclamation marks
            text.count('.'),  # Periods
            1.0 if any(word in text.lower() for word in ['hello', 'hi', 'hey']) else 0.0,
            1.0 if any(word in text.lower() for word in ['help', 'support', 'problem']) else 0.0,
            1.0 if any(word in text.lower() for word in ['thank', 'thanks', 'appreciate']) else 0.0,
            1.0 if any(word in text.lower() for word in ['bye', 'goodbye', 'see you']) else 0.0,
            np.random.random()  # Random feature for demonstration
        ]])
        
        return features
    
    def generate_response(self, user_input):
        """Generate a response based on user input and model prediction"""
        prediction_result = self.predict(user_input)
        
        if not prediction_result.get("success", False):
            return f"Sorry, I encountered an error: {prediction_result.get('error', 'Unknown error')}"
        
        prediction_value = prediction_result["prediction"][0][0]
        
        # Generate response based on prediction value
        # This is a simple example - customize based on your model's output
        if prediction_value > 0.8:
            responses = [
                "That's a great question! Based on my analysis, I'm very confident in my response.",
                "I'm highly confident about this topic. Let me help you with that!",
                "Excellent! I have strong insights on this matter."
            ]
        elif prediction_value > 0.6:
            responses = [
                "That's an interesting point. I have some good insights to share.",
                "I can definitely help you with that. Here's what I think...",
                "Good question! I have moderate confidence in my response."
            ]
        elif prediction_value > 0.4:
            responses = [
                "That's a thoughtful question. Let me provide what I can...",
                "I'll do my best to help, though I'm not entirely certain.",
                "Interesting topic. I have some thoughts, but with moderate confidence."
            ]
        else:
            responses = [
                "That's a complex question. I'm not very confident, but here's my best attempt...",
                "I'm not entirely sure about this, but I'll try to help.",
                "This is challenging for me, but let me share what I can..."
            ]
        
        import random
        base_response = random.choice(responses)
        
        # Add the prediction value for transparency
        return f"{base_response}\n\n(Model confidence: {prediction_value:.3f})"

