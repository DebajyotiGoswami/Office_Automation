import pprint, openpyxl as xl, csv, pandas as pd
from datetime import date

CCC_FILE= 'ccc.txt'
MASTER_FILE= 'master.csv'

def create_ds(ccc_file):
    non_govt_osd, govt_osd= {'LIVE': {}, 'DD': {}}, {'LIVE': {}, 'DD': {}}
    with open(ccc_file, 'r') as f:
        for line in f:
            line= line.strip()
            non_govt_osd['LIVE'][line]= {'D_count': 0, 'D_osd': 0, 'C_count': 0, 'C_osd': 0, 'I_count': 0, 'I_osd': 0, 'A_count': 0, 'A_osd': 0, 'O_count': 0, 'O_osd': 0}
            non_govt_osd['DD'][line]= {'D_count': 0, 'D_osd': 0, 'C_count': 0, 'C_osd': 0, 'I_count': 0, 'I_osd': 0, 'A_count': 0, 'A_osd': 0, 'O_count': 0, 'O_osd': 0}

            govt_osd['LIVE'][line]= {'DTW_count': 0, 'DTW_osd': 0, 'STW_count': 0, 'STW_osd': 0, 'PHE_count': 0, 'PHE_osd': 0, 'STR_count': 0, 'STR_osd': 0, 'MUNI_count': 0, 'MUNI_osd': 0, 'OTH_count': 0, 'OTH_osd':0}
            govt_osd['DD'][line]= {'DTW_count': 0, 'DTW_osd': 0, 'STW_count': 0, 'STW_osd': 0, 'PHE_count': 0, 'PHE_osd': 0, 'STR_count': 0, 'STR_osd': 0, 'MUNI_count': 0, 'MUNI_osd': 0, 'OTH_count': 0, 'OTH_osd':0}

    return non_govt_osd, govt_osd

def calculate_osd(master_file):
    non_govt_osd, govt_osd= create_ds(CCC_FILE) #CREATING BLANK DICTIONARY FOR OSD
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

def write_osd(non_govt_osd, govt_osd):
    df= pd.DataFrame.from_dict(non_govt_osd['LIVE'], orient= 'index')
    df.to_excel(str(date.today())+'-ZM-OSD.xlsx')
    
def main():
    non_govt_osd, govt_osd= calculate_osd(MASTER_FILE)
    write_osd(non_govt_osd, govt_osd)
    pprint.pprint(govt_osd)
    
if __name__== '__main__':
    main()
