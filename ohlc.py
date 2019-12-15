import argparse
import datetime
import sys
import pandas as pd


def createParser():
    parser = argparse.ArgumentParser(
        prog='ohlc.py',
        description='''Finally, I done this program. I did not sleep night, but i did this''',
        epilog='''(c) Author of this program stupid and irresponsible ''',
        add_help=False
    )

    parent_group = parser.add_argument_group(title='Команды')

    parent_group.add_argument('--help', '-h', action='help',
                              help='Справка')

    parent_group.add_argument('--full info', '-fi', help='Информация о используемых функциях')

    file_group = parser.add_argument_group(title='Параметры')

    file_group.add_argument('--file', '-f',
                            help='Путь к файлу',
                            type=argparse.FileType())

    file_group.add_argument('--timeframe', '-tf',
                            help='Маштаб свечного графика',
                            metavar='ВРЕМЯ',
                            type=str)

    file_group.add_argument('--tickets', '-t',
                            help='Название тикетов',
                            type=str,
                            nargs='+')

    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    print(namespace)

    text = namespace.file
    tickets = namespace.tickets
    timeframe = namespace.timeframe
    df = pd.read_csv(text, names=['Company', 'Price', 'Amount', 'DateTime'])


df['Dates'] = pd.to_datetime(df['DateTime']).dt.date
df['Time'] = pd.to_datetime(df['DateTime']).dt.time

df = df[(df['Time'] >= datetime.time(7, 0, 0)) & (df['Time'] <= datetime.time(23, 59, 59, 999999)) |
        (df['Time'] >= datetime.time(0, 0, 0)) & (df['Time'] <= datetime.time(2, 59, 59, 999999))]

df['DateTime'] = pd.to_datetime(df['DateTime'])
df = df.set_index('DateTime')
df = df.drop(columns=['Dates', 'Time', 'Amount'])


def trades(df1, timeframe, tickets):
    timeframe += 'Min'
    data = pd.DataFrame()
    for i in range(len(tickets)):
        t = tickets[i]
        tickets[i] = df1[df1['Company'] == tickets[i]]
        tickets[i] = pd.DataFrame(tickets[i])
        tickets[i] = tickets[i]['Price'].resample(timeframe).ohlc()
        tickets[i]['Company'] = t
        data = data.append(tickets[i])
    data = data.query("open != 'NaN'")
    data.sort_values(["DateTime"], inplace=True)
    data = data.reset_index()
    data = data.set_index('Company')
    data = data.reset_index()
    return data.to_csv()


print(trades(df, timeframe, tickets))
