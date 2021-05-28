import random
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.colors as mplc
import ppscore as pps
import warnings
warnings.filterwarnings('ignore')


def MissingData(df):
    t = df.sort_values('Counts')
    return px.bar(t, x='Columns', y='Counts', color_discrete_sequence=['#EDF1FF'], title='MISSING VALUES MATRIX')


def CountPlot(df, feature):
    df = df[df[feature].notna()]
    return px.histogram(data_frame=df, x=feature, color=feature, color_discrete_sequence=px.colors.qualitative.Light24[2:], title='CLASS COUNTS')


def PieChart(df, feature):
    df = df[df[feature].notna()]
    df = df.groupby(feature)[[feature]].count()
    df.columns = ['Count']
    df = df.reset_index()
    return px.pie(data_frame=df, values='Count', names=feature, color_discrete_sequence=px.colors.qualitative.Light24[2:], title='CLASS DISTRIBUTIONS', hole=0.5)


def DistPlot(df, feature, bin_size, curve_type):
    df = df[df[feature] < df[feature].quantile(0.99)]
    df = df[df[feature].notna()]
    df = df.groupby(feature)[[feature]].count()
    df.columns = ['Count']
    df = df.reset_index()
    t = [df[feature].tolist()]
    group_labels = [f'{feature.capitalize()} Distribution']
    fig = ff.create_distplot(t, group_labels, colors=[
                             '#F5DF4D'], bin_size=bin_size, curve_type=curve_type)
    fig.update_layout(title='DISTRIBUTION HISTOGRAM')
    return fig


def BoxViolinSwarmPlot(df, feature):
    df = df[df[feature].notna()]
    return px.violin(df, x=feature, box=True, points="all", color_discrete_sequence=['#F96714'], title='FEATURE DISTRIBUTION')


def BarPlot(df):
    df_ = df.head(10)
    return px.bar(df_, x='Elements', y='Counts', color_discrete_sequence=['#79C753'], title='MOST FREQUENT ELEMENTS')


def LenPlot(df, feature, bins):
    df = df.dropna()
    df['Length'] = df[feature].str.len().values
    return px.histogram(df, x="Length", nbins=bins, color_discrete_sequence=['#91A8D0'], title='LENGTH DISTRIBUTION')


def BarPlotM(df, feature, bar_mode, hue=None):
    if hue == None:
        t = df[[feature]].dropna()
        t = t.groupby(feature)[[feature]].count()
        t.columns = ['Count']
        l = len(t)
        t = t.reset_index()
        return px.bar(t, x=feature, y='Count', color=feature, color_discrete_sequence=px.colors.qualitative.Dark24, barmode=bar_mode)
    else:
        ct = pd.crosstab(df[feature], df[hue])
        cols = ct.columns
        ct = ct.reset_index()
        l = len(ct)
        return px.bar(ct, x=feature, y=cols, barmode=bar_mode, color_discrete_sequence=px.colors.qualitative.Dark24)


def PieChartM(df, feature, h):
    df = df[df[feature].notna()]
    df = df.groupby(feature)[[feature]].count()
    df.columns = ['Count']
    df = df.reset_index()
    return px.pie(data_frame=df, values='Count', names=feature, color_discrete_sequence=px.colors.qualitative.Alphabet[2:], hole=h)


def BoxPlotM(df, y, x, color, notched, boxmode, points):
    df = df.dropna()
    p = 'outliers'
    if points:
        p = 'all'
    if x == 'None' and color == 'None':
        if boxmode == 'None':
            return px.box(df, x=y, notched=notched, points=p, color_discrete_sequence=px.colors.qualitative.Light24)
        return px.box(df, x=y, notched=notched, boxmode=boxmode, points=p, color_discrete_sequence=px.colors.qualitative.Light24)
    elif color == 'None':
        if boxmode == 'None':
            return px.box(df, y=y, x=x, notched=notched, points=p, color_discrete_sequence=px.colors.qualitative.Light24)
        return px.box(df, y=y, x=x, notched=notched, boxmode=boxmode, points=p, color_discrete_sequence=px.colors.qualitative.Light24)
    else:
        if boxmode == 'None':
            return px.box(df, y=y, x=x, color=color, notched=notched, points=p, color_discrete_sequence=px.colors.qualitative.Light24)
        return px.box(df, y=y, x=x, color=color, notched=notched,
                      boxmode=boxmode, points=p, color_discrete_sequence=px.colors.qualitative.Light24)


