# encoding:GBK
import pandas as pd
from ricco import rdf
from ricco import reset2name


class BaseTransformer(object):
    def __init__(self, df):
        if isinstance(df, str):
            self.df = rdf(df)
        elif isinstance(df, pd.DataFrame):
            self.df = df
        else:
            ValueError('������Dataframe��·��')


class Data_process(BaseTransformer):
    def reset2name(df):
        df = reset2name(df)
        return df

    def to_gbk(self, finame: str):
        self.df.to_csv(finame, index=False, encoding='GBK')
        return self.df

# if __name__ == '__main__':
#     # df = rdf('�Ϻ����ص�λ.csv')
#     df = '�Ϻ����ص�λ.csv'
#
#     a = Data_process(df)
#     a.reset2name()
#     # a.to_gbk('tes.csv')
#     print(a.df)
