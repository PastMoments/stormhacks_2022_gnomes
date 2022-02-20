import pandas as pd
import matplotlib.pyplot as plt


# Graphing
def graph_bal(data, x, y):
    data.plot(
        x=x,
        y=y,
        figsize=(10, 5)
    )

    plt.title("Overall Result")
    plt.xlabel(x)
    plt.ylabel(y)

    plt.show()


# pre-process data for the withdrawal and deposit plots
def data_for_graph(df, col):    # col = df.columns[n]
    data = {
        "Date": df[df.columns[0]],
        col: []
    }
    sum = 0

    for i in range(len(df)):
        df[col] = df[col].fillna(0)
        sum += df.loc[i, col]
        data[col].append(sum)

    result = pd.DataFrame(data)
    return result


if __name__ == "__main__":
    df = pd.read_csv('test.csv', sep=',')
    df.columns = ['Date', 'Description', 'Withdrawal', 'Deposit', 'Balance']

    wd = data_for_graph(df, df.columns[2])
    dp = data_for_graph(df, df.columns[3])

    # graphing
    # graph_bal(df, df.columns[0], df.columns[4])   # balance graph
    graph_bal(wd, wd.columns[0], wd.columns[1])     # withdrawal graph
    # graph_bal(dp, dp.columns[0], dp.columns[1])   # deposit graph
