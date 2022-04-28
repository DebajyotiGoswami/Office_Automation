import pprint, openpyxl as xl, csv, pandas as pd
from datetime import date

CCC_FILE= 'ccc.txt'
MASTER_FILE= 'master.csv'
BILLING_FILE= 'billing.csv'
OSD2_FILE= 'osd2.csv'

def create_ds_osd2(ccc_file):
    osd_slab= {'osd_5K': {}, 'osd_10K': {}, 'osd_50K': {}, 'osd_lakh': {}}
    with open(ccc_file, 'r') as f:
        for line in f:
            line= line.strip()
            osd_slab['osd_5K'][line]= {'D_count': 0, 'D_osd': 0, 'C_count': 0, 'C_osd': 0, 'I_count': 0, 'I_osd': 0, 'O_count': 0, 'O_osd': 0}
            osd_slab['osd_10K'][line]= {'D_count': 0, 'D_osd': 0, 'C_count': 0, 'C_osd': 0, 'I_count': 0, 'I_osd': 0, 'O_count': 0, 'O_osd': 0}
            osd_slab['osd_50K'][line]= {'D_count': 0, 'D_osd': 0, 'C_count': 0, 'C_osd': 0, 'I_count': 0, 'I_osd': 0, 'O_count': 0, 'O_osd': 0}
            osd_slab['osd_lakh'][line]= {'D_count': 0, 'D_osd': 0, 'C_count': 0, 'C_osd': 0, 'I_count': 0, 'I_osd': 0, 'O_count': 0, 'O_osd': 0}

    return osd_slab

def create_ds_osd(ccc_file):
    non_govt_osd, govt_osd= {'LIVE': {}, 'DD': {}}, {'LIVE': {}, 'DD': {}}
    with open(ccc_file, 'r') as f:
        for line in f:
            line= line.strip()
            non_govt_osd['LIVE'][line]= {'D_count': 0, 'D_osd': 0, 'C_count': 0, 'C_osd': 0, 'I_count': 0, 'I_osd': 0, 'A_count': 0, 'A_osd': 0, 'O_count': 0, 'O_osd': 0}
            non_govt_osd['DD'][line]= {'D_count': 0, 'D_osd': 0, 'C_count': 0, 'C_osd': 0, 'I_count': 0, 'I_osd': 0, 'A_count': 0, 'A_osd': 0, 'O_count': 0, 'O_osd': 0}

            govt_osd['LIVE'][line]= {'DTW_count': 0, 'DTW_osd': 0, 'STW_count': 0, 'STW_osd': 0, 'PHE_count': 0, 'PHE_osd': 0, 'STR_count': 0, 'STR_osd': 0, 'MUNI_count': 0, 'MUNI_osd': 0, 'OTH_count': 0, 'OTH_osd':0}
            govt_osd['DD'][line]= {'DTW_count': 0, 'DTW_osd': 0, 'STW_count': 0, 'STW_osd': 0, 'PHE_count': 0, 'PHE_osd': 0, 'STR_count': 0, 'STR_osd': 0, 'MUNI_count': 0, 'MUNI_osd': 0, 'OTH_count': 0, 'OTH_osd':0}
    
    return non_govt_osd, govt_osd

