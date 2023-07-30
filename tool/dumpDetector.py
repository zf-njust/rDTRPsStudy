# __author__ = 'Zhifei Chen'

import parameter
import csv
import ast
import dump_python
import os
import numpy

# 1.Incompatible Assignment Types: Incompatible types in assignment
# 2.Incompatible Element Types: Container comprehension has incompatible types
# 3.Incompatible Argument Types: Argument Value has incompatible type
# 4.Incompatible Return Types: Return value has incompatible type
# 5.Incompatible SubType Method: Argument/Signature of subtype method incompatible with supertype
# 6.Incompatible Variable Types: Variable reference has incompatible types
# 7.Dynamic Element Deletion: del a[2]
# 8.Dynamic Attribute Deletion: del a.x
# 9.Dynamic Attribute Access: getattr

types_freq = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
argu_types = {}
assign_types = {}
var_types = {}


def analyzeArguTypes(record_item):
    # print(record_item)
    # print(record_item[4].split("has incompatible type \"")[1].split('\"')[0])
    # print(record_item[4].split("expected \"")[1].split('\"')[0])
    type1 = record_item[4].split("has incompatible type \"")[1].split('\"')[0]
    type2 = record_item[4].split("expected \"")[1].split('\"')[0]
    if type1.find("**dict") != -1 or type2.find("**dict") != -1 or (
            type1.find("Any") != -1 and type1.find("[") == -1) or (type2.find("Any") != -1 and type2.find("[") == -1):
        # print('False', record_item)
        return False
    if type1 in ['Real', 'float'] and type2 in ['Real', 'float']:
        # print('False', record_item)
        return False
    if (type1.startswith('list') or type1.startswith('tuple') or type1.startswith('dict') or type1.startswith(
            'set') or type1.startswith('Generator') or type1.startswith('Sequence') or type1.startswith(
        'Sized') or type1.startswith('Itera')) and (
            type2.startswith('list') or type2.startswith('tuple') or type2.startswith('dict') or type2.startswith(
        'set') or type2.startswith('Generator') or type2.startswith('Sequence') or type2.startswith(
        'Sized') or type2.startswith('Itera')):
        # print('False', record_item)
        return False
    if type1 < type2:
        key = type1 + ',' + type2
    else:
        key = type2 + ',' + type1
    if key not in argu_types:
        argu_types[key] = 1
    else:
        argu_types[key] += 1
    return True


def analyzeAssignTypes(record_item):
    # print(record_item)
    # print(record_item[4].split("has incompatible type \"")[1].split('\"')[0])
    # print(record_item[4].split("expected \"")[1].split('\"')[0])
    type1 = record_item[4].split("expression has type \"")[1].split('\"')[0]
    if record_item[4].find("variable has type \"") != -1:
        type2 = record_item[4].split("variable has type \"")[1].split('\"')[0]
    elif record_item[4].find("target has type \"") != -1:
        type2 = record_item[4].split("target has type \"")[1].split('\"')[0]
    else:
        # print('False', record_item)
        return False
    if type1.find("**dict") != -1 or type2.find("**dict") != -1 or (
            type1.find("Any") != -1 and type1.find("[") == -1) or (type2.find("Any") != -1 and type2.find("[") == -1):
        # print('False', record_item)
        return False
    if type1 in ['Real', 'float'] and type2 in ['Real', 'float']:
        # print('False', record_item)
        return False
    if (type1.startswith('list') or type1.startswith('tuple') or type1.startswith('dict') or type1.startswith(
            'set') or type1.startswith('Generator') or type1.startswith('Sequence') or type1.startswith(
            'Sized') or type1.startswith('Itera')) and (
            type2.startswith('list') or type2.startswith('tuple') or type2.startswith('dict') or type2.startswith(
        'set') or type2.startswith('Generator') or type2.startswith('Sequence') or type2.startswith(
        'Sized') or type2.startswith('Itera')):
        # print('False', record_item)
        return False
    if type1 < type2:
        key = type1 + ',' + type2
    else:
        key = type2 + ',' + type1
    if key not in assign_types:
        assign_types[key] = 1
    else:
        assign_types[key] += 1
    return True


def walkDirectory(rootdir):
    for root, dirs, files in os.walk(rootdir):
        for name in files:
            if (os.path.splitext(name)[1][1:] == 'py'):
                yield os.path.join(root, name)


def count_lines(node):
    childnodes = list(ast.walk(node))
    lines = [0]
    for n in childnodes:
        if hasattr(n, 'lineno'):
            lines.append(n.lineno)
    return max(lines)


def getProjectSize(proj_name):
    project_dir = parameter.Subject_Dir + proj_name
    lines = 0
    files = 0
    for currentFileName in walkDirectory(project_dir):
        files = files + 1
        try:
            astContent = dump_python.parse_file(currentFileName)
        except:
            print(project_dir, currentFileName)
            continue
        lines = lines + count_lines(astContent)
    return lines


