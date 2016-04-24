import csv
from pprint import pprint
"""
General Notes:


LIVING_QTRS:

Type of Living Quarters
01 House, apartment, flat, condo
02 HU in nontransient hotel, motel
03 HU-permanent in transient hotel, motel
04 HU in rooming house
05 Mobile home/trailer w/no permanent rooms added
06 Mobile home/trailer w/1+ permanent rooms added
07 HU not specified above
08 Quarters not HU in room or board house
09 Unit not permanent-transient hotel, motel
10 Unoccupied site for mobile home/trailer/tent
11 Student quarters in college dormitory
12 Group quarter unit not specified above
98 Not ascertained

NON_RESP:
Category of type A non-response
1 Refused
2 No one home - repeated calls
3 Temporarily absent
4 Language problem
5 Other

"""
def try_int(value):
    """
    Try to cast to int, if not return 0, because the problem
    with parsing some of these is that they at "00" which
    isn't a valid integer value
    """
    try:
        return int(value)
    except ValueError:
        return 0

def parse_family():
    """
Question ID             FinalDocName     Processing Variable Label                                   Location   Length
IDN.000_00.000          RECTYPE          File type identifier                                        1 - 2         2
IDN.000_02.000          SRVY_YR          Year of National Health Interview Survey                    3 - 6         4
IDN.000_04.000          HHX              Household Number                                            7 - 12        6
IDN.000_25.000          INTV_QRT         Interview Quarter                                           13            1
IDN.000_30.000          INTV_MON         Interview Month                                             14 - 15       2
IDN.000_65.000          WTIA_HH          Weight - Interim Annual                                     16 - 21       6
IDN.000_70.000          WTFA_HH          Weight - Final Annual                                       22 - 27       6
COV.260_00.000          LIVQRT           Type of Living Quarters                                     28 - 29       2
MHH.000_00.000          NON_INTV         Category of type A non-response                             30            1
MHH.000_00.000          ACPT_FAM         Number of families in HH responding                         31 - 32       2
MHH.000_00.000          REJ_FAM          Number of families in HH not responding                     33 - 34       2
MHH.000_00.000          ACPT_PER         Number of persons in HH responding                          35 - 36       2
MHH.000_00.000          REJ_PER          Number of persons in HH not responding                      37 - 38       2
MHH.000_00.000          ACPTCHLD         Number of children in HH that responded                     39 - 40       2
UCF.000_00.000          REGION           Region                                                      41            1
UCF.000_00.000          STRAT_P          Pseudo-stratum for public use file variance estimation      42 - 44       3
UCF.000_00.000          PSU_P            Pseudo-PSU for public use file variance estimation          45 - 46       2



    """
    ret_list = [] # list containing all the records that we will write to file

    familyData = open('familyxx.dat','r').readlines()
    for line in familyData:
        csv_dict_row = {
        'RECTYPE' : int(line[0:2])  , # int
        'SURVEY_YR' : int(line[2:6]), # int TODO: USE WITH INTERVW_MONTH for datetime object
        'HOUSE_NUM' : int(line[6:12]), # int  I believe it to be the Unique ID
        'INTERVW_QTR' : int(line[12]), # int
        'INTERVW_MONTH' : int(line[13:15]), # int
        'WEIGHT_INTERIM': int(line[15:21]), # int
        'WEIGHT_FINAL' : int(line[21:27]), # int
        'LIVING_QTRS' : int(line[27:29]), # int, ID highlighted above
        'NON_RESP' : try_int(line[29]), # int, if true probably should throw away
        'NUM_FAM_RESP': try_int(line[30:32]), # int
        'NUM_FAM_NON_RESP' : try_int(line[32:34]), # int
        'NUM_PPL_RESP' : try_int(line[34:36]), # int
        'NUM_PPL_NON_RESP': try_int(line[36:38]), # int
        'NUM_CHILD_RESP' : try_int(line[38:40]), # int
        'REGION' : int(line[40]), # int, pretty much useless
        'STRAT_P' : int(line[41:44]), # int, No idea what this is
        'PSU_P' : int(line[44:46]) # int, not a clue what this is either
        }
        ret_list.append(csv_dict_row)
    return ret_list

def parse_person_text():
    """
    The file to describe all of this stuff is very long ( approx. 650 Variables)
    So I'm writing a script to parse all that information automatically to make
    a dict containing all those variables

    Returns a list of strings and tuples containing the ranges
    """
    read1 = open('person_desc_small.txt','r')
    personDesc = read1.readlines()
    variable_names = []
    indices = []
    i = 0
    for x in xrange(0,len(personDesc)-23,24):
        curr_line = personDesc[x:x+24]
        curr_line = [x.strip('\n').strip() for x in curr_line]
        if i == 0:
            variable_names.extend(curr_line)
        if i == 1:
            tmp_value = None
            for elem in curr_line:
                try:
                    tmp_value = int(elem)-1
                except ValueError:
                    tmp_str = elem.split()
                    tmp_value = (int(tmp_str[0])-1,int(tmp_str[2]))
                indices.append(tmp_value)

        if i >= 2:
            break
        i+=1
    read1.close()
    read2 = open('person_desc.txt','r')
    personDesc = read2.readlines()
    for line in personDesc:
        line = line.split()
        if int(line[-1]) == 1:
            indices.append(int(line[-2])-1)
        else:
            indices.append((int(line[-4])-1,int(line[-2])))
        if len(line[1]) == 3 and line[1][0] == 'R':
            variable_names.append(line[3])
        else:
            variable_names.append(line[2])
    read2.close()
    return variable_names,indices

def try_types(elem):
    if elem.isspace():
        return None
    try:
        return int(elem)
    except ValueError:
        return elem

def parse_persons():
    """
    Check variable descriptions here: ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/NHIS/2014/personsx_summary.pdf

    Parses person file for data
    """
    csv_list = []
    variable_names, indices = parse_person_text()

    read_persons_file = open('personsx.dat','r')
    read_persons = read_persons_file.readlines()
    for line in read_persons:
        curr_dict = {}
        i = 0
        for name in variable_names:
            if type(indices[i]) == type(0):
                curr_dict[name] = try_types(line[indices[i]])
            else:
                curr_dict[name] = try_types(line[indices[i][0]:indices[i][1]])
            i+=1
        csv_list.append(curr_dict)
    read_persons_file.close()

    with open('persons.csv', 'w') as csvfile:
        fieldnames = variable_names
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for line in csv_list:
            writer.writerow(line)
        csvfile.close()
def check_file():
    f = open('persons.csv','r')
    i = 0
    while i < 2:
        print f.readline()
        i+=1
check_file()
