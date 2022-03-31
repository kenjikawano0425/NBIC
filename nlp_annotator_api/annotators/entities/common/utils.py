import os
from unicodedata import unidata_version
from chemdataextractor import Document
import re
import json
from inflector import Inflector

resources_dir = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../resources"
    )
)

#nlpmodel-v-h/nlp_annotator_api/resources/properties_resource.json

def RegPropertiesAnnotator(paragraph):

    exlist = []
    dictionary_filename=os.path.join(resources_dir, "properties_resource.json")
    json_open = open(dictionary_filename, 'r')
    json_load = json.load(json_open)

    for jsondata in json_load:
        jsondata['_synonyms'].append(jsondata['_name'])

        jsondata['_synonyms'].append(jsondata['_name'].capitalize())
        jsondata['_synonyms'].append(jsondata['_name'].upper())
        jsondata['_synonyms'].append(jsondata['_name'].lower())
        jsondata['_synonyms'].append(jsondata['_name'].title())

        jsondata['_synonyms'].append(Inflector().pluralize(jsondata['_name'].capitalize()))
        jsondata['_synonyms'].append(Inflector().pluralize(jsondata['_name'].upper()))
        jsondata['_synonyms'].append(Inflector().pluralize(jsondata['_name'].lower()))
        jsondata['_synonyms'].append(Inflector().pluralize(jsondata['_name'].title()))

        jsondata['_synonyms'].append(Inflector().pluralize(jsondata['_name']).capitalize())
        jsondata['_synonyms'].append(Inflector().pluralize(jsondata['_name']).upper())
        jsondata['_synonyms'].append(Inflector().pluralize(jsondata['_name']).lower())
        jsondata['_synonyms'].append(Inflector().pluralize(jsondata['_name']).title())

        jsondata['_synonyms'] = sorted(list(set(jsondata['_synonyms'])), key=len, reverse=True)

        pro_pattern = '|'.join(jsondata['_synonyms'])
        pattern_re = re.compile(pro_pattern)
        parser = pattern_re
        regex = parser.finditer(paragraph)
        for reg in regex:
            if not reg.group() == '':
                exlist.append([reg.start(), reg.end(), reg.group(), "properties"])
                exlist.append([reg.start(), reg.end(), reg.group(), jsondata['_name']])
        
    return exlist


def RegValueAnnotator(paragraph):
    value_pattern = '(([+\-]?)\s*(((10)(\s+|(\$?\^))\s*(\$\^)?\{?\s*([+\-])\s*(\$\^)?\{?\s*(\d+)\}?\$?)|(((\d+\.?\d*)|(\.\d+))(\s*(E|e|((\s|X|x|×|((\$_{)?(GLYPH<[A-Z]+\d+>(}\$)?)))\s*10))\s*\^?\s*(\$\^)?\{?\s*([+\-]?)\s*(\$\^)?\{?\s*(\d+)\}?\$?)?)))((( |to|and|\/|-)+(?=\d)))*'
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
    return valuelist


