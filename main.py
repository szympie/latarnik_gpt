import time

import streamlit as st
import pandas as pd

import streamlit_antd_components as sac
from dotenv import load_dotenv

from defaults import DEFAULT_QUESTIONS_DICT
from llm_logic import run_advise_chain


def prepare_questions_dict():
    df = pd.read_csv('./data/justifications.csv')
    questions = df['question'].unique()
    questions_dicts = [{'question': question, 'user_comment': ''} for question in questions]
    return questions_dicts


def update_answer(question_number):
    st.session_state.questions_dict[question_number - 1]['user_comment'] = st.session_state[
        f'question_{question_number}_text_area']


def next_page():
    st.session_state.page_number = st.session_state.page_number + 1


def previous_page():
    st.session_state.page_number = st.session_state.page_number - 1


def save_answer(question_number):
    update_answer(question_number)


@st.cache_data(show_spinner=False)
def create_answer(question_dict):
    result = run_advise_chain(question_dict)
    return result


load_dotenv()
if 'questions_dict' not in st.session_state:
    st.session_state.questions_dict = prepare_questions_dict()
    # st.session_state.questions_dict = DEFAULT_QUESTIONS_DICT

if 'page_number' not in st.session_state:
    st.session_state.page_number = 1

if st.session_state.page_number <= len(st.session_state.questions_dict):
    with st.container():
        question = st.session_state.questions_dict[st.session_state.page_number - 1]['question']
        user_answer = st.session_state.questions_dict[st.session_state.page_number - 1]['user_comment']

        st.markdown(f"<h3 style='text-align: center;'>{question}</h3>", unsafe_allow_html=True)
        st.text_area('Odpowiedź', value=user_answer, placeholder='Nie mam zdania',
                     key=f'question_{st.session_state.page_number}_text_area',
                     on_change=update_answer, args=[st.session_state.page_number])

        col1, col2 = st.columns(2)
        last_question = st.session_state.page_number == len(st.session_state.questions_dict)
        disabled_next = st.session_state.page_number == 20
        disabled_previous = st.session_state.page_number == 1
        previous_btn = col1.button('Wróć', use_container_width=True, type='secondary', on_click=save_answer,
                                   args=[st.session_state.page_number], disabled=disabled_previous)
        if previous_btn:
            previous_page()
            st.experimental_rerun()
        if not last_question:
            next_btn = col2.button('Dalej', use_container_width=True, type='primary', on_click=save_answer,
                                   args=[st.session_state.page_number], disabled=disabled_next)

            if next_btn:
                next_page()
                st.experimental_rerun()
        else:
            finish_btn = col2.button('Zakończ', use_container_width=True, type='primary', on_click=save_answer,
                                     args=[st.session_state.page_number])
            if finish_btn:
                next_page()
                st.experimental_rerun()

    st.divider()
    page_selector = sac.pagination(total=20, page_size=1, index=st.session_state.page_number, align='center',
                                   jump=False,
                                   show_total=False, key='page_number')
    if page_selector != st.session_state.page_number:
        st.session_state.page_number = page_selector
        st.experimental_rerun()
else:
    st.title('Wyniki ankiety')
    with st.spinner('Trwa generowanie wyników...'):
        answer = create_answer(st.session_state.questions_dict)
    st.markdown(answer)
    back_btn = st.button('Wróć do ankiety', use_container_width=True, type='primary')

    if back_btn:
        st.session_state.page_number = 1
        st.experimental_rerun()
