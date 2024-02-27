import streamlit as st
from streamlit_chat import message

import utils


def initialize_session_state():
    st.session_state.setdefault('history', [])
    st.session_state.setdefault('generated',
                                ["Hello! I am here to provide answers to questions fetched from Database."])
    st.session_state.setdefault('past', ["Hello Buddy!"])


st.session_state.fill = None

if st.button("Fill the input box with a sample text"):
    st.session_state.fill = "Brainstorm a list of points that can be mentioned in the technical document."
if st.button("Clear"):
    st.session_state.fill = None


def display_chat(chain):
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key='chat_form', clear_on_submit=True):
            user_input = st.text_input("Question:", placeholder="Ask me questions", key='input',
                                       value=st.session_state.fill)
            submit_button = st.form_submit_button(label='Send ⬆️')

        if submit_button and user_input:
            generate_response(user_input, chain)

    display_generated_responses(reply_container)


def generate_response(user_input, chain):
    with st.spinner('Spinning a snazzy reply...'):
        output = conversation_chat(user_input, chain, st.session_state['history'])
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)


def conversation_chat(user_input, chain, history):
    response = chain.invoke(user_input)
    history.append((user_input, response))
    return response


def display_generated_responses(reply_container):
    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=f"{i}_user", avatar_style="adventurer")
                message(st.session_state["generated"][i], key=str(i), avatar_style="bottts")


def main():
    initialize_session_state()

    st.title("Genie")
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Step 2: Initialize Streamlit
    chain = utils.create_conversational_chain()

    # Step 3 - Display Chat to Web UI
    display_chat(chain)


if __name__ == "__main__":
    main()
