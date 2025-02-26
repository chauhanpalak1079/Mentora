import google.generativeai as genai

genai.configure(api_key="AIzaSyBcfVY6OI_pQdROE-CCgMb1hLgKXukWya0")  # Replace with your key

models = genai.list_models()
for model in models:
    print(model.name)
