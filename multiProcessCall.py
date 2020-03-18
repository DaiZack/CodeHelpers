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
