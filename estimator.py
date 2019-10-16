def estimator(data, features, target, groupby='', quantile=0.9, corr=False):
  data = data.fillna(0)
  if groupby:
    option = list(set(data[groupby]))
    newdata = pd.DataFrame()
    for op in option:
      subdata =  data[data[groupby]==op]
      scaleddata = (subdata[features]-subdata[features].min())/(subdata[features].max()-subdata[features].min())
      scores = scaleddata.agg("mean", axis="columns")
      if subdata[target].quantile(quantile) >2:
        subdata.loc[:,'pred_'+target] = scores*(subdata[target].quantile(quantile)-subdata[target].quantile(1-quantile))+subdata[target].quantile(1-quantile)
      else:
        subdata.loc[:,'pred_'+target] = scores*(data[target].quantile(quantile)-data[target].quantile(1-quantile))+data[target].quantile(1-quantile)
      newdata = pd.concat([newdata, subdata])
    return newdata
  else:
    scaleddata = (data[features]-data[features].min())/(data[features].max()-data[features].min())
    scores = scaleddata.agg("mean", axis="columns")
    data.loc[:,'pred_'+target] = scores*(data[target].quantile(quantile)-data[target].quantile(1-quantile))+data[target].quantile(1-quantile)
    return data
      