def create_ds_billing(ccc_file):
    norm_bill= {'1': {'D': {}, 'C': {}}, '3': {'C': {}, 'I': {}}}
    def_bill= {'1': {}, '3': {}}
    with open(ccc_file, 'r') as f:
        for line in f:
            line= line.strip()
            norm_bill['1']['D'][line]= {'1tot': 0, '2.0_norm': 0, '3.0_adv': 0, '4.0_temp': 0, '5.11_count': 0, '5.11_unit': 0, '7.25_count': 0, '7.25_unit': 0}
            norm_bill['1']['C'][line]= {'1tot': 0, '2.0_norm': 0, '3.0_adv': 0, '4.0_temp': 0, '5.11_count': 0, '5.11_unit': 0, '7.25_count': 0, '7.25_unit': 0}
            norm_bill['3']['C'][line]= {'1tot': 0, '2.0_norm': 0, '3.0_adv': 0, '4.0_temp': 0, '5.100_count': 0, '5.100_unit': 0, '7.500_count': 0, '7.500_unit': 0}
            norm_bill['3']['I'][line]= {'1tot': 0, '2.0_norm': 0, '3.0_adv': 0, '4.0_temp': 0, '5.100_count': 0, '5.100_unit': 0, '7.500_count': 0, '7.500_unit': 0}
            def_bill['1'][line]= {'1.tot': 0, '11_count': 0, '11_unit': 0, '25_count': 0,'25_unit': 0, '50_count': 0, '50_unit': 0}
            def_bill['3'][line]= {'1.tot': 0, '100_count': 0, '100_unit': 0, '250_count': 0,'250_unit': 0, '500_count': 0, '500_unit': 0}
    print("OSD Procedure Completed")
    return norm_bill, def_bill

def calculate_osd2(osd2_file):
    osd_slab= create_ds_osd2(CCC_FILE)
    
    with open(osd2_file, 'r') as f:
        osdDict= csv.DictReader(f)
        for item in osdDict:
            if item['OSD_SLAB'] not in (None, ''):
                if item['BASE_CLASS'] in ('D', 'C', 'I'):
                    tariff= item['BASE_CLASS']
                else:
                    tariff= 'O'
                try:
                    osd_slab[item['OSD_SLAB'].strip()][item['CCC_CODE']][tariff+'_count']+= int(item['COUNT'])
                    osd_slab[item['OSD_SLAB'].strip()][item['CCC_CODE']][tariff+'_osd']+= float(item['OSD'])/100000
                except KeyError:
                    print("Some error occures. Proably unknown CCC_Code in csv file")
    return osd_slab
    
def calculate_billing(billing_file):
    norm_bill, def_bill= create_ds_billing(CCC_FILE)
    with open(billing_file, 'r') as f:
        billingDict= csv.DictReader(f)
        for item in billingDict:
            if item['MET_STATUS']== 'HEALTHY':
                try:
                    norm_bill[item['CONN_PHASE']][item['BASE_CLASS']][item['CCC_CODE']]['1tot']+= int(item['COUNT'])
                    norm_bill[item['CONN_PHASE']][item['BASE_CLASS']][item['CCC_CODE']][item['TYPE'].strip()]+= int(item['COUNT'])
                    unit= item['TYPE'].replace('_count', '_unit').strip()
                    if unit in norm_bill[item['CONN_PHASE']][item['BASE_CLASS']][item['CCC_CODE']]:
                        norm_bill[item['CONN_PHASE']][item['BASE_CLASS']][item['CCC_CODE']][unit]+= float(item['UNIT'])
                except:
                    pass
            else:
                try:
                    def_bill[item['CONN_PHASE']][item['CCC_CODE']]['1.tot']+= int(item['COUNT'])
                    def_bill[item['CONN_PHASE']][item['CCC_CODE']][item['TYPE'].strip()]+= int(item['COUNT'])
                    unit= item['TYPE'].replace('_count', '_unit').strip()
                    if unit in def_bill[item['CONN_PHASE']][item['CCC_CODE']]:
                        def_bill[item['CONN_PHASE']][item['CCC_CODE']][unit]+= float(item['UNIT'])
                except:
                    pass
    print("Billing Procedure Completed")               
    return norm_bill, def_bill

