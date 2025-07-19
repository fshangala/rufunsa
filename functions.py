import pandas as pd
from scipy.stats import fisher_exact


def bitab_fishers_exact_test(data: pd.DataFrame, variables: list[str], column: str) -> pd.DataFrame:
  dfout = pd.DataFrame()

  for variable in variables:
    # Create a DataFrame for the variable
    df1 = pd.DataFrame({"Variable": [variable["name"]]})
    
    # Create a crosstab for the variable and the column
    df2 = pd.crosstab(data[variable["label"]], data[column])
    df2 = df2[["yes", "no"]]
    df2 = df2.sort_index(ascending=False)

    # Create a DataFrame for value labels
    df3 = pd.DataFrame({"Labels": df2.index})
    
    df4 = pd.concat([df1, df3], axis=1)
    
    # Calculate percentages
    df5 = df2.copy()
    offset = 0
    for i in range(df2.columns.size):
      values = [ round((x/df2.iloc[:,i].sum())*100,2) for x in df2.iloc[:,i]]
      df5.insert(i+1+offset, df2.columns[i]+"_perc", value=values)
      offset += 1
    df5 = df5.reset_index(drop=True)
    
    df6 = pd.concat([df4,df5], axis=1)
      
    # Calculate Fisher's exact test
    odds_ratio, p_value = fisher_exact(df2)
    df7 = pd.DataFrame({"p_value": [round(p_value, 2) if p_value > 0.01 else "<0.01"]})

    # Concatenate all DataFrames
    dffinal = pd.concat([df6, df7], axis=1)
    
    dfout = pd.concat([dfout, dffinal], ignore_index=True)

  return dfout