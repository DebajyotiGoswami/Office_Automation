import pprint, openpyxl as xl, csv, pandas as pd
from datetime import date

CCC_FILE= 'ccc.txt'
MASTER_FILE= 'master.csv'

def create_ds(ccc_file):
    non_govt_osd, govt_osd= {'LIVE': {}, 'DD': {}}, {'LIVE': {}, 'DD': {}}
    with open(ccc_file, 'r') as f:
        for line in f:
            line= line.strip()
            non_govt_osd['LIVE'][line]= {'D': [0,0], 'C': [0,0], 'I': [0,0], 'A': [0,0], 'O': [0,0]}
            non_govt_osd['DD'][line]= {'D': [0,0], 'C': [0,0], 'I': [0,0], 'A': [0,0], 'O': [0,0]}

            govt_osd['LIVE'][line]= {'DTW': [0,0], 'STW': [0,0], 'PHE': [0,0], 'STR': [0,0], 'MUNI': [0,0], 'OTH': [0,0]}
            govt_osd['DD'][line]= {'DTW': [0,0], 'STW': [0,0], 'PHE': [0,0], 'STR': [0,0], 'MUNI': [0,0], 'OTH': [0,0]}

    return non_govt_osd, govt_osd

def calculate_osd(master_file):
    non_govt_osd, govt_osd= create_ds(CCC_FILE) #CREATING BLANK DICTIONARY FOR OSD
    with open(master_file, 'r') as f:
        masterDict= csv.DictReader(f)
        for item in masterDict:
            if item['OSD_REMARK'].strip()== 'OSD' and item['CONN_STAT'].strip() in ('LIVE', 'DD'):
                if item['GOVT_STAT']== 'NO':
                    non_govt_osd[item['CONN_STAT'].strip()][item['CCC_CODE']][item['TYPE'].strip()][0]+= int(item['COUNT'])
                    non_govt_osd[item['CONN_STAT'].strip()][item['CCC_CODE']][item['TYPE'].strip()][1]+= round(float(item['OSD'])/100000,2)
                elif item['GOVT_STAT']== 'YES':
                    govt_osd[item['CONN_STAT'].strip()][item['CCC_CODE']][item['TYPE'].strip()][0]+= int(item['COUNT'])
                    govt_osd[item['CONN_STAT'].strip()][item['CCC_CODE']][item['TYPE'].strip()][1]+= round(float(item['OSD'])/100000,2)
                    
    return non_govt_osd, govt_osd

def write_osd(non_govt_osd, govt_osd):
    #fileObj= xl.Workbook()
    #sheet= fileObj.active
    df= pd.DataFrame.from_dict(non_govt_osd['LIVE'], orient= 'index')
    #df= (df.T)
    print(df)
    df.to_excel(str(date.today())+'-ZM-OSD.xlsx')
    #fileObj.save(str(date.today())+'-ZM-OSD.xlsx')
    
def main():
    non_govt_osd, govt_osd= calculate_osd(MASTER_FILE)
    write_osd(non_govt_osd, govt_osd)
    pprint.pprint(govt_osd)
    
if __name__== '__main__':
    main()
