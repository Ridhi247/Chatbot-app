import streamlit as st
import tensorflow as tf
import numpy as np

# Function to load the model (cached for performance)
@st.cache_resource
def load_model():
    try:
        model = tf.keras.models.load_model("tf_model.h5")
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

st.title("AI Chatbot Demo")

if model:
    st.success("Model loaded successfully!")
    st.write("You can now interact with the chatbot.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Say something..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Dummy response for now, replace with actual model prediction
                # For a real model, you'd process the prompt and get a prediction
                # For example: prediction = model.predict(preprocess(prompt))
                # Then, generate a response based on the prediction
                
                # Placeholder for model inference
                dummy_input = np.random.rand(1, 10) # Adjust input shape as per your model
                try:
                    prediction = model.predict(dummy_input)
                    response = f"Model received your input and made a prediction: {prediction[0][0]:.4f}"
                except Exception as e:
                    response = f"Error during model prediction: {e}"

                st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.warning("Model could not be loaded. Please ensure 'tf_model.h5' is in the correct directory and is a valid TensorFlow model.")


