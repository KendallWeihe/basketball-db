import numpy as np
import pdb
import os

directories = os.listdir("/home/kendall/Development/nba-basketball-db/advanced-seasons/")

for d in directories:
    if d != "2012":
        files = os.listdir("/home/kendall/Development/nba-basketball-db/advanced-seasons/"+d)
        for f in files:
            data = np.genfromtxt("/home/kendall/Development/nba-basketball-db/advanced-seasons/"+d+"/"+f, delimiter=",")

            if data.shape[0] == 47:
                continue

            # if d == "2017" and f == "Golden-State.csv":
            #     pdb.set_trace()
            #     print

            try:
                data = data[::-1,:]
            except:
                pdb.set_trace()
                print

            accumulated_data = []
            for row in range(1,data.shape[0]+1):
                # accumulated_data.append(np.mean(data[0:row,:], axis=0))
                row_data = []
                for column in range(data.shape[1]):
                    # if column != 0 and column != 46 and column != 43:
                    if column != 0 and column != 29 and column != 32:
                        row_data.append(np.mean(data[0:row,column]))
                    else:
                        row_data.append(data[row-1,column])
                accumulated_data.append(row_data)

            accumulated_data = np.array(accumulated_data)[::-1,:]

            try:
                os.mkdir("/home/kendall/Development/nba-basketball-db/advanced-accumulated/"+d)
            except:
                pass
            np.savetxt("/home/kendall/Development/nba-basketball-db/advanced-accumulated/"+d+"/"+f, accumulated_data, delimiter=",")
