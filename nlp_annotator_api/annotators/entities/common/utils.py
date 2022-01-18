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



    pattern = '([A-Z]{3,})|(([\d\.]{1,}(K|MPa|kPa)|([\d\.]{1,} (K|MPa|kPa))))|([A-Z]*[CP]-[A-Z\d]*)|(\d{3,}C)|GC|As |SATP|STP|NTP|([A-Z]+[\.-]+)'
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

def RegValueUnitAnnotator(paragraph):
    value_pattern = '(([+\-]?)\s*(((10)(\s+|(\$?\^))\s*(\$\^)?\{?\s*([+\-])\s*(\$\^)?\{?\s*(\d+)\}?\$?)|(((\d+\.?\d*)|(\.\d+))(\s*(E|e|((\s|X|x|×|((\$_{)?(GLYPH<[A-Z]+\d+>(}\$)?)))\s*10))\s*\^?\s*(\$\^)?\{?\s*([+\-]?)\s*(\$\^)?\{?\s*(\d+)\}?\$?)?)))((( |to|and|\/|-)+(?=\d)))*'
    unit_pattern = '((?<=\d)|(?<=\d )|(?<=\$))(((mL\s*min-\$\^\{1\}\$|ml\s*g\s*\$\^\{1\}\$\s*h\s*1|s\s*\$\^\{1\}\$|μ\s*mol\s*g\s*\$\^\{1\}\$s\s*\$\^\{1\}\$|ml\s*g\s*\$\^\{1\}\$h \$\^\{1\}\$|(μ|u)\s*mol\s*g\s*(-\s*1|\-*\$\^\{\-*1\}\$)\s*s\s*(-\s*1|\-*\$\^\{\-*1\}\$)|cm\s*(3|\$\^\{3\}\$)\s*\/\s*g|m\s*(2|\$\^\{2\}\$)\s*\/\s*g|(μ|u)\s*mol|kJ\s*\/\s*mol|cm\s*(-\s*1|\-*\$\^\{\-*1\}\$)|g\s*\/\s*cm\s*(3|\$\^\{3\}\$)|s\s*\-*(\-1|\$\^\{\-*1\}\$)|MPa|kPa|h|H|%|mL|ml|g|min||sec|L|mg|wt\s*%|vol\s*%|mm|nm|km|cm|m|kJ\/mol|° C|eV|K|Å|°|θ)(?![a-z]))+)'
    pattern_re = re.compile(unit_pattern)
    parser = pattern_re
    regex = parser.finditer(paragraph)
    exlist = []
    for reg in regex:
        if not reg.group() == '':
            exlist.append([reg.start(), reg.end(), reg.group(), 'unit', reg.group(), False, None])

    exlist = list(map(list, set(map(tuple, exlist))))
    unitlist = sorted(exlist)

    exlist = []
    pattern_re = re.compile(value_pattern)
    parser = pattern_re
    regex = parser.finditer(paragraph)
    for reg in regex:
        if not reg.group() == '':
            exlist.append([reg.start(), reg.end(), reg.group(), "value"])
    exlist = list(map(list, set(map(tuple, exlist))))
    exlist = sorted(exlist)
    valuelist = revaluelist(connectlist(exlist))

    exlist = []
    exlist.extend(valuelist)
    exlist.extend(unitlist)
    valueunitlist = valueunit(exlist)
    return valueunitlist


def is_overlap(start1, end1, start2, end2):
    return start1 <= end2 and end1 >= start2

