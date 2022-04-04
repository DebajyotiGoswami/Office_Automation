import pprint, openpyxl as xl, csv, pandas as pd
from datetime import date

CCC_FILE= 'ccc.txt'
MASTER_FILE= 'master.csv'
BILLING_FILE= 'billing.csv'

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
            #def_bill['1'][line]= {'1.tot': 0, '11_count': 0, '11_unit': 0, '25_count': 0,'25_unit': 0, '50_count': 0, '50_unit': 0}
            #def_bill['3'][line]= {'1.tot': 0, '11_count': 0, '11_unit': 0, '25_count': 0,'25_unit': 0, '50_count': 0, '50_unit': 0}
    print("OSD Procedure Completed")
    return norm_bill, def_bill

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

def write_osd(non_govt_osd, govt_osd, norm_bill):
    writer= pd.ExcelWriter(str(date.today())+'-ZM-OSD.xlsx')
    with writer:
        df= pd.DataFrame.from_dict(non_govt_osd['LIVE'], orient= 'index')
        df.to_excel(writer, sheet_name= 'live_osd_non_govt', startrow= 1)

        df= pd.DataFrame.from_dict(govt_osd['LIVE'], orient= 'index')
        df.to_excel(writer, sheet_name= 'live_osd_govt', startrow= 1)

        df= pd.DataFrame.from_dict(non_govt_osd['DD'], orient= 'index')
        df.to_excel(writer, sheet_name= 'DD_osd_non_govt', startrow= 1)

        df= pd.DataFrame.from_dict(govt_osd['DD'], orient= 'index')
        df.to_excel(writer, sheet_name= 'DD_osd_govt', startrow= 1)

        df= pd.DataFrame.from_dict(norm_bill['1']['D'], orient= 'index')
        df.to_excel(writer, sheet_name= '1_PH_DOM_BILL', startrow= 1)

        df= pd.DataFrame.from_dict(norm_bill['1']['C'], orient= 'index')
        df.to_excel(writer, sheet_name= '1_PH_COM_BILL', startrow= 1)

        df= pd.DataFrame.from_dict(norm_bill['3']['C'], orient= 'index')
        df.to_excel(writer, sheet_name= '3_PH_COM_BILL', startrow= 1)

        df= pd.DataFrame.from_dict(norm_bill['3']['I'], orient= 'index')
        df.to_excel(writer, sheet_name= '3_PH_IND_BILL', startrow= 1)
        
def main():
    non_govt_osd, govt_osd= calculate_osd(MASTER_FILE)
    norm_bill, def_bill= calculate_billing(BILLING_FILE)
    #pprint.pprint(norm_bill['1'])
    write_osd(non_govt_osd, govt_osd, norm_bill)
    
if __name__== '__main__':
    main()