def ViolinPlotM(df, y, x, color, box, violinmode, points):
    df = df.dropna()
    p = 'outliers'
    if points:
        p = 'all'
    if x == 'None' and color == 'None':
        if violinmode == 'None':
            return px.violin(df, x=y, box=box, points=p, color_discrete_sequence=px.colors.qualitative.Vivid)
        return px.violin(df, x=y, box=box, violinmode=violinmode, points=p, color_discrete_sequence=px.colors.qualitative.Vivid)
    elif color == 'None':
        if violinmode == 'None':
            return px.violin(df, y=y, x=x, box=box, points=p, color_discrete_sequence=px.colors.qualitative.Vivid)
        return px.violin(df, y=y, x=x, box=box, violinmode=violinmode, points=p, color_discrete_sequence=px.colors.qualitative.Vivid)
    else:
        if violinmode == 'None':
            return px.violin(df, y=y, x=x, color=color, box=box, points=p, color_discrete_sequence=px.colors.qualitative.Vivid)
        return px.violin(df, y=y, x=x, color=color, box=box,
                         violinmode=violinmode, points=p, color_discrete_sequence=px.colors.qualitative.Vivid)


def DistPlotM(df, feature, hue, bin_size, curve_type, show_hist, show_curve, show_rug):
    df = df[df[feature] < df[feature].quantile(0.99)]
    if hue != 'None':
        data = []
        labels = []
        cats = df[hue].unique()
        for c in cats:
            t = df.copy()
            t = t[t[hue] == c]
            t = t.groupby(feature)[[feature]].count()
            t.columns = ['Count']
            t = t.reset_index()
            data.append(t[feature].tolist())
            labels.append(f'{feature.capitalize()} : {str(c)}')
        fig = ff.create_distplot(
            data, labels, bin_size=bin_size, curve_type=curve_type, show_hist=show_hist, show_curve=show_curve, show_rug=show_rug)
        return fig
    else:
        data = []
        labels = []
        t = df.copy()
        t = t.groupby(feature)[[feature]].count()
        t.columns = ['Count']
        t = t.reset_index()
        data.append(t[feature].tolist())
        labels.append(f'{feature.capitalize()}')
        fig = ff.create_distplot(
            data, labels, bin_size=bin_size, curve_type=curve_type, colors=['#00A170'], show_hist=show_hist, show_curve=show_curve, show_rug=show_rug)
        return fig


def ScatterPlotM(df, feature1, feature2, hue1, hue2, hue3, trendline='None'):
    df = df.dropna()
    if trendline == 'None':
        if hue1 == 'None' and hue2 == 'None' and hue3 == 'None':
            return px.scatter(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Pastel)
        elif hue2 == 'None' and hue3 == 'None':
            return px.scatter(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Pastel, color=hue1)
        elif hue1 == 'None' and hue3 == 'None':
            return px.scatter(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Pastel, symbol=hue2)
        elif hue1 == 'None' and hue2 == 'None':
            return px.scatter(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Pastel, size=hue3)
        elif hue1 == 'None':
            return px.scatter(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Pastel, symbol=hue2, size=hue3)
        elif hue2 == 'None':
            return px.scatter(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Pastel, color=hue1, size=hue3)
        elif hue3 == 'None':
            return px.scatter(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Pastel, color=hue1, symbol=hue2)
        else:
            return px.scatter(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Pastel, color=hue1, symbol=hue2, size=hue3)
    else:
        if hue1 == 'None' and hue2 == 'None' and hue3 == 'None':
            return px.scatter(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Pastel, trendline=trendline)
        elif hue2 == 'None' and hue3 == 'None':
            return px.scatter(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Pastel, color=hue1, trendline=trendline)
        elif hue1 == 'None' and hue3 == 'None':
            return px.scatter(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Pastel, symbol=hue2, trendline=trendline)
        elif hue1 == 'None' and hue2 == 'None':
            return px.scatter(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Pastel, size=hue3, trendline=trendline)
        elif hue1 == 'None':
            return px.scatter(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Pastel, symbol=hue2, size=hue3, trendline=trendline)
        elif hue2 == 'None':
            return px.scatter(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Pastel, color=hue1, size=hue3, trendline=trendline)
        elif hue3 == 'None':
            return px.scatter(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Pastel, color=hue1, symbol=hue2, trendline=trendline)
        else:
            return px.scatter(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Pastel, color=hue1, symbol=hue2, size=hue3, trendline=trendline)


