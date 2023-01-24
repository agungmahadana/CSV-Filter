import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV Filter", page_icon="♻")
st.title("Welcome to CSV Filter! 👋")
st.caption("CSV Filter is a web-based application that can filter data on csv file using insertion sort algorithm. Besides uploading, users can also download file that have been sorted. This app was created by a [student](https://github.com/agungmahadana/) using Python and Streamlit.")
uploaded_file = st.file_uploader(label='', type='csv')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, delimiter=';')
    data = []
    indeks = []

    # convert dataframe (csv) to list
    for i in df.axes[0]:
        data.append(df.loc[i])

    # create index (1, 2, 3, ...)
    for i in df.axes[0]:
        indeks.append(str(i+1))

    # sorting algorithm
    def insertion_sort(data, col, order):
        for i in range(1, len(data)):
            key = data[i][col]
            j = i - 1
            if order == 'Ascending':
                while j >= 0 and key < data[j][col]:
                    data[j], data[j+1] = data[j+1], data[j]
                    j -= 1
            elif order == 'Descending':
                while j >= 0 and key > data[j][col]:
                    data[j], data[j+1] = data[j+1], data[j]
                    j -= 1
        data[j+1][col] = key

    # prepare data to download
    def download(final):
        str = ''
        for i in range(len(final.axes[1])):
            if i != len(final.axes[1])-1:
                str += final.axes[1][i].__str__() + ';'
            else:
                str += final.axes[1][i].__str__() + '\n'
        for i in range(len(data)):
            for j in range(len(data[i])):
                    if j != len(data[i])-1:
                        str += data[i][j].__str__() + ';'
                    else:
                        str += data[i][j].__str__() + '\n'
        return str

    # frontend
    input = st.sidebar.selectbox('Choose column to sort', df.columns)
    order = st.sidebar.radio('Sort by',['Ascending', 'Descending'])
    insertion_sort(data, input, order)
    final = pd.DataFrame(data, index=indeks)
    st.write(final)
    download = download(final)
    name = uploaded_file.name
    st.sidebar.download_button(label='Download', data=download, file_name=name.replace('.csv', '_sorted.csv'), mime='text/csv')