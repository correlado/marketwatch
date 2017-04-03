from markets import Market
    
    
if __name__ == '__main__':
    
    
    m = Market()
    hd = m.full_historic_data()
    hd['next_price']=hd['price'].shift(-1) #target
    hd['increase']=(hd['next_price']-hd['price'])/hd['price']>0.01 #increase at least by 1%
    
    features = ['date','volume24','marketCap','availableSupplyNumber','price','next_price','increase']
    
    hd[features].to_csv('~/Data/crypto/ETH.csv',index=False)
    
    print "done"
