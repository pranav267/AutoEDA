import numpy as np
import pandas as pd
import re
import string


def check_number_str(strings):
    regex = '^[0-9]+$'
    for line in strings:
        s = str(line)
        s = s.replace(' ', '')
        if '.' in s:
            s = s.replace('.', '')
        puncts = list(string.punctuation.replace('.', ''))
        for i in list(s):
            if i in puncts:
                return True
        if re.search(regex, s):
            return False
    return True


def check_no(s):
    regex = '^[0-9]+$'
    s = str(s)
    s = s.replace(' ', '')
    f = False
    if '.' in s:
        s = s.replace('.', '')
        f = True
    puncts = list(string.punctuation.replace('.', ''))
    for i in list(s):
        if i in puncts:
            return True, f
    if re.search(regex, s):
        return False, f
    return True, f


def check_skew(df):
    df = df.dropna()
    skew = df.skew()
    if skew == 0:
        return np.round(skew, 2), 'Perfectly Symmetric Distribution', 'No Skew'
    elif skew >= -0.5 and skew <= 0.5:
        if skew < 0:
            return np.round(skew, 2), 'Fairly Symmetric Distribution', 'Lightly Left Skewed'
        else:
            return np.round(skew, 2), 'Fairly Symmetric Distribution', 'Lightly Right Skewed'
    elif skew < -0.5 and skew >= -1:
        return np.round(skew, 2), 'Asymmetric Distribution', 'Moderately Left Skewed'
    elif skew > 0.5 and skew <= 1:
        return np.round(skew, 2), 'Asymmetric Distribution', 'Moderately Right Skewed'
    elif skew < -1:
        return np.round(skew, 2), 'Asymmetric Distribution', 'Highly Left Skewed'
    elif skew > 1:
        return np.round(skew, 2), 'Asymmetric Distribution', 'Highly Right Skewed'


def check_kurtosis(df):
    df = df.dropna()
    kurt = df.kurt()
    out = ''
    if kurt > 10:
        out = 'Too Many Outliers'
    elif kurt <= 0:
        out = 'No Outliers'
    else:
        out = 'Less Outliers'
    if kurt == 3:
        return np.round(kurt, 2), 'Mesokurtic Distribution', 'Similar To Normal Distribution', out
    elif kurt < 3:
        return np.round(kurt, 2), 'Platykurtic Distribution', 'Flat Distribution Wth Moderately Spread Out Values', out
    elif kurt > 3:
        return np.round(kurt, 2), 'Leptokurtic Distribution', 'Tall And Thin Distribution With Values Near Means Or Extremes', out


def stats(df):
    df = df.dropna()
    mean = round(df.mean(), 2)
    median = df.median()
    var = round(df.var(), 2)
    std = round(df.std(), 2)
    min = round(df.min(), 2)
    max = round(df.max(), 2)
    p25 = round(df.quantile(0.25), 2)
    p75 = round(df.quantile(0.75), 2)
    iqr = round(p75 - p25, 2)
    return mean, var, std, min, p25, median, p75, max, iqr


def prepare_text_col(df, lower=True, stp=False, punct=False):
    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
                 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
                 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
                 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
                 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before',
                 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
                 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
                 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't",
                 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't",
                 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn',
                 "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't",
                 'wouldn', "wouldn't"]
    content = ' '.join(list(df.dropna()))
    if lower:
        content = content.lower()
    if punct:
        pattern = re.compile(
            'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        content = pattern.sub(' ', content)
        translator = str.maketrans(
            string.punctuation, ' '*len(string.punctuation))
        content = content.translate(translator)
    content = content.split()
    if stp:
        content = [i.strip() for i in content if i not in stopwords]
    word_counts = {}
    for i in content:
        if i in word_counts:
            word_counts[i] = word_counts[i] + 1
        else:
            word_counts[i] = 1
    word_c = pd.DataFrame()
    word_c['Elements'] = word_counts.keys()
    word_c['Counts'] = word_counts.values()
    word_c = word_c.sort_values(
        'Counts', ascending=False).reset_index(drop=True)
    return word_c


def get_grps(df):
    grp1 = []
    grp2 = []
    grp3 = []
    grp4 = []
    cat_cols = list(df.select_dtypes(include='object').columns)
    num_cols = list(df.select_dtypes(exclude='object').columns)

    for i in cat_cols:
        t = df[i].dropna()
        if not check_number_str(t):
            num_cols.append(i)
            cat_cols.remove(i)

    cat_cols_p = []
    for i in num_cols:
        if len(df[i].unique()) <= 10:
            cat_cols_p.append(i)

    for i in df.columns:
        if i in cat_cols or i in cat_cols_p:
            if len(df[i].unique()) <= 15:
                grp1.append(i)
            else:
                grp2.append(i)
        else:
            if len(df[i].unique()) <= 15:
                grp3.append(i)
            else:
                grp4.append(i)
    return grp1, grp2, grp3, grp4