def calculate_osd(master_file):
    non_govt_osd, govt_osd= create_ds_osd(CCC_FILE) #CREATING BLANK DICTIONARY FOR OSD
    with open(master_file, 'r') as f:
        masterDict= csv.DictReader(f)
        for item in masterDict:
            if item['OSD_REMARK'].strip()== 'OSD' and item['CONN_STAT'].strip() in ('LIVE', 'DD'):
                if item['GOVT_STAT']== 'NO':
                    non_govt_osd[item['CONN_STAT'].strip()][item['CCC_CODE']][item['TYPE'].strip()+'_count']+= int(item['COUNT'])
                    non_govt_osd[item['CONN_STAT'].strip()][item['CCC_CODE']][item['TYPE'].strip()+'_osd']+= round(float(item['OSD'])/100000,5)
                elif item['GOVT_STAT']== 'YES':
                    govt_osd[item['CONN_STAT'].strip()][item['CCC_CODE']][item['TYPE'].strip()+'_count']+= int(item['COUNT'])
                    govt_osd[item['CONN_STAT'].strip()][item['CCC_CODE']][item['TYPE'].strip()+'_osd']+= round(float(item['OSD'])/100000,5)
                    
    return non_govt_osd, govt_osd

def write_osd_billing(non_govt_osd, govt_osd, norm_bill, def_bill, osd_slab):
    writer= pd.ExcelWriter(str(date.today())+'-ZM-OSD.xlsx')
    with writer:
        ########
        df= pd.DataFrame.from_dict(non_govt_osd['LIVE'], orient= 'index')
        df.to_excel(writer, sheet_name= 'live_osd_non_govt', startrow= 1)

        df= pd.DataFrame.from_dict(govt_osd['LIVE'], orient= 'index')
        df.to_excel(writer, sheet_name= 'live_osd_govt', startrow= 1)
        #########
        
        df= pd.DataFrame.from_dict(non_govt_osd['DD'], orient= 'index')
        df.to_excel(writer, sheet_name= 'DD_osd_non_govt', startrow= 1)

        df= pd.DataFrame.from_dict(govt_osd['DD'], orient= 'index')
        df.to_excel(writer, sheet_name= 'DD_osd_govt', startrow= 1)

        #########
        df= pd.DataFrame.from_dict(osd_slab['osd_5K'], orient= 'index')
        df.to_excel(writer, sheet_name= 'DIS_ORD_5K', startrow= 1)

        df= pd.DataFrame.from_dict(osd_slab['osd_10K'], orient= 'index')
        df.to_excel(writer, sheet_name= 'DIS_ORD_10K', startrow= 1)

        df= pd.DataFrame.from_dict(osd_slab['osd_50K'], orient= 'index')
        df.to_excel(writer, sheet_name= 'DIS_ORD_50K', startrow= 1)

        df= pd.DataFrame.from_dict(osd_slab['osd_lakh'], orient= 'index')
        df.to_excel(writer, sheet_name= 'DIS_ORD_lakh', startrow= 1)
        ##########

        df= pd.DataFrame.from_dict(norm_bill['1']['D'], orient= 'index')
        df.to_excel(writer, sheet_name= '1_PH_DOM_BILL', startrow= 1)

        df= pd.DataFrame.from_dict(norm_bill['1']['C'], orient= 'index')
        df.to_excel(writer, sheet_name= '1_PH_COM_BILL', startrow= 1)

        df= pd.DataFrame.from_dict(norm_bill['3']['C'], orient= 'index')
        df.to_excel(writer, sheet_name= '3_PH_COM_BILL', startrow= 1)

        df= pd.DataFrame.from_dict(norm_bill['3']['I'], orient= 'index')
        df.to_excel(writer, sheet_name= '3_PH_IND_BILL', startrow= 1)

        df= pd.DataFrame.from_dict(def_bill['1'], orient= 'index')
        df.to_excel(writer, sheet_name= '1_PH_DEF_BILL', startrow= 1)

        df= pd.DataFrame.from_dict(def_bill['3'], orient= 'index')
        df.to_excel(writer, sheet_name= '3_PH_DEF_BILL', startrow= 1)        
        
def main():
    non_govt_osd, govt_osd= calculate_osd(MASTER_FILE)
    norm_bill, def_bill= calculate_billing(BILLING_FILE)
    osd_slab= calculate_osd2(OSD2_FILE)
    #pprint.pprint(osd_slab)
    write_osd_billing(non_govt_osd, govt_osd, norm_bill, def_bill, osd_slab)
    
if __name__== '__main__':
    main()