def RegChemAnnotator(paragraph):
    exlist = []

    doc = Document(paragraph)
    for text in doc.cems:
        exlist.append([text.start, text.end, text.text, 1])

    pattern = '((\$[_^]{[\d+-]{0,}}\$|[\[\]\=()\/\-\+])*((YSZ|NWs|@|He|Li|Be|Ne|Na|Mg|Al|Si|Cl|Ar|Ca|Sc|Ti|Cr|Mn|Fe|Co|Ni|Cu|Zn|Ga|Ge|As|Se|Br|Kr|Rb|Sr|Zr|Nb|Mo|Tc|Ru|Rh|Pd|Ag|Cd|In|Sn|Sb|Te|Xe|Cs|Ba|La|Ce|Pr|Nd|Pm|Sm|Eu|Gd|Tb|Dy|Ho|Er|Tm|Yb|Lu|Hf|Ta|Re|Os|Ir|Pt|Au|Hg|Tl|Pb|Bi|Po|At|Rn|Fr|Ra|Ac|Th|Pa|Np|Pu|Am|Cm|Bk|Cf|Es|Fm|Md|No|Lr|Rf|Db|Sg|Bh|Hs|Mt|Ds|Rg|Cn|Nh|Fl|Mc|Lv|Ts|Og|Hb|M|H|B|C|N|O|F|P|S|K|V|I|W|U|Y|X)(\$[_^]\{([+-]|[a-z]|(\d\.*\d*))*\}\$|[\–\[\]()\/\-\+\.\d\: ])*)+)'
    pattern_re = re.compile(pattern)
    regex = pattern_re.finditer(paragraph)
    for reg in regex:
        if not len(paragraph) == reg.end():
            if paragraph[reg.end()-2:reg.end()] == '/ ':
                exlist.append([reg.start(), reg.end()-2, reg.group()[0:-2], 1])
            elif paragraph[reg.end()-1] == ' ' or paragraph[reg.end()-1] == '/':
                exlist.append([reg.start(), reg.end()-1, reg.group()[0:-1], 1])
            elif re.search("(?<=[\(\/\$])[a-zø]", paragraph[reg.end()-1:reg.end()+1]):
                exlist.append([reg.start(), reg.end(), reg.group(), 1])
            elif not re.search("[a-zø]", paragraph[reg.end()]):
                exlist.append([reg.start(), reg.end(), reg.group(), 1])
        else:
            exlist.append([reg.start(), reg.end(), reg.group(), 1])


    pattern = '(Li|He),\s*[A-Z]\.|(([\d\.]{1,}(K|MPa|kPa)|([\d\.]{1,} (K|MPa|kPa))))|Re V\.*|J\.\s*(Mol|Am|Phys)\.|(\d{3,}C)|GC|As |In |At |TOF|SATP|STP|NTP|SMF|O\'Neill|CrossRef|PubMed|DI|II|XPS|ICP\-OES|QP\-5000|GC\-MS|F\-T|JEOL|DOI|S\/N|A\/F|(JP|US)\d{2,}[A-Z]|([A-Z]+[\.-]+)|([A-Z]*[CP]-[A-Z\d]*)|([A-Z]{3,})|\d+\s*((k|M|m|n)*eV|C|° C|\$\^\{◦\}\$\s*C)|(B|C),*\s*[12][09]\d{2}|((F|f)igure(s)*|(F|f)ig|(T|t)able(s)*)[\,\.\s\dA-Z\-]*(and)*[\,\.\s\d\-]*[A-Z\d]*'
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
                    
                    if max[3] == 0 or min[3] == 0:
                        max[3] = 0

                    if min[0] < max[0]:
                        gap = max[0] - min[0]
                        newword = min[2][0:gap] + max[2]
                        tmplist = [min[0], max[1], newword, max[3]]
                    elif min[0] >= max[0] and min[1] <= max[1]:
                            tmplist = [max[0], max[1], max[2], max[3]]
                    elif min[1] > max[1]:
                        gap = min[1] - max[1]
                        newword = max[2] + min[2][len(min[2])-gap:len(min[2])]
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

                    if max[3] == 0 or min[3] == 0:
                        max[3] = 0


                    if min[0] < max[0]:
                        gap = max[0] - min[0]
                        newword = min[2][0:gap] + max[2]
                        tmplist = [min[0], max[1], newword, max[3]]
                    elif min[0] >= max[0] and min[1] <= max[1]:
                            tmplist = [max[0], max[1], max[2], max[3]]
                    elif min[1] > max[1]:
                        gap = min[1] - max[1]
                        newword = max[2] + min[2][len(min[2])-gap:len(min[2])]
                        tmplist = [max[0], min[1], newword, max[3]]
                else:
                    if tmplist[3] == 1:
                        newlist.append(tmplist)
                    tmplist = []
        else:
            if tmplist == [] and exlist[i][3] == 1:
                newlist.append(exlist[i])
            elif tmplist == [] and exlist[i][3] == 0:
                break
            elif tmplist[3] == 1:
                newlist.append(tmplist)
    

    for i, check in enumerate(newlist):
        if check[2][-1] == ')' and not bool(re.search('\(',check[2])):
            newlist[i][1] = check[1]-1
            newlist[i][2] = check[2][0:len(check[2])-1]
        elif not check[2][-1] == ')' and check[2][0] == '(':
            newlist[i][0] = check[0]+1
            newlist[i][2] = check[2][1:len(check[2])]
        elif check[2][-1] == ')' and check[2][0] == '(':
            newlist[i][0] = check[0]+1
            newlist[i][1] = check[1]-1
            newlist[i][2] = check[2][1:len(check[2])-1]
        
        if check[2][-1] in ['(','/', '-', '.']:
            newlist[i][1] = check[1]-1
            newlist[i][2] = check[2][0:len(check[2])-1]
        if check[2][0] in ['/', '-', '.']:
            newlist[i][0] = check[0]+1
            newlist[i][2] = check[2][1:len(check[2])]

         
    return newlist

