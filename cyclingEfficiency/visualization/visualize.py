import seaborn as sns
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
from matplotlib.axes._axes import Axes
from matplotlib.ticker import FuncFormatter

class Visualize:
    @classmethod
    def hist_one_variable(
            cls, df: DataFrame, column: str,
            bins: int='auto', hue: str = None
        )-> None:

        format = lambda value, tick_number: '{:,.2f}'.format(value)

        beta_y: float = 0.9
        beta_x: float = 0.01

        mean: float = df[column].mean()
        median: float = df[column].median()
        plt.figure(figsize=(8, 5))
        graph: Axes = sns.histplot(
            data=df,
            x=column,
            bins=bins,
            hue=hue,
            multiple='stack'
        )
        ylim: float = graph.get_ylim()[1]
        graph.yaxis.set_major_formatter(FuncFormatter(format))
        graph.xaxis.set_major_formatter(FuncFormatter(format))
        xrange: float = graph.get_xlim()[1] - graph.get_xlim()[0]

        
        plt.axvline(mean, label='Mean', color='#DD0000')
        plt.axvline(median, label='Median', color='#22AA22')
        plt.text(
            mean + xrange * beta_x, ylim * beta_y, '{:,.2f}'.format(mean)
        )
        plt.text(
            median + xrange * beta_x, ylim * beta_y**2, '{:,.2f}'.format(median)
        )
        plt.title('Hist {}'.format(column.upper()))
        plt.legend()
        plt.show()

    @classmethod
    def hist_two_variables(
            cls, df: DataFrame, x: str, y: str,
            bins: int='auto', hue: str = None
        )-> None:
        sns.histplot(
            df, 
            x=x, y=y,
            bins=bins, 
            discrete=(False, False), 
            cbar=True, 
            cbar_kws=dict(shrink=0.9),
            hue=hue
        )
        plt.title('Hist {} vs {}'.format(
            x.upper(), y.upper()
        ))
        plt.show()