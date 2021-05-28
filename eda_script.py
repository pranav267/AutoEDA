import streamlit as st
from PIL import Image
import datetime
from plots import *
from eda_helpers import *


def eda():
    image = Image.open('eda.png')
    st.image(image)
    st.text('')
    st.text('')
    st.text('')
    uploaded_file = st.file_uploader("UPLOAD DATA", type=["csv"])
    st.text('')
    st.text('')
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        eda_choice = st.sidebar.radio(
            "OPTIONS", ('GENERAL INFORMATION', 'UNIVARIATE ANALYSIS', 'MULTIVARIATE ANALYSIS', 'RELATION HEATMAPS'))

        if eda_choice == 'GENERAL INFORMATION':
            st.markdown(
                "<h3 style='text-align: center; letter-spacing:8px;font-size: 30px; background-color:#242424; border-radius:25px;'>DATASET</h3>", unsafe_allow_html=True)
            st.text('')
            st.text('')
            st.dataframe(data)
            st.text('')
            variables = len(data.columns)
            observations = len(data)
            missing_cells = data.isna().sum().sum()
            m_c = (len(data) * len(data.columns))
            missing_cells_ = np.round((missing_cells / m_c)*100, 2)
            df_dup = data.drop_duplicates()
            dup_cells = len(data) - len(df_dup)
            dup_cells_ = np.round((dup_cells / observations)*100, 2)
            col1, col2 = st.beta_columns(2)
            with col1:
                st.markdown(
                    f"<h3 style='text-align: left; letter-spacing:3px;font-size: 15px;background-color:#242424;'>NUMBER OF VARIABLES : {str(variables)} </h3>", unsafe_allow_html=True)
                st.markdown(
                    f"<h3 style='text-align: left; letter-spacing:3px;font-size: 15px;background-color:#242424;'>NUMBER OF MISSING CELLS : {str(missing_cells)}</h3>", unsafe_allow_html=True)
                st.markdown(
                    f"<h3 style='text-align: left; letter-spacing:3px;font-size: 15px;background-color:#242424;'>NUMBER OF DUPLICATE OBSERVATIONS : {str(dup_cells)}</h3>", unsafe_allow_html=True)
            with col2:
                st.markdown(
                    f"<h3 style='text-align: right; letter-spacing:3px;font-size: 15px;background-color:#242424;'>NUMBER OF OBSERVATIONS : {str(observations)} </h3>", unsafe_allow_html=True)
                st.markdown(
                    f"<h3 style='text-align: right; letter-spacing:3px;font-size: 15px;background-color:#242424;'>PERCENTAGE OF MISSING CELLS : {str(missing_cells_)}%</h3>", unsafe_allow_html=True)
                st.markdown(
                    f"<h3 style='text-align: right; letter-spacing:3px;font-size: 15px;background-color:#242424;'>PERCENTAGE OF DUPLICATE OBSERVATIONS : {str(dup_cells_)}%</h3>", unsafe_allow_html=True)
            st.text('')
            st.text('')
            st.markdown(
                "<h3 style='text-align: center; letter-spacing:8px;font-size: 30px; background-color:#242424; border-radius:25px;'>DATA SUMMARY</h3>", unsafe_allow_html=True)
            st.text('')
            st.text('')
            _, col3, __ = st.beta_columns([1, 4, 1])
            with col3:
                st.dataframe(data.describe())
            st.text('')
            st.text('')
            st.markdown(
                "<h3 style='text-align: center; letter-spacing:8px;font-size: 30px; background-color:#242424; border-radius:25px;'>DATA TYPES</h3>", unsafe_allow_html=True)
            st.text('')
            st.text('')
            _, col4, col5 = st.beta_columns([1, 2, 3])
            with col4:
                df_types = pd.DataFrame()
                df_types['Columns'] = list(data.dtypes.index)
                df_types['Types'] = list(data.dtypes.values)
                st.dataframe(df_types, height=400)
            cat_cols = list(data.select_dtypes(include='object').columns)
            num_cols = list(data.select_dtypes(exclude='object').columns)

            for i in cat_cols:
                t = data[i].dropna()
                if not check_number_str(t):
                    num_cols.append(i)
                    cat_cols.remove(i)

            cat_cols_p = []
            for i in num_cols:
                if len(data[i].unique()) <= 10:
                    cat_cols_p.append(i)

            for i in num_cols:
                t = data[i]
                for j in range(len(t)):
                    a, b = check_no(t[j])
                    if a == False and b == False:
                        t[j] = int(t[j])
                    elif a == False and b == True:
                        t[j] = float(t[j])
                    else:
                        t[j] = np.nan
                data[i] = t

            for i in cat_cols:
                t = data[i]
                for j in range(len(t)):
                    if not isinstance(t[j], str):
                        t[j] = np.nan
                    else:
                        if len(t[j].strip()) == 0:
                            t[j] = np.nan
                data[i] = t
            with col5:
                st.text('')
                st.text('')
                st.text('')
                st.text('')
                st.text('')
                st.markdown(
                    f"<h3 style='text-align: left; letter-spacing:3px;font-size: 15px;background-color:#242424;'>NUMBER OF CATEGORICAL COLUMNS : {str(len(cat_cols))} </h3>", unsafe_allow_html=True)
                st.markdown(
                    f"<h3 style='text-align: left; letter-spacing:3px;font-size: 15px;background-color:#242424;'>NUMBER OF NUMERICAL COLUMNS : {str(len(num_cols))} </h3>", unsafe_allow_html=True)
                st.markdown(
                    f"<h3 style='text-align: left; letter-spacing:3px;font-size: 15px;background-color:#242424;'>NUMBER OF POTENTIAL CATEGORICAL COLUMNS : {str(len(cat_cols_p))} </h3>", unsafe_allow_html=True)
            st.text('')
            st.text('')
            st.markdown(
                "<h3 style='text-align: center; letter-spacing:8px;font-size: 30px; background-color:#242424; border-radius:30px;'>MISSING VALUES</h3>", unsafe_allow_html=True)
            col6, col7 = st.beta_columns([2, 1])
            with col6:
                st.text('')
                st.text('')
                df_present = pd.DataFrame()
                df_present['Columns'] = list(data.count().index)
                df_present['Counts'] = list(data.count().values)
                plot = MissingData(df_present)
                st.plotly_chart(plot, use_container_width=True)
            with col7:
                st.text('')
                st.text('')
                st.text('')
                st.text('')
                st.text('')
                st.text('')
                st.text('')
                st.text('')
                st.text('')
                df_missing = pd.DataFrame()
                df_missing['Columns'] = list(data.isnull().sum().index)
                df_missing['Missing Count'] = list(data.isnull().sum().values)
                df_missing['Missing %'] = np.round(
                    (df_missing['Missing Count'] / len(data)) * 100, 2)
                df_missing = df_missing[df_missing['Missing %'] > 0].sort_values(
                    'Missing %', ascending=False)
                df_missing['Missing %'] = df_missing['Missing %'].apply(
                    lambda x: str(x)+'%')
                df_missing.set_index('Columns', inplace=True)
                st.dataframe(df_missing, height=400)

        elif eda_choice == 'UNIVARIATE ANALYSIS':
            st.markdown(
                "<h3 style='text-align: center; letter-spacing:8px;font-size: 30px; background-color:#242424; border-radius:25px;'>UNIVARIATE ANALYSIS</h3>", unsafe_allow_html=True)
            st.text('')
            st.text('')
            col = st.selectbox('SELECT COLUMN', list(data.columns))
            st.text('')
            st.text('')
            if data[col].dtype != 'object' and len(data[col].unique()) <= 15:
                c1, c2 = st.beta_columns(2)
                with c1:
                    plot1 = CountPlot(data, col)
                    st.plotly_chart(plot1, use_container_width=True)
                with c2:
                    plot2 = PieChart(data, col)
                    st.plotly_chart(plot2, use_container_width=True)
                classes = len(data[col].unique())
                mia = data[col].isnull().sum().sum()
                mia_p = np.round((mia/len(data))*100, 2)
                df = data.groupby(col)[[col]].count()
                df.columns = ['Count']
                df = df.reset_index()
                max_count = df.loc[df['Count'] ==
                                   df['Count'].max()]['Count'].values[0]
                max_count_p = np.round((max_count/len(data))*100, 2)
                max_class = df.loc[df['Count'] ==
                                   df['Count'].max()][col].values[0]
                min_count = df.loc[df['Count'] ==
                                   df['Count'].min()]['Count'].values[0]
                min_count_p = np.round((min_count/len(data))*100, 2)
                min_class = df.loc[df['Count'] ==
                                   df['Count'].min()][col].values[0]
                c3, c4, c5 = st.beta_columns([1, 2, 1])
                with c4:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>NUMBER OF CLASSES : {str(classes)} </h3>", unsafe_allow_html=True)
                c6, c7 = st.beta_columns(2)
                with c6:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>NUMBER OF MISSING OBSERVATIONS : {str(mia)} </h3>", unsafe_allow_html=True)
                with c7:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>PERCENTAGE OF MISSING OBSERVATIONS : {str(mia_p)}% </h3>", unsafe_allow_html=True)
                c8, c9 = st.beta_columns(2)
                with c8:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>MOST FREQUENT VALUE : {str(max_class)} ({str(max_count_p)}%) </h3>", unsafe_allow_html=True)
                with c9:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>LEAST FREQUENT VALUE : {str(min_class)} ({str(min_count_p)}%) </h3>", unsafe_allow_html=True)
            elif data[col].dtype != 'object' and len(data[col].unique()) > 15:
                _, c01, c02, __ = st.beta_columns([1, 1, 2, 1])
                with c01:
                    kde = st.radio("CURVE TYPE", ('kde', 'normal'))
                with c02:
                    bins = st.slider("NUMBER OF BINS", min_value=1,
                                     max_value=100, value=1, step=1)
                plot1 = DistPlot(data, col, [bins], kde)
                st.plotly_chart(plot1, use_container_width=True)
                df_t = data[col].copy()
                df_t = df_t.dropna()
                card = np.round(
                    (df_t.nunique() / len(df_t))*100, 2)
                mia = data[col].isnull().sum().sum()
                mia_p = np.round((mia/len(data))*100, 2)
                _, c0, __ = st.beta_columns([1, 2, 1])
                with c0:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>UNIQUE(%) : {str(card)}% </h3>", unsafe_allow_html=True)
                c1, c2 = st.beta_columns(2)
                with c1:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>NUMBER OF MISSING OBSERVATIONS : {str(mia)} </h3>", unsafe_allow_html=True)
                with c2:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>PERCENTAGE OF MISSING OBSERVATIONS : {str(mia_p)}% </h3>", unsafe_allow_html=True)
                st.text('')
                s, sm1, sm2 = check_skew(data[col])
                k, km1, km2, km3 = check_kurtosis(data[col])
                c3, c4 = st.beta_columns([1, 2])
                with c3:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>SKEW : </h3>", unsafe_allow_html=True)
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>INFERENCE : </h3>", unsafe_allow_html=True)
                with c4:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'> {str(s)} </h3>", unsafe_allow_html=True)
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'> {str(sm1)} </h3>", unsafe_allow_html=True)
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'> {str(sm2)} </h3>", unsafe_allow_html=True)
                st.text('')
                c5, c6 = st.beta_columns([1, 2])
                with c5:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>KURTOSIS : </h3>", unsafe_allow_html=True)
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>INFERENCE : </h3>", unsafe_allow_html=True)
                with c6:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'> {str(k)} </h3>", unsafe_allow_html=True)
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'> {str(km1)} </h3>", unsafe_allow_html=True)
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'> {str(km2)} </h3>", unsafe_allow_html=True)
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'> {str(km3)} </h3>", unsafe_allow_html=True)
                plot2 = BoxViolinSwarmPlot(data, col)
                st.plotly_chart(plot2, use_container_width=True)
                mean, var, std, min, p25, median, p75, max, iqr = stats(
                    data[col])
                c7, c8 = st.beta_columns(2)
                with c7:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'> MEAN : {str(mean)} </h3>", unsafe_allow_html=True)
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'> MEDIAN : {str(median)} </h3>", unsafe_allow_html=True)
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'> VARIANCE : {str(var)} </h3>", unsafe_allow_html=True)
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'> STANDARD DEVIATION : {str(std)} </h3>", unsafe_allow_html=True)
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'> MINIMUM VALUE : {str(min)} </h3>", unsafe_allow_html=True)
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'> MAXIMUM VALUE : {str(max)} </h3>", unsafe_allow_html=True)
                with c8:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'> 25th PERCENTILE VALUE : {str(p25)} </h3>", unsafe_allow_html=True)
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'> 75th PERCENTILE VALUE: {str(p75)} </h3>", unsafe_allow_html=True)
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'> INTER QUARTILE RANGE : {str(iqr)} </h3>", unsafe_allow_html=True)
                    p = st.slider(
                        'PERCENTILE CALCULATOR', min_value=0, max_value=100, value=50, step=1)
                    p_ = p / 100
                    p__ = round(data[col].quantile(p_), 2)
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'> {str(p)} PERCENTILE : {str(p__)} </h3>", unsafe_allow_html=True)
            elif data[col].dtype == 'object' and len(data[col].unique()) <= 15:
                c1, c2 = st.beta_columns(2)
                with c1:
                    plot1 = CountPlot(data, col)
                    st.plotly_chart(plot1, use_container_width=True)
                with c2:
                    plot2 = PieChart(data, col)
                    st.plotly_chart(plot2, use_container_width=True)
                classes = len(data[col].unique())
                mia = data[col].isnull().sum().sum()
                mia_p = np.round((mia/len(data))*100, 2)
                df = data.groupby(col)[[col]].count()
                df.columns = ['Count']
                df = df.reset_index()
                max_count = df.loc[df['Count'] ==
                                   df['Count'].max()]['Count'].values[0]
                max_count_p = np.round((max_count/len(data))*100, 2)
                max_class = df.loc[df['Count'] ==
                                   df['Count'].max()][col].values[0]
                min_count = df.loc[df['Count'] ==
                                   df['Count'].min()]['Count'].values[0]
                min_count_p = np.round((min_count/len(data))*100, 2)
                min_class = df.loc[df['Count'] ==
                                   df['Count'].min()][col].values[0]
                c3, c4, c5 = st.beta_columns([1, 2, 1])
                with c4:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>NUMBER OF CLASSES : {str(classes)} </h3>", unsafe_allow_html=True)
                c6, c7 = st.beta_columns(2)
                with c6:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>NUMBER OF MISSING OBSERVATIONS : {str(mia)} </h3>", unsafe_allow_html=True)
                with c7:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>PERCENTAGE OF MISSING OBSERVATIONS : {str(mia_p)}% </h3>", unsafe_allow_html=True)
                c8, c9 = st.beta_columns(2)
                with c8:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>MOST FREQUENT VALUE : {str(max_class)} ({str(max_count_p)}%) </h3>", unsafe_allow_html=True)
                with c9:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>LEAST FREQUENT VALUE : {str(min_class)} ({str(min_count_p)}%) </h3>", unsafe_allow_html=True)
            else:
                c1, c2 = st.beta_columns([2, 1])
                stp = None
                lower = None
                punct = None
                word_c = None
                with c1:
                    stp = st.selectbox(
                        'WANT TO REMOVE STOPWORDS ?', ['No', 'Yes'])
                    lower = st.selectbox('WANT TO LOWER TEXT ?', ['Yes', 'No'])
                    punct = st.selectbox(
                        'WANT TO REMOVE PUNCTUATIONS ?', ['No', 'Yes'])
                    stp_ = None
                    lower_ = None
                    punct_ = None
                    if stp == 'No':
                        stp_ = False
                    else:
                        stp_ = True
                    if lower == 'No':
                        lower_ = False
                    else:
                        lower_ = True
                    if punct == 'No':
                        punct_ = False
                    else:
                        punct_ = True
                    word_c = prepare_text_col(
                        data[col], lower=lower_, stp=stp_, punct=punct_)
                    to = len(word_c)
                with c2:
                    st.dataframe(word_c)
                plot1 = BarPlot(word_c)
                st.plotly_chart(plot1, use_container_width=True)
                card = np.round(
                    (data[col].nunique() / len(data))*100, 2)
                mia = data[col].isnull().sum().sum()
                mia_p = np.round((mia/len(data))*100, 2)
                _, __, ___ = st.beta_columns(3)
                with __:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>UNIQUE(%) : {str(card)}% </h3>", unsafe_allow_html=True)
                c3, c4 = st.beta_columns(2)
                with c3:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>MOST FREQUENT : {str(word_c.head(1)['Elements'].values[0])} ({str(word_c.head(1)['Counts'].values[0])}) </h3>", unsafe_allow_html=True)
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>NUMBER OF MISSING OBSERVATIONS : {str(mia)} </h3>", unsafe_allow_html=True)
                with c4:
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>LEAST FREQUENT : {str(word_c.tail(1)['Elements'].values[0])} ({str(word_c.tail(1)['Counts'].values[0])}) </h3>", unsafe_allow_html=True)
                    st.markdown(
                        f"<h3 style='text-align: center; letter-spacing:3px;font-size: 15px;background-color:#242424;'>PERCENTAGE OF MISSING OBSERVATIONS : {str(mia_p)}% </h3>", unsafe_allow_html=True)
                st.text('')
                st.text('')
                cc1, cc2 = st.beta_columns([1, 2])
                bins = None
                with cc1:
                    st.text('')
                    st.text('')
                    st.text('')
                    st.text('')
                    st.text('')
                    st.text('')
                    st.text('')
                    st.text('')
                    st.text('')
                    st.text('')
                    bins = st.slider(
                        'NUMBER OF BINS', min_value=5, max_value=50, value=10, step=5)
                with cc2:
                    plot2 = LenPlot(data, col, bins)
                    st.plotly_chart(plot2, use_container_width=True)
        elif eda_choice == 'MULTIVARIATE ANALYSIS':
            st.markdown(
                "<h3 style='text-align: center; letter-spacing:8px;font-size: 30px; background-color:#242424; border-radius:25px;'>MULTIVARIATE ANALYSIS</h3>", unsafe_allow_html=True)
            st.text('')
            st.text('')
            PLOTS = [
                'Bar Plot', 'Pie Chart', 'Box Plot', 'Violin Plot', 'Dist Plot',
                'Scatter Plot', 'Line Plot', 'Area Plot', 'Density Contour Plot']
            grp1, grp2, grp3, grp4 = get_grps(data)
            plot_type = st.selectbox('CHOOSE NEEDED PLOT', PLOTS)
            if plot_type == 'Bar Plot':
                if len(grp1) < 1:
                    st.text('')
                    st.text('')
                    st.error('UNSUFFICIENT NUMBER OF SUITABLE FEATURES FOUND')
                else:
                    c1, c2 = st.beta_columns([1, 2])
                    bar_choice = None
                    hue_choice = None
                    barp_choice = None
                    with c1:
                        st.text('')
                        st.text('')
                        st.text('')
                        st.text('')
                        st.text('')
                        st.text('')
                        st.text('')
                        st.text('')
                        bar_choice = st.selectbox('CHOOSE FEATURE', grp1)
                        hue_col = grp1.copy()
                        hue_col.remove(bar_choice)
                        hue_choice = st.selectbox(
                            'CHOOSE HUE FEATURE', ['None']+hue_col)
                        if hue_choice != 'None':
                            barp_choice = st.selectbox(
                                'CHOOSE BAR TYPE', ['Relative', 'Group'])
                with c2:
                    hp = None
                    bp = None
                    if hue_choice != 'None':
                        hp = hue_choice
                    if barp_choice == 'Relative':
                        bp = 'relative'
                    else:
                        bp = 'group'
                    plot = BarPlotM(data, bar_choice,
                                    bp, hue=hp)
                    st.plotly_chart(plot, use_container_width=True)
            elif plot_type == 'Pie Chart':
                if len(grp1) < 1:
                    st.text('')
                    st.text('')
                    st.error('UNSUFFICIENT NUMBER OF SUITABLE FEATURES FOUND')
                else:
                    c1, c2 = st.beta_columns([1, 2])
                    bar_choice = None
                    hole_r = 0
                    with c1:
                        st.text('')
                        st.text('')
                        st.text('')
                        st.text('')
                        st.text('')
                        st.text('')
                        bar_choice = st.selectbox('CHOOSE FEATURE', grp1)
                        st.text('')
                        hole_r = st.slider(
                            'HOLE RADIUS', min_value=0, max_value=9, value=6, step=1)
                        hole_r /= 10
                    with c2:
                        plot = PieChartM(data, bar_choice, hole_r)
                        st.plotly_chart(plot, use_container_width=True)
            elif plot_type == 'Box Plot':
                if len(grp4) < 1:
                    st.text('')
                    st.text('')
                    st.error('UNSUFFICIENT NUMBER OF SUITABLE FEATURES FOUND')
                else:
                    bc = 'None'
                    hc1 = 'None'
                    hc2 = 'None'
                    c_1 = 'None'
                    c_2 = 'None'
                    c_3 = 'None'
                    c1, c2 = st.beta_columns([2, 1])
                    with c1:
                        st.text('')
                        st.text('')
                        st.text('')
                        bc = st.selectbox('CHOOSE FEATURE', grp4)
                        h_ = ['None']+grp1
                        hc1 = st.selectbox('CHOOSE HUE FEATURE', h_)
                        if hc1 != 'None':
                            h__ = h_.copy()
                            h__.remove(hc1)
                            hc2 = st.selectbox(
                                'CHOOSE ANOTHER HUE FEATURE', h__)
                    with c2:
                        st.text('')
                        st.text('')
                        st.text('')
                        st.text('')
                        st.text('')
                        st.text('')
                        c_1 = st.checkbox('Notched', value=True)
                        st.text('')
                        if hc2 != 'None':
                            c_2_ = st.selectbox(
                                'CHOOSE BAR TYPE', ['Group', 'Overlay'])
                            if c_2_ == 'Group':
                                c_2 = 'group'
                            else:
                                c_2 = 'overlay'
                        st.text('')
                        c_3 = st.checkbox('SHOW ALL POINTS')
                    plot = BoxPlotM(data, bc, hc1, hc2, c_1, c_2, c_3)
                    st.plotly_chart(plot, use_container_width=True)
            elif plot_type == 'Violin Plot':
                if len(grp4) < 1:
                    st.text('')
                    st.text('')
                    st.error('UNSUFFICIENT NUMBER OF SUITABLE FEATURES FOUND')
                else:
                    bar_option = 'None'
                    hue1_c = 'None'
                    hue2_c = 'None'
                    cont_1 = 'None'
                    cont_2 = 'None'
                    cont_3 = 'None'
                    column1, column2 = st.beta_columns([2, 1])
                    with column1:
                        st.text('')
                        st.text('')
                        st.text('')
                        __h__ = grp4.copy()
                        bar_option = st.selectbox('CHOOSE FEATURE', __h__)
                        ___h___ = grp1.copy()
                        hue1_c = st.selectbox(
                            'CHOOSE HUE FEATURE', ['None']+___h___)
                        if hue1_c != 'None':
                            ____h____ = ___h___.copy()
                            ____h____.remove(hue1_c)
                            hue2_c = st.selectbox(
                                'CHOOSE ANOTHER HUE FEATURE', ['None']+____h____)
                    with column2:
                        st.text('')
                        st.text('')
                        st.text('')
                        st.text('')
                        st.text('')
                        st.text('')
                        cont_1 = st.checkbox('SHOW BOX PLOT')
                        st.text('')
                        if hue2_c != 'None':
                            cont_2_ = st.selectbox('CHOOSE BAR TYPE', [
                                                   'Group', 'Overlay'])
                            cont_2 = cont_2_.lower()
                        st.text('')
                        cont_3 = st.checkbox('SHOW ALL POINTS')
                    plot = ViolinPlotM(
                        data, bar_option, hue1_c, hue2_c, cont_1, cont_2, cont_3)
                    st.plotly_chart(plot, use_container_width=True)
            elif plot_type == 'Dist Plot':
                if len(grp4) < 1:
                    st.text('')
                    st.text('')
                    st.error('UNSUFFICIENT NUMBER OF SUITABLE FEATURES FOUND')
                else:
                    st.text('')
                    st.text('')
                    st.text('')
                    c1, c2 = st.beta_columns(2)
                    cc = 'None'
                    hc = 'None'
                    with c1:
                        cc = st.selectbox('CHOOSE FEATURE', grp4)
                    if cc != 'None':
                        with c2:
                            hc = st.selectbox(
                                'CHOOSE HUE FEATURE', ['None']+grp1)
                    st.text('')
                    st.text('')
                    _, c01, c02 = st.beta_columns([1, 1, 2])
                    hist = 'None'
                    curve = 'None'
                    rug = 'None'
                    with _:
                        hist = st.checkbox('HISTOGRAM', value=True)
                        curve = st.checkbox('CURVE', value=True)
                        rug = st.checkbox('RUGS', value=False)
                    kde = 'kde'
                    bins = 1
                    if curve:
                        with c01:
                            kde = st.radio("CURVE TYPE", ('kde', 'normal'))
                    if hist:
                        with c02:
                            bins = st.slider("NUMBER OF BINS", min_value=1,
                                             max_value=100, value=1, step=1)
                    plot = DistPlotM(data, cc, hc, bins, kde, hist, curve, rug)
                    st.plotly_chart(plot, use_container_width=True)
            elif plot_type == 'Scatter Plot':
                st.text('')
                st.text('')
                st.text('')
                if len(grp4) < 2:
                    st.text('')
                    st.text('')
                    st.error('UNSUFFICIENT NUMBER OF SUITABLE FEATURES FOUND')
                else:
                    _, __, ___ = st.beta_columns([2, 1, 2])
                    with __:
                        sc_t = st.radio(
                            'CHOOSE SCATTER PLOT TYPE', ('2D', '3D'))

                    st.text('')
                    st.text('')

                    if sc_t == '2D':
                        c1, c2 = st.beta_columns(2)
                        feature1 = 'None'
                        feature2 = 'None'
                        hue1 = 'None'
                        hue2 = 'None'
                        hue3 = 'None'
                        trendline = 'None'
                        f1_c = None
                        f2_c = None
                        h1_c = []
                        h2_c = []
                        h3_c = []
                        with c1:
                            f1_c = grp4.copy()
                            feature1 = st.selectbox(
                                'CHOOSE FIRST FEATURE', f1_c)
                        with c2:
                            f2_c = f1_c.copy()
                            f2_c.remove(feature1)
                            feature2 = st.selectbox(
                                'CHOOSE SECOND FEATURE', f2_c)
                        st.text('')
                        c3, c4, c5, c6 = st.beta_columns([2, 2, 2, 1])
                        with c3:
                            h1_c = grp1.copy()
                            hue1 = st.selectbox(
                                'HUE FEATURE 1 (COLOR)', ['None']+h1_c)
                        with c4:
                            h2_c = h1_c.copy()
                            if hue1 != 'None':
                                h2_c.remove(hue1)
                            hue2 = st.selectbox(
                                'HUE FEATURE 2 (SYMBOL)', ['None']+h2_c)
                        with c5:
                            h3_c_ = h2_c.copy()
                            if hue2 != 'None':
                                h3_c_.remove(hue2)
                            for i in h3_c_:
                                if not isinstance(data[i][0], str):
                                    h3_c.append(i)
                            hue3 = st.selectbox(
                                'HUE FEATURE 3 (SIZE)', ['None']+h3_c)
                        with c6:
                            td = st.selectbox(
                                'REGRESSION LINE', ['None', 'Ols', 'Lowess'])
                            if td == 'Ols':
                                trendline = 'ols'
                            elif td == 'Lowess':
                                trendline = 'lowess'
                        plot = ScatterPlotM(
                            data, feature1, feature2, hue1, hue2, hue3, trendline)
                        st.plotly_chart(plot, use_container_width=True)
                    else:
                        if len(grp4) < 3:
                            st.text('')
                            st.text('')
                            st.error(
                                'UNSUFFICIENT NUMBER OF SUITABLE FEATURES FOUND')
                        else:
                            c1, c2, c3 = st.beta_columns(3)
                            feature1 = 'None'
                            feature2 = 'None'
                            feature3 = 'None'
                            hue1 = 'None'
                            hue2 = 'None'
                            hue3 = 'None'
                            f1_c = None
                            f2_c = None
                            f3_c = None
                            h1_c = []
                            h2_c = []
                            h3_c = []
                            with c1:
                                f1_c = grp4.copy()
                                feature1 = st.selectbox(
                                    'CHOOSE FIRST FEATURE', f1_c)
                            with c2:
                                f2_c = f1_c.copy()
                                f2_c.remove(feature1)
                                feature2 = st.selectbox(
                                    'CHOOSE SECOND FEATURE', f2_c)
                            with c3:
                                f3_c = f2_c.copy()
                                f3_c.remove(feature2)
                                feature3 = st.selectbox(
                                    'CHOOSE THIRD FEATURE', f3_c)
                            st.text('')
                            c4, c5, c6 = st.beta_columns(3)
                            with c4:
                                h1_c = grp1.copy()
                                hue1 = st.selectbox(
                                    'HUE FEATURE 1 (COLOR)', ['None']+h1_c)
                            with c5:
                                h2_c = h1_c.copy()
                                if hue1 != 'None':
                                    h2_c.remove(hue1)
                                hue2 = st.selectbox(
                                    'HUE FEATURE 2 (SYMBOL)', ['None']+h2_c)
                            with c6:
                                h3_c_ = h2_c.copy()
                                if hue2 != 'None':
                                    h3_c_.remove(hue2)
                                for i in h3_c_:
                                    if not isinstance(data[i][0], str):
                                        h3_c.append(i)
                                hue3 = st.selectbox(
                                    'HUE FEATURE 3 (SIZE)', ['None']+h3_c)
                            plot = ScatterPlot3DM(
                                data, feature1, feature2, feature3, hue1, hue2, hue3)
                            st.plotly_chart(plot, use_container_width=True)
            elif plot_type == 'Line Plot':
                st.text('')
                st.text('')
                st.text('')
                if len(grp4) < 2:
                    st.text('')
                    st.text('')
                    st.error('UNSUFFICIENT NUMBER OF SUITABLE FEATURES FOUND')
                else:
                    c1, c2 = st.beta_columns(2)
                    feature1 = 'None'
                    feature2 = 'None'
                    hue1 = 'None'
                    hue2 = 'None'
                    hue3 = 'None'
                    f1_c = None
                    f2_c = None
                    h1_c = []
                    h2_c = []
                    h3_c = []
                    with c1:
                        f1_c = grp4.copy()
                        feature1 = st.selectbox(
                            'CHOOSE FIRST FEATURE', f1_c)
                    with c2:
                        f2_c = f1_c.copy()
                        f2_c.remove(feature1)
                        feature2 = st.selectbox(
                            'CHOOSE SECOND FEATURE', f2_c)
                    st.text('')
                    c3, c4, c5 = st.beta_columns(3)
                    with c3:
                        h1_c = grp1.copy()
                        hue1 = st.selectbox(
                            'HUE FEATURE 1 (COLOR)', ['None']+h1_c)
                    with c4:
                        h2_c = h1_c.copy()
                        if hue1 != 'None':
                            h2_c.remove(hue1)
                        hue2 = st.selectbox(
                            'HUE FEATURE 2 (LINE TYPE)', ['None']+h2_c)
                    with c5:
                        h3_c = h2_c.copy()
                        if hue2 != 'None':
                            h3_c.remove(hue2)
                        hue3 = st.selectbox(
                            'HUE FEATURE 3 (LINE GROUPS)', ['None']+h3_c)
                    plot = LinePlotM(
                        data, feature1, feature2, hue1, hue2, hue3)
                    st.plotly_chart(plot, use_container_width=True)
            elif plot_type == 'Area Plot':
                st.text('')
                st.text('')
                st.text('')
                if len(grp4) < 2:
                    st.text('')
                    st.text('')
                    st.error('UNSUFFICIENT NUMBER OF SUITABLE FEATURES FOUND')
                else:
                    c1, c2 = st.beta_columns(2)
                    feature1 = 'None'
                    feature2 = 'None'
                    hue1 = 'None'
                    hue2 = 'None'
                    f1_c = None
                    f2_c = None
                    h1_c = []
                    h2_c = []
                    with c1:
                        f1_c = grp4.copy()
                        feature1 = st.selectbox(
                            'CHOOSE FIRST FEATURE', f1_c)
                    with c2:
                        f2_c = f1_c.copy()
                        f2_c.remove(feature1)
                        feature2 = st.selectbox(
                            'CHOOSE SECOND FEATURE', f2_c)
                    st.text('')
                    c3, c4 = st.beta_columns(2)
                    with c3:
                        h1_c = grp1.copy()
                        hue1 = st.selectbox(
                            'HUE FEATURE 1 (COLOR)', ['None']+h1_c)
                    with c4:
                        h2_c = h1_c.copy()
                        if hue1 != 'None':
                            h2_c.remove(hue1)
                        hue2 = st.selectbox(
                            'HUE FEATURE 2 (LINE GROUP)', ['None']+h2_c)
                    plot = AreaPlotM(
                        data, feature1, feature2, hue1, hue2)
                    st.plotly_chart(plot, use_container_width=True)
            else:
                st.text('')
                st.text('')
                st.text('')
                if len(grp4) < 2:
                    st.text('')
                    st.text('')
                    st.error('UNSUFFICIENT NUMBER OF SUITABLE FEATURES FOUND')
                else:
                    c1, c2 = st.beta_columns(2)
                    feature1 = 'None'
                    feature2 = 'None'
                    hue1 = 'None'
                    hue2 = 'None'
                    hue3 = 'None'
                    f1_c = None
                    f2_c = None
                    h1_c = []
                    h2_c = []
                    h3_c = []
                    with c1:
                        f1_c = grp4.copy()
                        feature1 = st.selectbox(
                            'CHOOSE FIRST FEATURE', f1_c)
                    with c2:
                        f2_c = f1_c.copy()
                        f2_c.remove(feature1)
                        feature2 = st.selectbox(
                            'CHOOSE SECOND FEATURE', f2_c)
                    st.text('')
                    c3, c4, c5 = st.beta_columns(3)
                    with c3:
                        h1_c = ['None', 'Histogram', 'Box', 'Violin', 'Rug']
                        hue1 = st.selectbox(
                            'FACET X PLOT', h1_c)
                        if hue1 != 'None':
                            hue1 = hue1.lower()
                    with c4:
                        h2_c = ['None', 'Histogram', 'Box', 'Violin', 'Rug']
                        hue2 = st.selectbox(
                            'FACET Y PLOT', h2_c)
                        if hue2 != 'None':
                            hue2 = hue2.lower()
                    with c5:
                        h3_c = grp1.copy()
                        hue3 = st.selectbox(
                            'HUE FEATURE', ['None']+h3_c)
                    plot = DensityContourPlotM(
                        data, feature1, feature2, hue1, hue2, hue3)
                    st.plotly_chart(plot, use_container_width=True)
        else:
            _, __, ___, ____ = st.beta_columns([1, 2, 2, 1])
            hmopps = 'None'
            with __:
                hmopps = st.radio(
                    'CHOOSE TYPE', ('CORRELATION', 'PREDICTIVE POWER SCORE'))
            if hmopps == 'CORRELATION':
                type_corr = 'None'
                with ___:
                    type_corr_ = st.selectbox('TYPE OF CORRELATION', [
                                              'Pearson', 'Kendall', 'Spearman'])
                    type_corr = type_corr_.lower()
                plot = HeatMapCorrM(data, type_corr)
                st.plotly_chart(plot, use_container_width=True)
            else:
                plot = HeatMapPpsM(data)
                st.plotly_chart(plot, use_container_width=True)
