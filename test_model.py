#!/usr/bin/env python3.11

"""
Test script to verify TensorFlow model functionality
"""

import sys
import numpy as np
from model_handler import ModelHandler

def test_model_loading():
    """Test if the model loads correctly"""
    print("🧪 Testing model loading...")
    
    handler = ModelHandler()
    info = handler.get_model_info()
    
    if info["status"] == "Model loaded successfully":
        print("✅ Model loaded successfully!")
        print(f"   Input shape: {info['input_shape']}")
        print(f"   Output shape: {info['output_shape']}")
        print(f"   Parameters: {info['parameters']:,}")
        print(f"   Layers: {info['layers']}")
        return True
    else:
        print(f"❌ Model loading failed: {info['status']}")
        return False

def test_prediction():
    """Test model prediction functionality"""
    print("\n🔮 Testing prediction functionality...")
    
    handler = ModelHandler()
    
    # Test with sample text inputs
    test_inputs = [
        "Hello, how are you?",
        "What is artificial intelligence?",
        "Can you help me with machine learning?",
        "Thank you for your assistance!",
        "Goodbye!"
    ]
    
    all_passed = True
    
    for i, test_input in enumerate(test_inputs, 1):
        print(f"\n   Test {i}: '{test_input}'")
        
        # Test prediction
        result = handler.predict(test_input)
        
        if result.get("success", False):
            prediction = result["prediction"][0][0]
            print(f"   ✅ Prediction: {prediction:.4f}")
            
            # Test response generation
            response = handler.generate_response(test_input)
            print(f"   💬 Response: {response[:100]}...")
            
        else:
            print(f"   ❌ Prediction failed: {result.get('error', 'Unknown error')}")
            all_passed = False
    
    return all_passed

def test_preprocessing():
    """Test text preprocessing functionality"""
    print("\n🔧 Testing text preprocessing...")
    
    handler = ModelHandler()
    
    test_texts = [
        "Short text",
        "This is a longer text with multiple words and punctuation!",
        "Hello? How are you doing today. Thanks!",
        "A" * 200,  # Long text
        ""  # Empty text
    ]
    
    for i, text in enumerate(test_texts, 1):
        try:
            features = handler.preprocess_text(text)
            print(f"   Test {i}: Input length {len(text)} -> Features shape {features.shape}")
        except Exception as e:
            print(f"   ❌ Preprocessing failed for test {i}: {e}")
            return False
    
    print("   ✅ All preprocessing tests passed!")
    return True

def run_performance_test():
    """Test performance with multiple predictions"""
    print("\n⚡ Running performance test...")
    
    handler = ModelHandler()
    
    import time
    
    # Test with 10 predictions
    start_time = time.time()
    
    for i in range(10):
        test_input = f"Performance test message number {i+1}"
        result = handler.predict(test_input)
        
        if not result.get("success", False):
            print(f"   ❌ Performance test failed at iteration {i+1}")
            return False
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / 10
    
    print(f"   ✅ Performance test completed!")
    print(f"   📊 Total time: {total_time:.3f}s")
    print(f"   📊 Average time per prediction: {avg_time:.3f}s")
    print(f"   📊 Predictions per second: {1/avg_time:.1f}")
    
    return True

def main():
    """Run all tests"""
    print("🚀 AI Chatbot Model Testing Suite")
    print("=" * 50)
    
    tests = [
        ("Model Loading", test_model_loading),
        ("Prediction Functionality", test_prediction),
        ("Text Preprocessing", test_preprocessing),
        ("Performance", run_performance_test)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} Test...")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test PASSED")
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your chatbot is ready for demo!")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

