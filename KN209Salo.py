import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dateutil
from collections import Counter
from matplotlib.dates import DayLocator, DateFormatter


def showGraphs(df):
    print("Graphs that could be shown:")
    for i in range(1, len(df.columns)):
        print( str(i) + ')' + ' - ' + str(df.columns[i]))
    print("Enter what graphs you want to be shown using their number:")
    selected_graphs = np.array(list(map(int, input().split())))
    timeline = pd.to_datetime(df.index.astype(str) + ' ' + df['Time'].astype(str))

    for col in selected_graphs:
        if type(df.iloc[0, col]) is not str:
            x = timeline
            y = np.array(df.iloc[:, col])

            ax = plt.figure().add_subplot()
            ax.plot(x, y, label=df.columns[col])

            ax.xaxis.set_major_locator(DayLocator())
            ax.xaxis.set_major_formatter(DateFormatter("%d %b"))
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
            plt.ylabel(df.columns[col])

            ax.grid(which='major', color='black')
            ax.grid(which='minor', linestyle='dotted')
            ax.minorticks_on()

            plt.legend()
        else:
            fig, ax = plt.subplots()

            dictionary = Counter(df.iloc[:, col])
            keys = np.array(list(dictionary.keys()))
            values = np.array(list(dictionary.values()))

            ax.pie(values, radius=1, startangle=90)
            ax.set(aspect="equal", title=df.columns[col])
            plt.legend(labels=keys, bbox_to_anchor=(1, 1))

        plt.show()



def numbersConversion(df):
    for column in ['Humidity', 'Wind Speed', 'Wind Gust']:
        df[column] = df[column].replace('\D', '', regex=True).astype(int)
    df['Pressure'] = df['Pressure'].replace(',', '.', regex=True).astype(float)


def timeConversion(df):
    for i in range(df.shape[0]):
        df.loc[i, 'Time'] = dateutil.parser.parse(df.loc[i, 'Time'])
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M').dt.time


def dateConversion(df):
    for i in range(df.shape[0]):
        df.loc[i, 'day/month'] = dateutil.parser.parse(df.loc[i, 'day/month'] + '2019').date()


def dataParsing(df):
    numbersConversion(df)
    timeConversion(df)
    dateConversion(df)
    df.set_index('day/month', inplace=True)
    return df

dataframe = pd.read_csv('DATABASE.csv', sep=';')
parseddata = dataParsing(dataframe)
showGraphs(parseddata)
