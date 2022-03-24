import pprint

def create_ds(ccc_file):
    non_govt_osd, govt_osd= {'live': {}, 'dd': {}}, {'live': {}, 'dd': {}}
    with open(ccc_file, 'r') as f:
        for line in f:
            line= line.strip()
            non_govt_osd['live'][line]= {'D': [0,0], 'C': [0,0], 'I': [0,0], 'A': [0,0], 'O': [0,0]}
            non_govt_osd['dd'][line]= {'D': [0,0], 'C': [0,0], 'I': [0,0], 'A': [0,0], 'O': [0,0]}

            govt_osd['live'][line]= {'dtw': [0,0], 'stw': [0,0], 'phe': [0,0], 'str': [0,0], 'muni': [0,0], 'oth': [0,0]}
            govt_osd['dd'][line]= {'dtw': [0,0], 'stw': [0,0], 'phe': [0,0], 'str': [0,0], 'muni': [0,0], 'oth': [0,0]}

    return non_govt_osd, govt_osd

def main():
    ccc_file= 'ccc.txt'
    non_govt_osd, govt_osd= create_ds(ccc_file)
    pprint.pprint(govt_osd)
    
if __name__== '__main__':
    main()
