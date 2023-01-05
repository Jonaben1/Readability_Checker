import streamlit as st
import textstat as ts
from pdfminer.high_level import extract_text
from io import StringIO
import docx2txt
import requests
from bs4 import BeautifulSoup as bs


st.title('Streamlit Readability Checker')
st.write("Created and designed by [Jonaben](https://www.linkedin.com/in/jonathan-ben-okah-7b507725b)")

def main():

    """
    The main function for readability checking. It gives several options which when selected
    triggers the execution of several other functions all linked together to acheive a result.
    """

    mode = st.sidebar.selectbox('Select your option', ['Text', '.pdf', '.txt', '.docx', 'Online'])
    # a function is called depending on the mode selected
    if mode == 'Text':
        text_result()
    elif mode == '.pdf':
        upload_pdf()
    elif mode == '.txt':
        upload_txt()
    elif mode == '.docx':
        upload_docx()
    else:
        get_url()




def text_result():

    """
    To enable text to be typed or pasted. It accepts input from the user, send it to the
    readability_checker() to scan the input and gives out the result.
    """

    text = 'Your text goes here...'
    #displaying the textbox where texts will be written
    box = st.text_area('Text Field', text, height=200)
    scan = st.button('Scan File')
    # if button is pressed
    if scan:
        # display statistical results
        st.write('Text Statistics')
        st.write(readability_checker(box))


def readability_checker(w):

    """
    The function that checks for readability of the text received and returns
    result in dictionary form.
    """

    stats = dict(flesch_reading_ease=ts.flesch_reading_ease(w),
            flesch_kincaid_grade=ts.flesch_kincaid_grade(w),
            automated_readability_index=ts.automated_readability_index(w),
            smog_index=ts.smog_index(w),
            coleman_liau_index=ts.coleman_liau_index(w),
            dale_chall_readability_score=ts.dale_chall_readability_score(w),
            linsear_write_formula=ts.linsear_write_formula(w),
            gunning_fog=ts.gunning_fog(w),
            word_count=ts.lexicon_count(w),
            difficult_words=ts.difficult_words(w),
            text_standard=ts.text_standard(w),
            sentence_count=ts.sentence_count(w),
            syllable_count=ts.syllable_count(w),
            reading_time=ts.reading_time(w)
    )
    return stats


def upload_pdf():

    """ To enable pdf files to be uploaded by the user. It extracts the file
        and sends it to another function to display the readability result.
    """

    file = st.sidebar.file_uploader('Choose a file', type='pdf')
    if file is not None:
        pdf = extract_text(file)
        # sending the text to textbox
        document_result(pdf)


def upload_txt():

    """ To enable txt files to be uploaded by the user. It receives a file
        and sends it to another function that will extract it.
    """

    file = st.sidebar.file_uploader('Choose a file', type='txt')
    if file is not None:
        extract_txt(file)


def extract_txt(text):

    """ It recieves txt file, extracts it and sends it to another function
        to display the readability result.
    """

    string_io = StringIO(text.getvalue().decode('utf-8'))
    string_data = string_io.read()
    document_result(string_data)


def upload_docx():

    """ To enable docx files to be uploaded by the user. It extracts the file
        and sends it to another function to display the readability result.
    """

    file = st.sidebar.file_uploader('Choose a file', type='docx')
    if file is not None:
        docx = docx2txt.process(file)
        document_result(docx)


def document_result(file):

    """
    It receives texts extracted, send it to the
    readability_checker() to be scanned and gives out the result.
    """

    #displaying the textbox where texts will be received
    box = st.text_area('Text Field', file, height=200)
    scan = st.button('Scan Text')
    # if button is pressed
    if scan:
        # display statistical results
        st.write('Text Statistics')
        st.write(readability_checker(box))


def get_url():

    """
    It recieves the url address of a webpage and sends it to
    another function.
    """
    url = st.sidebar.text_input("Paste your url")
    if url:
        get_data(url)


def get_data(url):

    """
    receive the url address and make a request. If successful, it
    returns the content of the webpage. It then filters out the
    html tags and sends the 'clean' content to be scanned.
    """

    page = requests.get(url)
    if page.status_code != 200:
        print('Error fetching page')
        exit()
    else:
        content = page.content
    soup = bs(content, 'html.parser')
    document_result(soup.get_text())



if __name__ == '__main__':
    main()