def connectlist(exlist):
    exlist = list(map(list, set(map(tuple, exlist))))
    exlist = sorted(exlist)
        
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
                    
                    unit = max[3]


                    if min[0] < max[0]:
                        gap = max[0] - min[0]
                        newword = min[2][0:gap] + max[2]
                        tmplist = [min[0], max[1], newword, unit]
                    elif min[0] >= max[0] and min[1] <= max[1]:
                            tmplist = [max[0], max[1], max[2], unit]
                    elif min[1] > max[1]:
                        gap = min[1] - max[1]
                        newword = max[2] + min[2][gap-len(min[2]):len(min[2])]
                        tmplist = [max[0], min[1], newword, unit]
                else:
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

                    unit = max[3]

                    if min[0] < max[0]:
                        gap = max[0] - min[0]
                        newword = min[2][0:gap] + max[2]
                        tmplist = [min[0], max[1], newword, unit]
                    elif min[0] >= max[0] and min[1] <= max[1]:
                        tmplist = [max[0], max[1], max[2], unit]
                    elif min[1] > max[1]:
                        gap = min[1] - max[1]
                        newword = max[2] + min[2][gap-len(min[2]):len(min[2])]
                        tmplist = [max[0], min[1], newword, unit]
                else:
                    newlist.append(tmplist)
                    tmplist = []
        else:
            if tmplist == []:
                newlist.append(exlist[i])
            else:
                newlist.append(tmplist)
    return newlist


def valueunit(exlist):
    exlist = list(map(list, set(map(tuple, exlist))))
    exlist = sorted(exlist)
        
    newlist = []
    for i in range(0, len(exlist)):
        if not i == len(exlist)-1:
            lista = exlist[i]
            listb = exlist[i+1]
            if lista[3]=="value" and listb[3]=="unit":
                if lista[1]+1 == listb[0]:
                    newword = lista[2] + ' ' + listb[2]
                    valueunit = [lista[0], listb[1], newword, "value + unit", listb[4], lista[5], lista[6]]
                    newlist.append(valueunit)
                elif lista[1] == listb[0]:
                    newword = lista[2] + listb[2]
                    valueunit = [lista[0], listb[1], newword, "value + unit", listb[4], lista[5], lista[6]]
                    newlist.append(valueunit)
            elif lista[3] == "value" and not listb[3] == 'unit':
                    valueunit = lista
                    newlist.append(valueunit)
        else:
            if exlist[i][3] == 'value':
                newlist.append(exlist)
                


            
                    
    return newlist

def uniformvalue(value):
    if bool(re.search('(X|x|×|GLYPH<[A-Z]+\d+>)', value)):
        if bool(re.search('(E|e|10)\s*((?=\-)|(?=\+)|(?=\$))', value)):
            tmplist = re.split('(X|x|×|GLYPH<[A-Z]+\d+>)', value)
            revalue = float(tmplist[0]) * 10 ** int(re.sub('[\s\$\^\{\}]', '', re.split('E|e|10',tmplist[-1])[-1]))
        else:
            tmplist = re.split('(X|x|×|GLYPH<[A-Z]+\d+>)', value)
            revalue = float(tmplist[0]) * float(tmplist[-1])            
    else:
        if bool(re.search('((E|e|10)\s*)((?=\-)|(?=\+)|(?=\$))', value)):
            tmplist = re.split('E|e|10', value)
            if tmplist[0] == '':
                revalue = 10 ** int(re.sub('[\s\$\^\{\}]', '', tmplist[-1]))
            else:
                revalue = float(tmplist[0]) * 10 ** int(re.sub('[\s\$\^\{\}]', '', tmplist[-1]))
        else:
            revalue = float(value)
    return revalue


def revaluelist(valuelist):
    exlist = []
    for value in valuelist:
        flag = 0
        if value[2][0] == ' ':
            value[0] = value[0]+1
            value[2] = value[2][1:len(value[2])]
        if bool(re.search('(and|to|&)\s*(?=\d)', value[2])):
            tmpvalue = re.split('(and|to|&)\s*(?=\d)', value[2])
            revalue = (uniformvalue(tmpvalue[0]) + uniformvalue(tmpvalue[2]))/2
            flag = 1
        elif bool(re.search('(?<!10)\-\s*(?=\d)', value[2])):
            revalue = (float(value[2].split('-')[0])+float(value[2].split('-')[1]))/2
            flag = 1
        elif bool(re.search('\/', value[2])):
            tmpvalue = re.split('\/', value[2])
            revalue = float(tmpvalue[0])/float(tmpvalue[2])
        else:
            revalue = uniformvalue(value[2])
        if flag == 1:
            tmplist = [value[0], value[1], value[2], 'value', 'no unit', True, revalue]
        else:
            tmplist = [value[0], value[1], value[2], 'value', 'no unit', False, revalue]
        exlist.append(tmplist)

    return exlist
