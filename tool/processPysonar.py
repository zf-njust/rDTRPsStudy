__author__ = 'Zhifei Chen'

import parameter
import os
import csv


def convertPysonarSummary():
    for proj_name in parameter.Project_Names:
        pysonar_path = parameter.Pysonar_Dir + proj_name
        if not os.path.exists(pysonar_path):
            continue
        print("processing", proj_name)
        output_path = parameter.Pysonar_Dir + proj_name
        proj_path = parameter.Subject_Dir + proj_name
        binding_record = csv.writer(open(output_path + '\\all-bindings.csv', 'w', newline=''))
        binding_record.writerow(['id', 'var', 'file', 'lineno', 'offset_start', 'offset_end'])
        txt_record = open(parameter.Pysonar_Dir + proj_name + '\\all-bindings.txt').readlines()
        total_record = []
        for record in txt_record:
            # [id] <var> <file#lineno:offset_start-offset_end>
            id = int(record[1:record.index(']')])
            var = record[record.index('<') + 1:record.index('>')]
            file = record.split('<')[-1].split('#')[0]
            lineno = int(record.split('<')[-1].split('#')[1].split(':')[0])
            offset_start = int(record.split('<')[-1].split('#')[1].split(':')[1].split('-')[0])
            offset_end = int(record.split('<')[-1].split('#')[1].split(':')[1].split('-')[1].split('>')[0])
            if file.startswith(proj_path):
                total_record.append([id, var, file[len(proj_path) + 1:], lineno, offset_start, offset_end])
        total_record.sort(key=lambda k: (k[2], k[3]))
        binding_record.writerows(total_record)
        references_record = csv.writer(open(output_path + '\\all-references.csv', 'w', newline=''))
        references_record.writerow(['id', 'var', 'file', 'lineno', 'offset_start', 'offset_end', 'ref_id'])
        txt_record = open(parameter.Pysonar_Dir + proj_name + '\\all-references.txt').readlines()
        total_record = []
        for record in txt_record:
            # [id] <var> <file#lineno:offset_start-offset_end> <ref_id>
            id = int(record[1:record.index(']')])
            var = record[record.index('<') + 1:record.index('>')]
            file = record.split('<')[2].split('#')[0]
            lineno = int(record.split('<')[2].split('#')[1].split(':')[0])
            try:
                offset_start = int(record.split('<')[2].split('#')[1].split(':')[1].split('-')[0])
                offset_end = int(record.split('<')[2].split('#')[1].split(':')[1].split('-')[1].split('>')[0])
            except:
                print(record)
                continue
            ref_id = record.split('<')[-1].split('>')[0]
            # print record, id, var, file, lineno, offset_start, offset_end, ref_id
            if file.startswith(proj_path):
                total_record.append([id, var, file[len(proj_path) + 1:], lineno, offset_start, offset_end, ref_id])
        total_record.sort(key=lambda k: (k[2], k[3]))
        references_record.writerows(total_record)


def getAllBinsRefs(proj_name):
    proj_path = parameter.Subject_Dir + proj_name
    binding_record = []  # ['id', 'var', 'file', 'lineno', 'offset_start', 'offset_end'])
    txt_record = open(parameter.Pysonar_Dir + proj_name + '\\all-bindings.txt').readlines()
    for record in txt_record:
        # [id] <var> <file#lineno:offset_start-offset_end>
        id = int(record[1:record.index(']')])
        var = record[record.index('<') + 1:record.index('>')]
        file = record.split('<')[-1].split('#')[0]
        lineno = int(record.split('<')[-1].split('#')[1].split(':')[0])
        offset_start = int(record.split('<')[-1].split('#')[1].split(':')[1].split('-')[0])
        offset_end = int(record.split('<')[-1].split('#')[1].split(':')[1].split('-')[1].split('>')[0])
        if file.startswith(proj_path):
            binding_record.append([id, var, file[len(proj_path) + 1:], lineno, offset_start, offset_end])
    binding_record.sort(key=lambda k: (k[2], k[3]))

    reference_record = []  # ['id', 'var', 'file', 'lineno', 'offset_start', 'offset_end', 'ref_id'])
    txt_record = open(parameter.Pysonar_Dir + proj_name + '\\all-references.txt').readlines()
    for record in txt_record:
        # [id] <var> <file#lineno:offset_start-offset_end> <ref_id>
        id = int(record[1:record.index(']')])
        var = record[record.index('<') + 1:record.index('>')]
        file = record.split('<')[2].split('#')[0][len(proj_path) + 1:]
        lineno = int(record.split('<')[2].split('#')[1].split(':')[0])
        try:
            offset_start = int(record.split('<')[2].split('#')[1].split(':')[1].split('-')[0])
        except:
            print(record)
            continue
        offset_end = int(record.split('<')[2].split('#')[1].split(':')[1].split('-')[1].split('>')[0])
        ref_id = record.split('<')[-1].split('>')[0]
        # print record, id, var, file, lineno, offset_start, offset_end, ref_id
        if file.startswith(proj_path):
            reference_record.append([id, var, file[len(proj_path) + 1:], lineno, offset_start, offset_end, ref_id])
    reference_record.sort(key=lambda k: (k[2], k[3]))

    return binding_record, reference_record


# def convertPysonarResult():
#     for proj_name in parameter.Project_Names:
#         pysonar_path = parameter.Pysonar_Dir+proj_name
#         if not os.path.exists(pysonar_path):
#             continue
#         print "processing", proj_name
#         for root, dirs, files in os.walk(pysonar_path):
#             for name in files:
#                 if root == pysonar_path and (name=='all-bindings.txt' or name=='all-constraints.txt'\
#                                            or name=='all-references.txt' or name=='all-typeattrs.txt'):
#                     continue
#                 print root + '\\' + name


if __name__ == '__main__':
    convertPysonarSummary()
