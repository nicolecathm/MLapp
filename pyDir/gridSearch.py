def clean_dataset(df):
    # code to remove : INFINITY, NaN, bad data! 
    # sent from Tyler Balson in Zoom, also found on stackoverflow 
    # https://stackoverflow.com/a/46581125  
    import numpy as np
    import pandas as pd
    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    df.dropna(inplace=True)
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
    return df[indices_to_keep].astype(np.float64)

def cleand ( filename ):
  # takes filename --> returns training data, testing data, unsplit dataframe 

  # read in csv file w pandas dataframe
  # removes date columb that breaks clean_dataset function
  # creates new date index column to use as feature
  # divides ticket_price and total_sales by 1e4
  import pandas as pd
  from sklearn.model_selection import train_test_split

  data = pd.read_csv(filename)            # reads in as pandas df

  data = data.drop(columns = ['date'])    # removes problematic date column, uses quarter as time feature
  data = clean_dataset(data)              # removes any nan or infinity 



  # combines the month and day colums to a day index (1 - 365)
  # doesn't account for leap year, in my opinion this one day out of a year is negligible
  month = {1: 0, 2: 31, 3: 59, 4: 90, 5: 120, 6: 151, 7: 181, 8: 212, 9:243, 10: 273, 11: 304, 12: 334 }
  days = []
  for x in range(0, len(data)):
    i = data['month'].iloc[x]
    y = data['day'].iloc[x]
    days.append(month[i] + y)

  data["day_index"] = days # add day columb to dataframe



  # fix imbalance in ticket_price, and total_sales, off by factor of 4?

  for i in range(0, len(data)):
    data['total_sales'].iloc[i]/=1e4
    data['ticket_price'].iloc[i]/=1e4

  datax = data[[ 'ticket_price', 'day_index', 'show_time', 'capacity', 'month', 'quarter', 'day']]
  datay = data['total_sales']
  return datax, datay

if __name__ == "__main__":
   from sklearn import svm
   import numpy as np
   from scipy.stats import uniform
   from sklearn.model_selection import RandomizedSearchCV

   datax, datay = cleand('cinemaTicket_Ref.csv')
   print("\n~~~~Data Cleaned~~~~\n")

   mySVR = svm.SVR()
   C = np.logspace(0,4,10)
   hyperparameters = dict(C=C)

   randsearch = RandomizedSearchCV(mySVR, hyperparameters, random_state=0, n_iter=100, cv=5, verbose = 1, n_jobs=-1)
   print("\n~~~~Random Search init~~~~\n")

   from joblib import dump, load

   best_model = randsearch.fit(datax, datay)
   dump(best_model, 'bestMod.pkl')
   print("\n~~~~SUCCESS: Model pickled~~~~\n")
                                            
