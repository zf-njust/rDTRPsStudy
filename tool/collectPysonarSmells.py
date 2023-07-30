# __author__ = 'Zhifei Chen'

import csv
import os
import dump_python
import parameter
import ClassStructureAST
import processPysonar

CompatibleTypes_Append = [{'str', 'tuple'}, {'int', 'float'}, {'list', 'tuple'}, {'MIMEText', 'MIMEBase'},
                          {'type', 'module'},
                          {'HTTPSConnection', 'HTTPConnection'}, {'timedelta', 'datetime'}]


def getProjectClassGroups(proj_name):
    classgroups = []
    project_dir = parameter.Subject_Dir + proj_name
    for root, dirs, files in os.walk(project_dir):
        for pyfile in files:
            if pyfile.endswith('.py'):
                file_path = os.path.join(root, pyfile)
                file_name = file_path[len(project_dir) + 1:]
                # print file_path
                # print file_name
                try:
                    astContent = dump_python.parse_file(file_path)
                    myast = ClassStructureAST.ClassStructureAST(classgroups)
                    myast.visit(astContent)
                except Exception as e:
                    print('parse error', file_name, e)
                    continue
                classgroups = myast.classgroups
    # for item in classgroups:
    #     print item
    classgroups = classgroups + CompatibleTypes_Append
    return classgroups


# to test
def checkTypePair(var1, var2, compatible_types):
    if var1 in ['None', '?', 'type'] or var2 in ['None', '?', 'type']:
        return False
    if var1 == var2:
        return False
    for type_group in compatible_types:
        if var1 in type_group and var2 in type_group:
            return False
    else:
        if var1.lower().find(var2.lower()) != -1 or var2.lower().find(var1.lower()) != -1:
            # print 'Is Compatible? ', var1, var2
            return False
        else:
            return True


# to test
def checkTypeGroup(group, compatible_types):
    if len(group) == 0 or len(group) == 1:
        return False
    for i in range(len(group) - 1):
        for j in range(i + 1, len(group)):
            if checkTypePair(group[i], group[j], compatible_types):
                # print group[i], group[j], True
                return True
            # else:
            #     print group[i], group[j], False
    return False


def checkIncompatibleTypes(proj_name):
    methods_record = csv.reader(open(parameter.Data_Dir + proj_name + '\\methods_info.csv'))
    incompatible_var_record = csv.writer(
        open(parameter.Data_Dir + proj_name + '\\incompatible_var.csv', 'w', newline=''))
    incompatible_var_record.writerow(['file', 'method', 'params', 'startLineno', 'endLineno',
                                      'affectedLineno', 'affectedOffsets', 'affectedVar', 'affectedTypes'])
    incompatible_def_record = csv.writer(
        open(parameter.Data_Dir + proj_name + '\\incompatible_def.csv', 'w', newline=''))
    incompatible_def_record.writerow(['file', 'method', 'params', 'startLineno', 'endLineno',
                                      'var1', 'lineno1', 'offsets1', 'types1', 'var2', 'lineno2', 'offsets2', 'types2'])
    file2methods = {}  # methodName, params, startLineno, endLineno
    for method in methods_record:
        if methods_record.line_num == 1:
            continue
        (filePath, methodName, params, startLineno, endLineno) = method
        startLineno = int(startLineno)
        endLineno = int(endLineno)
        # print filePath, methodName, params, startLineno, endLineno
        if filePath not in file2methods.keys():
            file2methods[filePath] = [[methodName, params, startLineno, endLineno]]
        else:
            file2methods[filePath].append([methodName, params, startLineno, endLineno])
    compatible_types = getProjectClassGroups(proj_name)
    pysonar_root = parameter.Pysonar_Dir + proj_name
    # id, var, file, lineno, offset_start,offset_end, [ref id]
    all_bindings, all_references = processPysonar.getAllBinsRefs(proj_name)
    for root, dirs, files in os.walk(pysonar_root):
        for pyfile in files:
            if not pyfile.endswith('.py.txt'):
                continue
            file_path = os.path.join(root, pyfile)[len(pysonar_root) + 1:-4]
            # print file_path
            # if file_path!='tests\integration\dynamodb\\test_layer1.py':
            #     continue
            if file_path not in file2methods.keys():
                continue

            # prepare methods
            method_id = 1
            id2method = {}  # method_id:[methodName, params, startLineno, endLineno]
            for method in file2methods[file_path]:
                id2method[method_id] = method
                method_id += 1

            # prepare def bindings
            mid2bindings = {}  # mid:{def_records}

            # analyze types
            type_record = open(os.path.join(root, pyfile)).readlines()
            for record in type_record:
                var = record.split('<<')[1].split('>>')[0]
                lineno = int(record.split('<<')[2].split(':')[0])
                offsets = record.split('<<')[2].split('>>')[0].split(':')[1]
                types = record.split('<<')[3].split('>>')[0]
                types = types.lstrip('{').rstrip('}').split('||')
                kind = record.split('<<')[-1].split('>>')[0]
                current_mid = 0
                for mid in id2method.keys():
                    startLineno = id2method[mid][2]
                    endLineno = id2method[mid][3]
                    if lineno >= startLineno and lineno <= endLineno:
                        current_mid = mid
                        break
                if current_mid == 0:  # not in a method
                    continue
                if kind == 'LINK' and checkTypeGroup(types, compatible_types):
                    incompatible_var_record.writerow([file_path] + id2method[current_mid] +
                                                     [lineno, offsets, var, ','.join(types)])
                # record if is a binding
                for binding in all_bindings:  # id, var, file, lineno, offset_start,offset_end
                    if var == binding[1] and file_path == binding[2] and lineno == binding[3] and \
                            int(offsets.split('-')[0]) == binding[4] and int(offsets.split('-')[1]) == binding[5]:
                        # print binding, record
                        if current_mid not in mid2bindings.keys():
                            mid2bindings[current_mid] = [[var, lineno, offsets, types], ]
                        else:
                            for b in mid2bindings[current_mid]:
                                if var == b[0] and lineno == b[1] and offsets == b[2]:
                                    if kind == 'ANCHOR':
                                        print('Existed Anchor: ', file_path, record, b)
                                    break
                            else:
                                mid2bindings[current_mid].append([var, lineno, offsets, types])
                        break

            # check def type imcompatible
            for mid in mid2bindings.keys():
                method_bindings = mid2bindings[mid]
                # if file_path=='tests\integration\dynamodb\\test_layer1.py':
                #     print method_bindings
                for i in range(len(method_bindings) - 1):
                    for j in range(i + 1, len(method_bindings)):
                        if method_bindings[i][0] == method_bindings[j][0] and (
                                method_bindings[i][1] != method_bindings[j][1] or method_bindings[i][2] !=
                                method_bindings[j][2]):
                            if not checkTypeGroup(method_bindings[i][3], compatible_types) and \
                                    not checkTypeGroup(method_bindings[j][3], compatible_types) and \
                                    checkTypeGroup(method_bindings[i][3] + method_bindings[j][3], compatible_types):
                                incompatible_def_record.writerow(
                                    [file_path] + id2method[mid] + method_bindings[i] + method_bindings[j])


def writeIncompatibleTypes():
    for proj_name in parameter.Project_Names:
        print("processing", proj_name)
        checkIncompatibleTypes(proj_name)


if __name__ == '__main__':
    writeIncompatibleTypes()
