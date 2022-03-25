import pprint, openpyxl as xl, csv

CCC_FILE= 'ccc.txt'
MASTER_FILE= 'master.xlsx'

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
            print(item)
    return non_govt_osd, govt_osd

def main():
    master_file= 'master.xlsx'
    non_govt_osd, govt_osd= calculate_osd(MASTER_FILE)
    #pprint.pprint(non_govt_osd)
    
if __name__== '__main__':
    main()
