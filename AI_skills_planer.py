import streamlit as st
import openai
import os

def get_openai_client(api_key):
    return openai.OpenAI(api_key=api_key)

def gpt_function(client, size, sector):
    """
    Brief documentation for the gpt_function.

    This function takes 3 inputs, calls the GPT API,
    and returns a string concatenating the inputs.

    Returns:
    gpt_output
    """
    user_content = f"""
    Get future recommendations for training or hiring strategies for the following parameters 
    Company Size: {size} People.
    Company Sector: {sector}
"""

    # Make GPT call here
    conversation = [{"role": "system", "content": """You are a future AI skills Planner bot.
                                    - Your role is to identify AI skills gaps in your organization and get recommendations for training or hiring strategies, based on the given parameters Company size and Sector
                                    - You should address skill gaps and inform talent development strategies
                                    
                                    Steps to analyze:
                                    - Analyze current skills inventory
                                    - Forecast future needs
                                    - Provide recommendations for training or hiring to fill gaps 
                                    """},
                     {"role": "user", "content": f"{user_content}"}]

    response = client.chat.completions.create(
        messages=conversation,
        model="gpt-3.5-turbo",
    )
    text_response = response.choices[0].message.content

    return text_response

def main():
    """
    Briefly documents the main() function.

    The main() function:
    - Creates the Streamlit app title
    - Initializes a list of input prompts
    - Gets text inputs from the user
    - Calls the gpt_function() with the inputs
    - Writes the output of gpt_function()
    """
    st.sidebar.title("OpenAI API Key")
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
    client = get_openai_client(openai_api_key)

    st.title("AI Skills Planner")

    input_list = ["Company Size", "Company Sector"]

    size = st.text_input(input_list[0])
    sector = st.text_input(input_list[1])

    if size and sector:
        if st.button("Submit"):
            with st.spinner("Let the magic happen..."):
                output = gpt_function(client, size, sector)
                st.write(output)

if __name__ == "__main__":
    main()