def ScatterPlot3DM(df, feature1, feature2, feature3, hue1, hue2, hue3):
    df = df.dropna()
    if hue1 == 'None' and hue2 == 'None' and hue3 == 'None':
        return px.scatter_3d(df, feature1, feature2, feature3, color_discrete_sequence=px.colors.qualitative.Vivid)
    elif hue2 == 'None' and hue3 == 'None':
        return px.scatter_3d(df, feature1, feature2, feature3, color_discrete_sequence=px.colors.qualitative.Vivid, color=hue1)
    elif hue1 == 'None' and hue3 == 'None':
        return px.scatter_3d(df, feature1, feature2, feature3, color_discrete_sequence=px.colors.qualitative.Vivid, symbol=hue2)
    elif hue1 == 'None' and hue2 == 'None':
        return px.scatter_3d(df, feature1, feature2, feature3, color_discrete_sequence=px.colors.qualitative.Vivid, size=hue3)
    elif hue1 == 'None':
        return px.scatter_3d(df, feature1, feature2, feature3, color_discrete_sequence=px.colors.qualitative.Vivid, symbol=hue2, size=hue3)
    elif hue2 == 'None':
        return px.scatter_3d(df, feature1, feature2, feature3, color_discrete_sequence=px.colors.qualitative.Vivid, color=hue1, size=hue3)
    elif hue3 == 'None':
        return px.scatter_3d(df, feature1, feature2, feature3, color_discrete_sequence=px.colors.qualitative.Vivid, color=hue1, symbol=hue2)
    else:
        return px.scatter_3d(df, feature1, feature2, feature3, color_discrete_sequence=px.colors.qualitative.Vivid, color=hue1, symbol=hue2, size=hue3)


def LinePlotM(df, feature1, feature2, hue1, hue2, hue3):
    df = df.dropna()
    if hue1 == 'None' and hue2 == 'None' and hue3 == 'None':
        return px.line(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Safe)
    elif hue2 == 'None' and hue3 == 'None':
        return px.line(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Safe, color=hue1)
    elif hue1 == 'None' and hue3 == 'None':
        return px.line(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Safe, line_dash=hue2)
    elif hue1 == 'None' and hue2 == 'None':
        return px.line(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Safe, line_group=hue3)
    elif hue1 == 'None':
        return px.line(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Safe, line_dash=hue2, line_group=hue3)
    elif hue2 == 'None':
        return px.line(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Safe, color=hue1, line_group=hue3)
    elif hue3 == 'None':
        return px.line(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Safe, color=hue1, line_dash=hue2)
    else:
        return px.line(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Safe, color=hue1, line_dash=hue2, line_group=hue3)


def AreaPlotM(df, feature1, feature2, hue1, hue2):
    df = df.dropna()
    if hue1 == 'None' and hue2 == 'None':
        return px.area(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Dark24)
    elif hue2 == 'None':
        return px.area(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Dark24, color=hue1)
    elif hue1 == 'None':
        return px.area(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Dark24, line_group=hue2)
    else:
        return px.area(df, feature1, feature2, color_discrete_sequence=px.colors.qualitative.Dark24, color=hue1, line_group=hue2)


def DensityContourPlotM(df, feature1, feature2, mx, my, c):
    df = df.dropna()
    if mx == 'None' and my == 'None' and c == 'None':
        return px.density_contour(df, x=feature1, y=feature2, color_discrete_sequence=px.colors.qualitative.Light24)
    elif my == 'None' and c == 'None':
        return px.density_contour(df, x=feature1, y=feature2, marginal_x=mx, color_discrete_sequence=px.colors.qualitative.Light24)
    elif mx == 'None' and c == 'None':
        return px.density_contour(df, x=feature1, y=feature2, marginal_y=my, color_discrete_sequence=px.colors.qualitative.Light24)
    elif mx == 'None' and my == 'None':
        return px.density_contour(df, x=feature1, y=feature2, color=c, marginal_y=my, color_discrete_sequence=px.colors.qualitative.Light24)
    elif my == 'None':
        return px.density_contour(df, x=feature1, y=feature2, color=c, marginal_x=mx, color_discrete_sequence=px.colors.qualitative.Light24)
    elif c == 'None':
        return px.density_contour(df, x=feature1, y=feature2, marginal_x=mx, marginal_y=my, color_discrete_sequence=px.colors.qualitative.Light24)
    else:
        return px.density_contour(df, x=feature1, y=feature2, color=c, marginal_x=mx, marginal_y=my, color_discrete_sequence=px.colors.qualitative.Light24)


def HeatMapCorrM(df, type_corr):
    cor = df.corr(method=type_corr)
    cor = cor.round(2)
    x = cor.index.tolist()
    y = cor.columns.tolist()
    cor = cor.values.tolist()
    if type_corr == 'spearman':
        return ff.create_annotated_heatmap(cor, x=x, y=y, colorscale='YlGnBu')
    elif type_corr == 'kendall':
        return ff.create_annotated_heatmap(cor, x=x, y=y, colorscale='PuBuGn')
    else:
        return ff.create_annotated_heatmap(cor, x=x, y=y, colorscale='YlOrRd')


def HeatMapPpsM(df):
    matrix_df = pps.matrix(df)[['x', 'y', 'ppscore']].pivot(
        columns='x', index='y', values='ppscore')
    matrix_df = matrix_df.apply(lambda x: round(x, 2))
    x = matrix_df.index.tolist()
    y = matrix_df.columns.tolist()
    cor = matrix_df.values.tolist()
    return ff.create_annotated_heatmap(cor, x=x, y=y, colorscale='PuRd')
