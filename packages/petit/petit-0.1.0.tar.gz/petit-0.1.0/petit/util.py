import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import sys
import os

# check install
def check_install():
    print("petit was successfully installed.")

# convert .xlsx table to .fasta file
def xlsx_to_fasta(filepath):    
    dirname = os.path.dirname(filepath)
    filename = os.path.splitext(os.path.basename(filepath))[0]
    df = pd.read_excel(filepath)
    with open(dirname+"/"+filename+".fasta", "w") as f:
        for i in range(len(df.index)):
            seq = Seq(df.iloc[i,1])
            rec = SeqRecord(seq, description="")
            rec.id = df.iloc[i,0]
            SeqIO.write(rec, f, "fasta")

# in case of "$ python excel_to_fasta.py %1"
if __name__ == '__main__':
    filepath = sys.argv[1]
    xlsx_to_fasta(filepath)
