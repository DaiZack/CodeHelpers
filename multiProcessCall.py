
from py2neo import Graph
import pandas as pd
from multiprocessing import Pool

df = pd.read_csv('/var/rel8ed.to/nfs/share/MexicoCensus.csv', encoding='Latin1')

def predict(region,naics, productivity):
    print(region,naics, productivity)
    # region,naics, productivity = line[0],line[1],line[2]
    g = Graph('bolt://10.8.0.58:7687', user='', password='')
    query = 'match (a:Address)<-[:LOCATED_IN]-(c:Corp)-[:ATTRIBUTED_BY]->(m:Metric {name:"employees"}), (c)-[:CAT]->(ct:Category) where a.region = "%s" and substring(ct.code, 0,3) = "%s" return id(c) as idc, a.region as region, ct.code as naics, m.count as emp, "%s" as productivity, toFloat(m.count)*%s as sales' % ( region,naics, productivity,productivity)
    resutlt = g.run(query).to_data_frame()
    return resutlt
    # if len(resutlt)>0:
    #     resutlt.to_csv('MexicoSalesPredict2.csv', index=0, header=(i==0), mode='a')

jobs = [(str(df.loc[i,'Naics']),str(df.loc[i,'stateABBREV']),str(df.loc[i,'productivity'])) for i in df.index]

p = Pool(10)
for resutlt in p.imap(predict, jobs):
    print(len(resutlt))
    if len(resutlt)>0:
        resutlt.to_csv('MexicoSalesPredict2.csv', index=0, header=False, mode='a')








''' older code
from py2neo import Graph 
from multiprocessing import Pool

g= Graph('bolt://10.8.0.102:7687', user='', password='')
regions = ['ON','QC','NS','NB','MB','BC','PE','SK','AB','NL','YK', 'YT', 'NT', 'NU']
states = ['AK','AL','AR','AS','AZ','CA','CO','CT','DC','DE','FL','GA','HI','IA','ID','IL','IN','KS','KY','LA','MA','MD','ME','MI','MN','MO','MP','MS','MT','NC','ND','NE','NH','NJ','NM','NV','NY','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VA','VT','WA','WI','WV','WY','VI','PR','GU','MH', 'FM']

def callneo(region):
    print(region, 'start')
    query = 'match (A:Address {region:"%s"}) return count(A) as num' % str(region)
    data = g.run(query).data()
    return {region: data[0]['num']}

with Pool(processes=4) as pool:
    multiple_results = [pool.apply_async(callneo, (region,)) for region in regions]
    print([res.get() for res in multiple_results])

with Pool(processes=4) as pool:
    multiple_results = [pool.apply_async(callneo, (region,)) for region in states]
    print([res.get() for res in multiple_results])
'''
