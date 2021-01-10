"""
validate the name, father name and PAN number data either by reguler expression
or by replcaing the similar visible characters/numbers to numbers/characters.
"""

import re

def validate_name(name):
    name=name.upper()
    name=name.strip()
    name = name.replace("8", "B")
    name = name.replace("0", "O")
    name = name.replace("6", "G")
    name = name.replace("1", "I")
    name = name.replace("!","I")
    name = re.sub('[^A-Z]+', ' ', name)
    return name


def validate_father_name(fname):
    fname=fname.upper()
    fname=fname.strip()
    fname = fname.replace("8", "B")
    fname = fname.replace("0", "O")
    fname = fname.replace("6", "G")
    fname = fname.replace("1", "I")
    fname = fname.replace("!","I")
    fname = re.sub('[^A-Z]+', ' ', fname)
    return fname

def validate_pan_no(Pan):
    Pan=Pan.upper()
    Pan=Pan.strip()
    Pan=Pan.replace(" ","")
    if len(Pan)==10:
        boolpan=re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$',Pan)
        if boolpan:
            return Pan
        else:
            temp_pan_chrs=Pan[0:5]
            for temp_chr in temp_pan_chrs:
                if temp_chr=="0":
                    Pan=Pan.replace(temp_chr,"O")
                if temp_chr=="5":
                    Pan=Pan.replace(temp_chr,"S")
                if temp_chr=="8":
                    Pan=Pan.replace(temp_chr,"B")
                if temp_chr=="6":
                    Pan=Pan.replace(temp_chr,"G")
                if temp_chr=="1":
                    Pan=Pan.replace(temp_chr,"I")
            temp_pan_chrs = Pan[0:5]

            temp_pan_nums=Pan[5:9]
            for temp_num in temp_pan_nums:
                if temp_num=="O":
                    Pan=Pan.replace(temp_num,"0")
                if temp_num=="S":
                    Pan=Pan.replace(temp_num,"5")
                if temp_num=="B":
                    Pan=Pan.replace(temp_num,"8")
                if temp_num=="G":
                    Pan=Pan.replace(temp_num,"6")
                if temp_num=="I":
                    Pan=Pan.replace(temp_num,"1")
                if temp_num=="$":
                    Pan=Pan.replace(temp_num,"5")
            temp_pan_nums=Pan[5:10]

            Pan = temp_pan_chrs + temp_pan_nums
            boolpan=re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', Pan)

            if boolpan:
                return Pan
            else:
                return ""
    else:
        return ""