def countBadPractices(output_root, subjects):
    global types_freq
    subject_counts = []
    for proj_name in subjects:
        # print proj_name
        subject_item = [proj_name, 0, 0, 0, 0, 0, 0]
        # count mypysmells
        mypysmell_record = csv.reader(open(output_root + proj_name + '\\incompatible_mypy.csv'))
        for record in mypysmell_record:
            if mypysmell_record.line_num == 1:
                continue
            elif record[3] == 'argument' and analyzeArguTypes(record):
                subject_item[2] += 1
                types_freq[2].append([proj_name] + record)
            elif record[3] == 'assignment' and analyzeAssignTypes(record):
                subject_item[1] += 1
                types_freq[1].append([proj_name] + record)
        # count statictype smells
        statictype_record = csv.reader(open(output_root + proj_name + '\\incompatible_var.csv'))
        for record in statictype_record:
            if statictype_record.line_num == 1:
                continue
            types = sorted(record[-1].split(','))
            if "?" in types:
                types.remove("?")
            types = list(set(types))
            types = ','.join(types)
            if types not in var_types:
                var_types[types] = 1
            else:
                var_types[types] += 1
            subject_item[3] += 1
            types_freq[3].append([proj_name] + record)
        # count dynamic smells
        dynamicpatterns_record = csv.reader(open(output_root + proj_name + '\\dynamic_patterns.csv'))
        for record in dynamicpatterns_record:
            if dynamicpatterns_record.line_num == 1:
                continue
            if record[1] == 'delsubscript':
                subject_item[4] += 1
                types_freq[4].append([proj_name] + record)
            elif record[1] == 'delattribute':
                subject_item[5] += 1
                types_freq[5].append([proj_name] + record)
            elif record[1] == 'getattr':
                subject_item[6] += 1
                types_freq[6].append([proj_name] + record)
        subject_item = subject_item + [sum(subject_item[1:]), getProjectSize(proj_name)]
        subject_counts.append(subject_item)
    for i in subject_counts:
        print(i)
    record_file = csv.writer(open('assignment100.csv', 'w', newline=''))
    record_file.writerows(types_freq[1])
    record_file = csv.writer(open('argument100.csv', 'w', newline=''))
    record_file.writerows(types_freq[2])
    record_file = csv.writer(open('reference100.csv', 'w', newline=''))
    record_file.writerows(types_freq[3])
    record_file = csv.writer(open('delsubscript100.csv', 'w', newline=''))
    record_file.writerows(types_freq[4])
    record_file = csv.writer(open('delattribute100.csv', 'w', newline=''))
    record_file.writerows(types_freq[5])
    record_file = csv.writer(open('getattr100.csv', 'w', newline=''))
    record_file.writerows(types_freq[6])
    record_file = csv.writer(open('assigntypes.csv', 'w', newline=''))
    sortdata = sorted(assign_types.items(), key=lambda k: k[1], reverse=True)
    record_file.writerows(sortdata)
    record_file = csv.writer(open('argumenttypes.csv', 'w', newline=''))
    sortdata = sorted(argu_types.items(), key=lambda k: k[1], reverse=True)
    record_file.writerows(sortdata)
    record_file = csv.writer(open('referencetypes.csv', 'w', newline=''))
    sortdata = sorted(var_types.items(), key=lambda k: k[1], reverse=True)
    record_file.writerows(sortdata)
    return subject_counts


def writeAllBadPractices():
    record_file = csv.writer(open('practices_count100.csv', 'w', newline=''))
    record_file.writerow(['subject', 'Incompatible Assignment Types', 'Incompatible Argument Types',
                          'Incompatible Variable Types', 'Dynamic Element Deletion', 'Dynamic Attribute Deletion',
                          'Dynamic Attribute Access', 'Total', 'LOC'])
    record_file.writerows(countBadPractices(parameter.Data_Dir, parameter.Project_Names))


def analyzeDomain():
    projects_record = csv.reader(open('practices_count100'))
    proj_dict = {}
    for item in projects_record:
        if projects_record.line_num == 1:
            continue
        proj_dict[item[0]] = item[1:]
    for k, v in parameter.Domain_Dict.items():
        total = [k, len(v), 'Total', sum([proj_dict[proj][0] for proj in v]),
                 sum([proj_dict[proj][1] for proj in v]),
                 sum([proj_dict[proj][2] for proj in v]),
                 sum([proj_dict[proj][3] for proj in v]),
                 sum([proj_dict[proj][4] for proj in v]),
                 sum([proj_dict[proj][5] for proj in v]),
                 sum([proj_dict[proj][6] for proj in v]),
                 sum([proj_dict[proj][7] for proj in v])]
        med = [k, len(v), 'Median', 0, 0, 0, 0, 0, 0, 0, 0]
        numpy.median()


if __name__ == '__main__':
    # writeAllBadPractices()
    analyzeDomain()
