import streamlit as st
import openai
import os

def get_openai_client(api_key, endpoint):
    openai.api_type = 'azure'
    openai.api_key = api_key
    openai.api_version = '2023-12-01-preview'
    openai.api_base = endpoint
    return openai

def gpt_function(client, size, sector , function):
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
    function{function}(Optional)
"""

  
    conversation = [{"role": "system", "content": """You are a future AI skills Planner bot.
                                    - Your role is to identify AI skills gaps in your organization and get recommendations for training or hiring strategies, based on the given parameters Company size , Sector and function(Optional).
                                    - You should address skill gaps and inform talent development strategies
                                    
                                The output should also contain:
                                    - AI impact on sector summary Skills & Capabilities required to harness AI
                                    - Next steps (ordered by priority based on AI impact on given sector and perceived maturity levels based on company) Note. skills & capabilities output should be split by business function
                                    
                                    Steps to analyze:
                                    - Analyze current skills inventory
                                    - Forecast future needs
                                    - Provide recommendations for training or hiring to fill gaps 
                                    """},
                     {"role": "user", "content": f"{user_content}"}]

    response = client.ChatCompletion.create(
        messages=conversation,
        engine="gpt-35-turbo",
        temperature=0
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
    st.sidebar.title("Azure OpenAI API Key")
    openai_api_key = st.sidebar.text_input("Enter your Azure OpenAI API Key", type="password")
    openai_endpoint = 'https://bc-api-management-uksouth.azure-api.net'
    client = get_openai_client(openai_api_key, openai_endpoint)

    st.title("AI Skills Planner")

    description = """
    #### About the App
    ###### Identify skills gaps in your orginazation and get recommedations for training or hiring strategies.
    """

    st.markdown(description , unsafe_allow_html=True)

    input_list = ["Company Size", "Company Sector", "Function(Optional)"]

    sector = st.text_input(input_list[1])
    size = st.text_input(input_list[0])
    function = st.text_input(input_list[2])

    if not function:
        function = "None"

    

    if size and sector:
        if st.button("Submit"):
            with st.spinner("Let the magic happen..."):
                output = gpt_function(client, size, sector,function)
                st.markdown(output,unsafe_allow_html=True)

if __name__ == "__main__":
    main()
