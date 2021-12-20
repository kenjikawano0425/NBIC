import os


resources_dir = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../resources"
    )
)


from chemdataextractor import Document
import re

def RegChemAnnotator(paragraph):
    exlist = []

    doc = Document(paragraph)
    for text in doc.cems:
        exlist.append([text.start, text.end, text.text, 1])


    pattern = '((\$[_^]{[\d+-]{0,}}\$|[()\/\-\+])*((He|Li|Be|Ne|Na|Mg|Al|Si|Cl|Ar|Ca|Sc|Ti|Cr|Mn|Fe|Co|Ni|Cu|Zn|Ga|Ge|As|Se|Br|Kr|Rb|Sr|Zr|Nb|Mo|Tc|Ru|Rh|Pd|Ag|Cd|In|Sn|Sb|Te|Xe|Cs|Ba|La|Ce|Pr|Nd|Pm|Sm|Eu|Gd|Tb|Dy|Ho|Er|Tm|Yb|Lu|Hf|Ta|Re|Os|Ir|Pt|Au|Hg|Tl|Pb|Bi|Po|At|Rn|Fr|Ra|Ac|Th|Pa|Np|Pu|Am|Cm|Bk|Cf|Es|Fm|Md|No|Lr|Rf|Db|Sg|Bh|Hs|Mt|Ds|Rg|Cn|Nh|Fl|Mc|Lv|Ts|Og|H|B|C|N|O|F|P|S|K|V|I|W|U|Y|X)(\$[_^]{[\d+-]{0,}}\$|[()\/\-\+ ])*)+)'
    pattern_re = re.compile(pattern)
    regex = pattern_re.finditer(paragraph)
    for reg in regex:
        if not len(paragraph) == reg.end():
            if paragraph[reg.end()-2:reg.end()] == '/ ':
                exlist.append([reg.start(), reg.end()-2, reg.group()[0:-2], 1])
            elif paragraph[reg.end()-1] == ' ' or paragraph[reg.end()-1] == '/':
                exlist.append([reg.start(), reg.end()-1, reg.group()[0:-1], 1])
            elif not re.search("[a-z]", paragraph[reg.end()]):
                exlist.append([reg.start(), reg.end(), reg.group(), 1])
        else:
            exlist.append([reg.start(), reg.end(), reg.group(), 1])



    pattern = '([A-Z]{3,})|(([\d\.]{1,}(K|MPa|kPa)|([\d\.]{1,} (K|MPa|kPa))))|([A-Z]*[CP]-[A-Z\d]*)|(\d{3,}C)|GC|As |([A-Z]+[\.-]+)'
    pattern_re = re.compile(pattern)
    regex = pattern_re.finditer(paragraph)

    for reg in regex:
        exlist.append([reg.start(), reg.end(), reg.group(), 0])


    exlist = list(map(list, set(map(tuple, exlist))))
    exlist = sorted(exlist)
        
    def is_overlap(start1, end1, start2, end2):
        return start1 <= end2 and end1 >= start2

    tmplist = []
    newlist = []
    for i in range(0, len(exlist)):
        if not i == len(exlist)-1:
            if tmplist == []:
                lista = exlist[i]
                listb = exlist[i+1]
                if is_overlap(lista[0],lista[1], listb[0], listb[1]):
                    if lista[1]-lista[0] > listb[1]-listb[0]:
                        max = lista
                        min = listb
                    else:
                        max = listb
                        min = lista

                    if min[0] < max[0]:
                        gap = max[0] - min[0]
                        newword = min[2][0:gap] + max[2]
                        tmplist = [min[0], max[1], newword, max[3]]
                    elif min[0] >= max[0] and min[1] <= max[1]:
                        tmplist = [max[0], max[1], max[2], max[3]]
                    elif min[1] > max[1]:
                        gap = min[1] - max[1]
                        newword = max[2] + min[2][gap-1:len(min[2])]
                        tmplist = [max[0], min[1], newword, max[3]]
                else:
                    if exlist[i][3] == 1:
                        newlist.append(exlist[i])
            else:
                lista = tmplist
                listb = exlist[i+1]
                if is_overlap(lista[0],lista[1], listb[0], listb[1]):
                    if lista[1]-lista[0] > listb[1]-listb[0]:
                        max = lista
                        min = listb
                    else:
                        max = listb
                        min = lista

                    if min[0] < max[0]:
                        gap = max[0] - min[0]
                        newword = min[2][0:gap] + max[2]
                        tmplist = [min[0], max[1], newword, max[3]]
                    elif min[0] >= max[0] and min[1] <= max[1]:
                        tmplist = [max[0], max[1], max[2], max[3]]
                    elif min[1] > max[1]:
                        gap = min[1] - max[1]
                        newword = max[2] + min[2][gap-1:len(min[2])]
                        tmplist = [max[0], min[1], newword, max[3]]
                else:
                    if tmplist[3] == 1:
                        newlist.append(tmplist)
                    tmplist = []
        else:
            if tmplist == [] and exlist[i][3] == 1:
                newlist.append(exlist[i])
            elif exlist[i][3] == 0:
                break
            elif tmplist[3] == 1:
                newlist.append(tmplist)
    return newlist

