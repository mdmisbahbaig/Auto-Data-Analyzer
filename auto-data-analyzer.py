import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Auto Data Analyzer",
    layout="wide"
)

st.sidebar.title("Auto Data Analyzer")

file = st.sidebar.file_uploader("Upload your dataset", type= ['csv'])

if file:
    st.sidebar.success("File upload successful")

if file:
    st.subheader(file.name)
    df = pd.read_csv(file)


# Identifying Categorical and Numerical Columns
if file:
    max_unq = st.sidebar.slider("Max unique values for categorical charts", 5,50,5)

    if max_unq:
        cat_cols = []
        num_cols = []
        for col in df.columns:
            if len(df[col].unique()) <= max_unq:
                cat_cols.append(col)
            else:
                num_cols.append(col)

if file:
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric('ROWS', df.shape[0])
    with col2:
        st.metric('COLUMNS', df.shape[1])
    with col3:
        st.metric('NUMERIC', len(num_cols))
    with col4:
        st.metric('CATEGORICAL', len(cat_cols))
    with col5:
        st.metric('MISSING %', round((df.isnull().sum().sum() / df.size) * 100, 2))
    with col6:
        st.metric('DUPLICATES', df.duplicated().sum())

if file:
    st.write('Data Overview')
    st.write(df)

if file:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Overview")
        index = ['No. of Rows', 'No. of Columns', 'Duplicate Rows']
        rows = df.shape[0]
        cols = df.shape[1]
        duplicates = df.duplicated().sum()
        vals = [rows, cols, duplicates]
        st.write(pd.DataFrame({'0':index, '1':vals}))

    with col2:
        st.subheader("Missing Values")
        st.write(pd.DataFrame(df.isnull().sum()[df.isnull().sum() >0], columns = ['Missing']))

    with col3:
        st.subheader("Unique Values")
        st.write(df.nunique())
        
    st.markdown("## Statistical Summary of Numerical Columns")
    st.write(df.describe())

    st.markdown("### Correlation Between Numerical Columns")
    st.write(df.corr(numeric_only= True))

    # Plotting Numerical Column Graphs
    with st.expander('Show Univariate Numerical Graphs'):
            # plt.style.use('default')
            sns.set_theme(style="darkgrid")
            num_cols = df.describe().columns
            for col in num_cols:

                fig, ax = plt.subplots(1,3, figsize = (15,4))
                sns.histplot(df[col].dropna(),kde=True,ax=ax[0])
                ax[0].set_title(f"{col} Histogram")

                sns.boxplot(df[col].dropna(), ax= ax[1])
                ax[1].set_title(f"{col} Box Plot")
                
                sns.kdeplot(df[col].dropna(), ax = ax[2])
                ax[2].set_title(f"{col} KDE Plot")

                st.pyplot(fig)

    with st.expander('Show Correlation Heatmap'):
        fig, ax = plt.subplots()
        corr = df[num_cols].corr()
        sns.heatmap(corr, ax = ax)
        st.pyplot(fig)
            
    with st.expander('Show Pairplot'):
        st.markdown("### Pair Plot")
        pairplot_fig = sns.pairplot(data = df)
        st.pyplot(pairplot_fig) 