def RegValueUnitAnnotator(paragraph):
    value_pattern = '(([+\-]?)\s*(((10)(\s+|(\$?\^))\s*(\$\^)?\{?\s*([+\-])\s*(\$\^)?\{?\s*(\d+)\}?\$?)|(((\d+\.?\d*)|(\.\d+))(\s*(E|e|((\s|X|x|×|((\$_{)?(GLYPH<[A-Z]+\d+>(}\$)?)))\s*10))\s*\^?\s*(\$\^)?\{?\s*([+\-]?)\s*(\$\^)?\{?\s*(\d+)\}?\$?)?)))((( |to|and|\/|-|,)+(?=\d)))*'
    unit_pattern = '((?<=\d)|(?<=\d )|(?<=\$))(((atom\s*atom\-\$\^\{\d\}\$|K\s*min\-\$\^\{\d\}\$|m\s*\d\s*g\-\$\^\{\d\}\$|mL\s*g\-\$\^\{\d\}\$|mL\s*g\s*\$\_\{cat\}\$-1\s*h-\$\^\{1\}\$|kJ\s*mol\s*-\$\^\{1\}\$|m\s*\$\^\s*\{2\}\$\s*g\s*-\s*\$\^\{1\}\$|m(L|l)\s*min-\$\^\{1\}\$|ml\s*g\s*\$\^\{1\}\$\s*h\s*1|s\s*\$\^\{1\}\$|μ\s*mol\s*g\s*\$\^\{1\}\$s\s*\$\^\{1\}\$|ml\s*g\s*\$\^\{1\}\$h \$\^\{1\}\$|(μ|u)\s*mol\s*g\s*(-\s*1|\-*\$\^\{\-*1\}\$)\s*s\s*(-\s*1|\-*\$\^\{\-*1\}\$)|cm\s*(3|\$\^\{3\}\$)\s*\/\s*g|m\s*(2|\$\^\{2\}\$)\s*\/\s*g|(μ|u)\s*mol|kJ\s*\/\s*mol|cm\s*(-\s*1|\-*\$\^\{\-*1\}\$)|g\s*\/\s*cm\s*(3|\$\^\{3\}\$)|s\s*\-*(\-1|\$\^\{\-*1\}\$)|C\s*m\s*i\s*n\s*-\$\^\{1\}\$|C\s*min-1|h-1|M\s*Pa|k\s*Pa|m\s*Pa|(h|H)|%|m\s*(L|l)\s*\/\s*min|m(L|l)|g|m\s*i\s*n|atom\-\$\^\{\d\}\$|atom|ppm|ml\s*min\s*-1|h\s*-\$\^\{1\}\$|mol\s*l\s*-1|mA|kV|sec|m\s*g|wt\s*%|vol\s*%|mol\s*%|(µ|u)\s*m|m\s*m|n\s*m|k\s*m|(c|C)\s*m|m|kJ\s*\/\s*mol|° C|C|\$\^{◦}\$\s*C|eV|L|s|K|Å|°|θ)((?=to)|(?![a-z])))+)'
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
                        newword = max[2] + min[2][len(min[2])-gap:len(min[2])]
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
                        newword = max[2] + min[2][len(min[2])-gap:len(min[2])]
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
                
                if exlist[i][5] == True:
                    for num in range(i-1,-1,-1):
                        if exlist[num][3] == "value":
                            if exlist[num][5] == True:
                                lista = exlist[num]
                                if lista[1]+1 == listb[0]:
                                    newword = lista[2] + ' ' + listb[2]
                                    valueunit = [lista[0], listb[1], newword, "value + unit", listb[4], lista[5], lista[6]]
                                    newlist.append(valueunit)
                                elif lista[1] == listb[0]:
                                    newword = lista[2] + listb[2]
                                    valueunit = [lista[0], listb[1], newword, "value + unit", listb[4], lista[5], lista[6]]
                                    newlist.append(valueunit)
                            elif exlist[num][5] == False:
                                continue
                        else:
                            continue


            elif lista[3] == "value" and not listb[3] == 'unit':
                pass
        else:
            pass
    return newlist

