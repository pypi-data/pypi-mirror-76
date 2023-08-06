import operator

def fasta_sequence_count(inputfile,outputfile):
    file1=open(inputfile,"r")
    file2=file1.read().strip().split(">")[1:]
    a=[]
    for elements1 in file2:
        name = elements1.strip().split("\n")[0]
        length = len(elements1.strip().split("\n")[1])
        a.append(length)
    dict_1={}
    for item in a:
        dict_1[item] = a.count(item)
        sorted_x = sorted(dict_1.items(), key=operator.itemgetter(1), reverse=True)
    for k, v in sorted_x:
        with open(outputfile,"a+")as f:
            f.write(str(k) + "\t" + str(v)  +"\n" )

