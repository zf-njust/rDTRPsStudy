# __author__ = 'Zhifei Chen'

import csv
import os
import parameter
import PatternAST
import dump_python


# modules methods linenos

def writeMethodsPatterns():
    for proj_name in parameter.Project_Names:
        print("processing", proj_name)
        project_dir = parameter.Subject_Dir + proj_name
        result_dir = parameter.Data_Dir + proj_name
        if not os.path.exists(result_dir):
            os.mkdir(result_dir)
        linenos_out_file = csv.writer(open(result_dir + '\methods_info.csv', 'w', newline=''))
        linenos_out_file.writerow(['file', 'method', 'params', 'startlineno', 'endlineno'])
        patterns_out_file = csv.writer(open(result_dir + '\dynamic_patterns.csv', 'w', newline=''))
        patterns_out_file.writerow(['file', 'pattern', 'lineno'])
        for root, dirs, files in os.walk(project_dir):
            for pyfile in files:
                if pyfile.endswith('.py'):
                    file_path = os.path.join(root, pyfile)
                    file_name = file_path[len(project_dir) + 1:]
                    # print file_path
                    # print file_name
                    try:
                        astContent = dump_python.parse_file(file_path)
                        myast = PatternAST.PatternAST()
                        myast.source = dump_python.get_source(file_path)
                        myast.visit(astContent)
                        for method in myast.methods:
                            linenos_out_file.writerow([file_name] + method)
                        for pattern in myast.patterns:
                            patterns_out_file.writerow([file_name] + pattern)
                    except Exception as e:
                        print('parse error', proj_name, file_name, e)
                        continue

    # patAST = myAST.PatternAST()
    # astContent = customast.parse_file('test.py')


if __name__ == '__main__':
    writeMethodsPatterns()