def uniformvalue(value):
    if bool(re.search('(X|x|×|GLYPH<[A-Z]+\d+>)', value)):
        if bool(re.search('(E|e|10)\s*((?=\-)|(?=\s)|(?=\+)|(?=\$))', value)):
            tmplist = re.split('(X|x|×|GLYPH<[A-Z]+\d+>)', value)
            revalue = float(tmplist[0]) * 10 ** int(re.sub('[\s\$\^\{\}]', '', re.split('E|E|e|10',tmplist[-1])[-1]))
        else:
            tmplist = re.split('(X|×|x|×|GLYPH<[A-Z]+\d+>)', value)
            revalue = float(tmplist[0]) * float(tmplist[-1])            
    else:
        if bool(re.search('((E|E|e|10)\s*)((?=\-)|(?=\+)|(?=\$))', value)):
            tmplist = re.split('E|e|10', value)
            if tmplist[0] == '':
                revalue = 10 ** int(re.sub('[\s\$\^\{\}]', '', tmplist[-1]))
            else:
                revalue = float(tmplist[0]) * 10 ** float(re.sub('[\s\$\^\{\}]', '', tmplist[-1]))
        else:
            try:
                revalue = eval(re.sub(' ', '', value))
            except SyntaxError:
                revalue = float(re.sub(' ', '', value))
            except ValueError:
                print("warning:{0}, this is not value:{1}".format("ValueError", value[2]))
                revalue = 0
    return revalue


def revaluelist(valuelist):
    exlist = []
    for value in valuelist:
        flag = 0
        if value[2][0] == ' ':
            value[0] = value[0]+1
            value[2] = value[2][1:len(value[2])]
        try:
            if bool(re.search('(?<=\d)\s6\s(?=\d)', value[2])):
                revalue = value[2].split(" 6 ")[0]
                flag = 1
            elif bool(re.search('and|to|&|,', value[2])):
                splitvalue = value[2]
                regex = re.finditer(',', splitvalue)
                offset = 0
                for reg in regex:
                    if not splitvalue[reg.start()-offset+1]==' ':
                        replace_tmp = list(splitvalue)
                        replace_tmp[reg.start()-offset] = ''
                        splitvalue = ''.join(replace_tmp)
                        offset = offset + 1
                tmpvalues = re.split('and|to|&|,', splitvalue)
                for i, tmpvalue in enumerate(tmpvalues):
                    if bool(re.search('\d', tmpvalue)):
                        if bool(re.search('((?<![Ee])(?<!10))\-\s*(?=\d)', tmpvalue)):
                            if tmpvalue[0] == "-":
                                revalue = uniformvalue(tmpvalue)
                            else:
                                revalue = (uniformvalue(tmpvalue.split('-')[0])+uniformvalue(tmpvalue.split('-')[1]))/2
                        else:
                            revalue = uniformvalue(tmpvalue)
                        tmplist = [value[0], value[1], value[2], 'value', 'no unit', True, revalue]
                        exlist.append(tmplist)
                continue

            elif bool(re.search('((?<![Ee])(?<!10))\-\s*(?=\d)', value[2])):
                if value[2][0] == "-":
                    revalue = uniformvalue(value[2])
                    flag = 0
                else:
                    revalue = (uniformvalue(re.sub(' ', '', value[2].split('-')[0]))+uniformvalue(re.sub(' ', '', value[2].split('-')[1])))/2
                    flag = 1
            else:
                revalue = uniformvalue(value[2])
        except ValueError:
            print("warning:{0}, this is not value:{1}".format("ValueError", value[2]))
            continue

        if flag == 1:
            tmplist = [value[0], value[1], value[2], 'value', 'no unit', True, revalue]
        else:
            tmplist = [value[0], value[1], value[2], 'value', 'no unit', False, revalue]
        exlist.append(tmplist)

    return exlist
