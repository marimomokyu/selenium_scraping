# coding:utf-8
import pandas as pd
hoge = pd.read_csv('/Users/tsutsumi/csv/親情報_1000件以上.csv')

# データフレーム型に格納
df = pd.DataFrame(hoge)

#重複を確認
df.duplicated()

#重複を削除
sindf = df.drop_duplicates()
sindf

# CSVで保存
sindf.to_csv('/Users/tsutsumi/csv/親情報_1000件以上_重複削除.csv', index=False, encoding='utf-8-sig')