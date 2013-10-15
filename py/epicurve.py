# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Epicurves
# ____
# * Caitlin Rivers
# * Virginia Bioinformatics Institute at Virginia Tech
# * [cmrivers@vbi.vt.edu](cmrivers@vbi.vt.edu)
# 
# Epicurve creates weekly, monthly, and daily epicurves (count of new cases over time) from line lists.
# 
# Wish list for improvements:
# 
# * FIX DATETIME HANDLING FOR DAILY EPICURVE

# <codecell>

import pandas as pd
from __future__ import division
import matplotlib.pyplot as plt
from datetime import datetime
from mpltools import style
style.use('ggplot')

# <codecell>

def _date_convert(x, frmt):
    '''
    Convert date given on line list to datetime object
    '''
    try:
        y = datetime.strptime(x, frmt)
    except:
        y = np.nan
        
    return y

# <markdowncell>

# Example data are available in cmrivers/epipy

# <codecell>

epi = pd.read_csv("../Line list & epi stats - Line list.csv", parse_dates=True)
epi['onset_date'] = epi['Approx onset date'].map(lambda x: _date_convert(x, '%Y-%m-%d'))
epi['report_date'] = epi['Approx reporting date'].map(lambda x: _date_convert(x, '%Y-%m-%d'))
epi['dates'] = epi['onset_date'].combine_first(epi['report_date']) #Combine onset and reported date columns, with onset preferential

# <codecell>

def epicurve(df, date_col, freq, title=None, date_format="%Y-%m-%d"):
    '''
    Creates an epicurve (count of new cases over time)

    df = pandas dataframe
    date_col = date used to denote case onset or report date
    freq = desired plotting frequency. Can be day, month or year
    title = optional
    date_format = datetime string format, default is "%Y-%m-%d"
    '''
    freq = freq.lower()[0]  # 'day' -> 'd', 'month' -> 'm', or 'year' -> 'y'; 'd' -> 'd', ...
    df.new_col = df[date_col] #df[date_col].map(lambda x: _date_convert(x, date_format))

    #count the number of cases per time period
    if freq == 'd':
        #broken. datetimes are tricky.
        counts = epi['dates'].value_counts()
        epicurve = pd.DataFrame(df[date_col].value_counts(), columns=['count'])

    elif freq == 'm':
        format_date = df.new_col.dropna().map(lambda x: str(x.strftime("%Y/%m"))) #convert dates to months
        form = format_date.map(lambda x: _date_convert(x, "%Y/%m"))
        epicurve = pd.DataFrame(form.value_counts(), columns=['count']) #count number of cases per month
        
    elif freq == 'y':
        df.new_col = df.new_col.dropna().map(lambda x: x.year) #convert dates to year
        epicurve = pd.DataFrame(df.new_col.value_counts(), columns=['count']) #count number of cases per year
        
    _plot(epicurve, freq, title=date_col)

# <codecell>

def _plot(freq_table, freq, title):
    '''
    Plot number of new cases over time
    freq_table = frequency table of cases by date generated by epicurve()
    freq = inherited from epicurve
    '''
    fig, ax = plt.subplots()
    freq_table['plotdates'] = freq_table.index 

    # care about date formatting
    if freq == 'd':
        wid = .1
        ax.xaxis_date()
        fig.autofmt_xdate()
        
    elif freq == 'm':
        ax.xaxis_date()
        fig.autofmt_xdate()
        wid = len(freq_table)
    
    elif freq == 'y':
        locs = freq_table['plotdates'].values.tolist()
        labels = [str(loc) for loc in locs]
        wid =1 
        ax.set_xticks(locs)
        ax.set_xticklabels(labels)
                
    ax.bar(freq_table['plotdates'].values, freq_table['count'].values, width=wid, align='center')
    ax.set_title(title)

# <codecell>

epicurve(epi, date_col='dates', freq='day')
plt.title('Approximate onset or report date')
#plt.savefig('./day.png')

# <codecell>

epicurve(epi, 'dates', freq='y')

# <codecell>

epicurve(epi, 'dates', freq='month')
plt.title('Approximate onset or report date')
plt.savefig('./month.png')

