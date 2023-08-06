import pandas as pd

import humailib.utils as hu
import humailib.hasher as hh
from humailib.cloud_tools import GoogleCloudStorage, GoogleBigQuery

class CustomerIDFromNameAddressEmail:
    
    def __init__(self):
        self.cid = 0
        self.customer_id_lookup = {}
        self.customer_table = []
        
    def generate(
        self, 
        df, name_col='Name', addr_col='Address', email_col='Email', 
        verbose=False
    ):
      
        num_new = 0
        ii = 1
        n = df[name_col].nunique()
        cids = {}
        
        dfg = df[[name_col, addr_col, email_col, 'Transaction_ID']].groupby(by=[name_col])
        
        if verbose:
            print("0/{:,} ({:.2f}%)".format(n, 0))
        
        for name, data in dfg:
            #print(name)
            
            name = name.strip().upper()
    
            if verbose and ii % 5000 == 0:
                print("{:,}/{:,} ({:.2f}%) New IDs created: {:,}".format(ii, n, 100.0*ii/n, num_new))

            id_by_email = {}
            id_by_addr = {}
            if name in self.customer_id_lookup:
                id_by_email, id_by_addr = self.customer_id_lookup[name]
    
            for index, row in data.iterrows():
                new_email = row[email_col].strip().upper()
                new_addr = row[addr_col].strip().upper()
                if not new_email in id_by_email and not new_addr in id_by_addr:
                    id_by_email[ new_email ] = self.cid
                    id_by_addr[ new_addr ] = self.cid
                    #print(cid)
                    #cids.append(self.cid)
                    cids[str(row['Transaction_ID'])] = self.cid
                    
                    self.customer_table.append([self.cid, name, new_email, new_addr])
                    self.cid = 1 + self.cid
                    num_new = 1 + num_new
                else:
                    if new_email in id_by_email:
                        id_by_addr[ new_addr ] = id_by_email[ new_email ]
                    elif new_addr in id_by_addr:
                        id_by_email[ new_email ] = id_by_addr[ new_addr ]

                    #print(addr[ ad ])
                    #cids.append( id_by_addr[ new_addr ] )
                    cids[str(row['Transaction_ID'])] = id_by_addr[new_addr]
                    
                    #if name == 'MIRANDA VEREGGEN':
                    #    print("Miranda: {}".format(id_by_addr[new_addr]))
                        
                #if self.cid == '91962' or id_by_addr[new_addr] == '91962':
                #    print("91962: {}".format(name))

            self.customer_id_lookup[name] = [id_by_email, id_by_addr]

            ii = 1 + ii
            
        if verbose:
            print("{:,}/{:,} ({:.2f}%). New IDs created: {:,}".format(n, n, 100.0, num_new))
    
        return cids
    
    def get_customer_id_table(self):
        
        if self.customer_table is not None:
            
            data = [tuple(c) for c in self.customer_table]
            df = pd.DataFrame(data, columns=['Customer_ID','Name','Email','Address'])
            hu.columns_as_str(df, columns=['Customer_ID', 'Name','Email','Address'])
            
            return df
        
        return None
    
    def upload_and_replace(self, dataset_table_name, gbq):
        
        if self.customer_table is None or self.customer_id_lookup is None:
            return
        
        if gbq is None:
            gbq = GoogleBigQuery()
        df = self.get_customer_id_table()

        hh.encrypt_columns(df, columns=['Name','Email','Address'])
        gbq.upload_and_replace_table(df, dataset_table_name)
        
    def merged_and_upload(self, dataset_table_name, gbq, flush_cache=True):
        
        if self.customer_table is None or self.customer_id_lookup is None:
            return
        
        if gbq is None:
            gbq = GoogleBigQuery()
        #df_old = gbq.download_table_to_pandas(dataset_table_name)
        df_old = hu.load_table(gbq, dataset_table_name, table_type='customers', flush_cache=flush_cache)
        if df_old is None:
            return self.upload_and_replace_customers_to_bq(dataset_table_name)
        
        # Keep only those rows that we haven't touched.
        df_old.drop(columns=['Name','Email','Address'], inplace=True)
        #hu.columns_as_str(df_old, columns=['Name','Email','Address'])
        #hh.decrypt_columns(df_old, columns=['Name','Email','Address'])
        
        print("df_old:")
        print(df_old.head())
        
        df_new = self.get_customer_id_table()
        
        print("df_new:")
        print(df_new.head())
        
        df_merged = df_old.merge(df_new, left_on='Customer_ID', right_on='Customer_ID', how='outer')
        
        print("df_merged:")
        print(df_merged.head())

        hh.encrypt_columns(df_merged, columns=['Name','Email','Address'])
        gbq.upload_and_replace_table(df_merged, dataset_table_name)
        
    def download(self, dataset_table_name, gbq, flush_cache=True):
        
        self.__init__()
        
        if gbq is None:
            gbq = GoogleBigQuery()
        #df = gbq.download_table_to_pandas(dataset_table_name, from_cache)
        df = hu.load_table(gbq, dataset_table_name, table_type='customers', flush_cache=flush_cache)
        if df is None:
            return False
        
        hh.decrypt_columns(df, columns=['Name','Email','Address'])
        
        self.cid = len(df)
        self.customer_table = df[['Customer_ID','Name','Email','Address']].to_numpy().tolist()
        
        for d in self.customer_table:
            
            cid = d[0]
            name = d[1]

            id_by_email = {}
            id_by_addr = {}
            if name in self.customer_id_lookup:
                id_by_email, id_by_addr = self.customer_id_lookup[name]
                
            new_email = d[2]
            new_addr = d[3]
            
            id_by_email[ new_email ] = cid
            id_by_addr[ new_addr ] = cid

            self.customer_id_lookup[name] = [id_by_email, id_by_addr]
            
        return True
        
        