def RegValueAnnotator(paragraph):
    exlist = []
    ex_in_list = []
    pattern = '([+\-]?)\s*(((10)(\s+|(\$?\^))\s*(\$\^)?\{?\s*([+\-])\s*(\$\^)?\{?\s*(\d+)\}?\$?)|(((\d+\.?\d*)|(\.\d+))(\s*(E|e|((\s|X|x|((\$_{)?(GLYPH<[A-Z]+\d+>(}\$)?)))\s*10))\s*\^?\s*(\$\^)?\{?\s*([+\-]?)\s*(\$\^)?\{?\s*(\d+)\}?\$?)?))'
    pattern_re = re.compile(pattern)
    parser = pattern_re
    regex = parser.finditer(paragraph)
    for reg in regex:
        exlist.append([reg.start(), reg.end(), reg.group(), 1])

    exlist = list(map(list, set(map(tuple, exlist))))
    exlist = sorted(exlist)

    def is_overlap(start1, end1, start2, end2):
        return start1 <= end2 and end1 >= start2

    tmplist = []
    newlist = []
    for i in range(0, len(exlist)):
        if not i == len(exlist)-1:
            if tmplist == []:
                lista = exlist[i]
                listb = exlist[i+1]
                if is_overlap(lista[0],lista[1], listb[0], listb[1]):
                    if lista[1]-lista[0] > listb[1]-listb[0]:
                        max = lista
                        min = listb
                    else:
                        max = listb
                        min = lista

                    if min[0] < max[0]:
                        gap = max[0] - min[0]
                        newword = min[2][0:gap] + max[2]
                        tmplist = [min[0], max[1], newword, max[3]]
                    elif min[0] >= max[0] and min[1] <= max[1]:
                        tmplist = [max[0], max[1], max[2], max[3]]
                    elif min[1] > max[1]:
                        gap = min[1] - max[1]
                        newword = max[2] + min[2][gap-1:len(min[2])]
                        tmplist = [max[0], min[1], newword, max[3]]
                else:
                    if exlist[i][3] == 1:
                        newlist.append(exlist[i])
            else:
                lista = tmplist
                listb = exlist[i+1]
                if is_overlap(lista[0],lista[1], listb[0], listb[1]):
                    if lista[1]-lista[0] > listb[1]-listb[0]:
                        max = lista
                        min = listb
                    else:
                        max = listb
                        min = lista

                    if min[0] < max[0]:
                        gap = max[0] - min[0]
                        newword = min[2][0:gap] + max[2]
                        tmplist = [min[0], max[1], newword, max[3]]
                    elif min[0] >= max[0] and min[1] <= max[1]:
                        tmplist = [max[0], max[1], max[2], max[3]]
                    elif min[1] > max[1]:
                        gap = min[1] - max[1]
                        newword = max[2] + min[2][gap-1:len(min[2])]
                        tmplist = [max[0], min[1], newword, max[3]]
                else:
                    if tmplist[3] == 1:
                        newlist.append(tmplist)
                    tmplist = []
        else:
            newlist.append(exlist[i])


    pattern_inverse = '((?<=\$[_^]{)\d+?(?=}\$))|((?<=\[)(\-*\d+)+?(?=\]))|((?<=figure)|((?<=Figure)|(?<=fig)|(?<=Fig)|(?<=figure\.)|(?<=Figure\.)|(?<=fig\.)|(?<=Fig\.)|(?<=table)|(?<=Table)|(?<=table\.)|(?<=Table\.))( \d+|\d+)(\.|))'
    pattern_re = re.compile(pattern_inverse)
    parser = pattern_re
    regex = parser.finditer(paragraph)
    for reg in regex:
        newlist.append([reg.start(), reg.end(), reg.group(), 1])

    finallist = []
    for new in newlist:
        if newlist.count(new) == 1:
            finallist.append(new)
    
    return finallist