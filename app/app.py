import streamlit as st
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Azure OpenAI service client
client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ['AZURE_OPENAI_API_KEY'],
    api_version="2023-10-01-preview"
)

deployment = 'gpt-4o-mini'

# Streamlit app
st.title("Recipe Generator with Shopping List")

st.sidebar.header("Input Parameters")

# Sidebar inputs
no_recipes = st.sidebar.text_input("Number of recipes:", "5")
ingredients = st.sidebar.text_input("List of ingredients:", "chicken, potatoes, carrots")
filter = st.sidebar.selectbox("Filter:", ["none", "vegetarian", "vegan", "gluten-free"])

# Button to generate recipes
if st.sidebar.button("Generate Recipes"):
    with st.spinner("Generating recipes..."):
        # Prompt for recipes
        prompt = f"Show me {no_recipes} recipes for a dish with the following ingredients: {ingredients}. Per recipe, list all the ingredients used, no {filter}:"
        messages = [{"role": "user", "content": prompt}]

        try:
            completion = client.chat.completions.create(
                model=deployment,
                messages=messages,
                max_tokens=600,
                temperature=0.1
            )
            recipes = completion.choices[0].message.content
            st.subheader("Generated Recipes")
            st.text_area("Recipes:", recipes, height=200)

            # Generate shopping list
            prompt_shopping = "Produce a shopping list, and please don't include ingredients that I already have at home:"
            new_prompt = f"Given ingredients at home {ingredients} and these generated recipes: {recipes}, {prompt_shopping}"
            messages = [{"role": "user", "content": new_prompt}]

            shopping_completion = client.chat.completions.create(
                model=deployment,
                messages=messages,
                max_tokens=600,
                temperature=0.1
            )
            shopping_list = shopping_completion.choices[0].message.content
            
            st.subheader("Shopping List")
            st.text_area("Shopping List:", shopping_list, height=200)
        except Exception as e:
            st.error(f"An error occurred: {e}")
