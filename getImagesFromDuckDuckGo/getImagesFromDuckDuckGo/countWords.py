import pandas as pd
import re
import os
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
imageURLs_path = os.path.join(script_dir, 'imageURLs.csv')
wordCount_path = os.path.join(script_dir, 'wordCount.csv')

if __name__ == "__main__":
    print("countWords")
    dfW = pd.read_csv(imageURLs_path, header=None)
    dfC = pd.read_csv(wordCount_path, header=None)
    dfC.iloc[:, 1] = 0

    rowCount = dfW.shape[0]
    for i in range(rowCount):
        sntnc = dfW.iloc[i,0]
        wrds = re.findall(r"[A-Za-z]+", sntnc)
        for wrd in wrds:
            if wrd in dfC.iloc[:, 0].values:
                # 存在するなら2列目を+1
                dfC.loc[dfC.iloc[:, 0] == wrd, 1] += 1
            else:
                # 存在しないなら行を追加
                dfC.loc[len(dfC)] = [wrd, 1]

            #print(dfC)
            #time.sleep(1)

    dfC_sorted = dfC.sort_values(by = 1, ascending = False, kind = "mergesort").reset_index(drop = True)

    dfC_sorted.to_csv(wordCount_path, index = False, header = False)