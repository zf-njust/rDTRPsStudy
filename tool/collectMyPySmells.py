# __author__ = 'Zhifei Chen'


import parameter
import os
import csv
import subprocess


def dump_mypy_results(name):
    project_dir = parameter.Subject_Dir + name
    result_dir = parameter.Data_Dir + name
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    out_file = open(result_dir + '\mypy_result.txt', 'w+')
    reduce_repet_record = []
    os.chdir(project_dir)
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                file_path = file_path[len(project_dir) + 1:]
                file_path = '"' + file_path + '"'
                # print(file_path)
                txt_tmp_file = 'txt_tmp_type.txt'
                shell_script = 'D:\software\python\Scripts\mypy ' + \
                               file_path + \
                               ' --ignore-missing-imports --show-column-numbers --check-untyped-defs' + \
                               ' > ' + txt_tmp_file
                subprocess.call(shell_script, shell=True)

                with open(txt_tmp_file, 'r') as f:
                    lines = f.readlines()
                    if len(lines) == 0:
                        continue
                    for line in lines:
                        # print line
                        if line not in reduce_repet_record:
                            out_file.write(line)
                            reduce_repet_record.append(line)
                        # line = line.strip(' \t\n').replace('\\', '/')
                        # line = line[2:]
                        # #print('line')
                        # if 'error: Incompatible types' in line and not 'string interpolation' in line:
                        #     result_dict['IC1'] += 1
                        # elif 'Argument' in line and 'has incompatible type' in line:
                        #     result_dict['IC2'] += 1
                        # elif 'string interpolation' in line:
                        #     result_dict['IC3'] += 1
                try:
                    os.remove(txt_tmp_file)
                except FileNotFoundError:
                    print(txt_tmp_file + ' not found')
    out_file.close()
    # os.chdir(parameter.Subject_Dir)
    # shell_script = 'C:\software\python36\Scripts\mypy ' + \
    #                            name + \
    #                            ' --ignore-missing-imports --show-column-numbers --check-untyped-defs' + \
    #                            ' > ' + result_dir+'\mypy_result.txt'
    # subprocess.call(shell_script, shell=True)


CompatibleTypes = [{'MIMEBase', 'MIMEText'},
                   {'Type[SESIdentityNotVerifiedError]', 'Type[SESAddressBlacklistedError]',
                    'Type[SESLocalAddressCharacterError]', 'Type[SESDomainEndsWithDotError]',
                    'Type[SESDomainNotConfirmedError]', 'Type[SESMaxSendingRateExceededError]',
                    'Type[SESDailyQuotaExceededError]', 'Type[SESAddressNotVerifiedError]',
                    'Type[SESIllegalAddressError]'},
                   {'Type[PollSelector]', 'Type[EpollSelector]', 'Type[KqueueSelector]', 'Type[SelectSelector]'},
                   {'WebSocketsWriter', 'StreamWriterAdapter'},
                   {'WebSocketsReader', 'StreamReaderAdapter'},
                   {'ExternalQuestion', 'QuestionForm', 'HTMLQuestion'},
                   {'Type[DummyConnection]', 'Type[HTTPSConnection]'},
                   {'HTTPConnectionPool', 'Type[HTTPConnection]'},
                   {'LoggerAdapter', 'Logger'},
                   {'BufferedWriter', 'BufferedRWPair', 'IO[bytes]'},
                   {'BufferedReader', 'BufferedRWPair', 'IO[bytes]'},
                   {'Type[SecureTransportContext]', 'Type[PyOpenSSLContext]', 'Type[SSLContext]'},
                   {'RotatingFileHandler', 'StreamHandler'},
                   {'MultipleSort', 'NullSort'},
                   {'RangeKey', 'HashKey'},
                   {'Histogram', 'Counter'},
                   {'_SixMetaPathImporter', '_MetaPathFinder'},
                   {'Parameter', 'ChoiceParameter', 'IntParameter', '**Dict[str, Parameter]', 'str', 'int', 'float'},
                   {'Type[PolyphonicMidiCaptor]', 'Type[MonophonicMidiCaptor]'},
                   {'List[Any]', 'ValuesView[Any]'},
                   {'ItemsView[Any, Any]', 'List[Tuple[Any, Any]]'},
                   {'Type[NoPreprocessor]', 'Type[OneHotPreprocessor]', 'Type[GenericPixelPreprocessor]',
                    'Type[TupleFlatteningPreprocessor]', 'Type[DictFlatteningPreprocessor]',
                    'Type[AtariRamPreprocessor]'},
                   {'InputPostprocIgnoreList', 'InputPostprocCalibration', 'InputPostprocRetainTouch',
                    'InputPostprocTripleTap', 'InputPostprocDejitter', 'InputPostprocDoubleTap'},
                   {'MiddlePipelineThread', 'FirstPipelineThread', 'LastPipelineThread'},
                   {'Type[DateQuery]', 'Type[PathQuery]', 'Type[SubstringQuery]', 'Type[NumericQuery]',
                    'Type[DurationQuery]', 'Type[BooleanQuery]'}]


def isIncompatibleTypes(message):
    index = message.find("type \"")
    if index == -1:
        return False
    type1 = message[index + 6:].split('\"')[0]
    type2 = message.split('\"')[-2]
    # except:
    #     print(message)
    #     return False
    if type1 in ['None', 'Meta', 'object'] or type2 in ['None', 'Meta', 'object']:
        return False
    if type1 == 'QueueProcessingWorker' or type2 == 'QueueProcessingWorker':
        return False
    if type1.replace('bytes', 'str') == type2.replace('bytes', 'str'):
        return False
    if ((type1.startswith('List[') or type1.startswith('Tuple[') or type1.startswith('Sequence[') \
         or type1.startswith('Iterator[') or type1.startswith('Union[') or type1.startswith('map[') \
         or type1.startswith('Type[Tuple[') or type1.startswith('Type[List[') or type1.startswith('Collection[') \
         or type1.startswith('Dict[') or type1.startswith('Iterable[') or type1 == 'range') \
        and (type2.startswith('List[') or type2.startswith('Tuple[') or type2.startswith('Sequence[') \
             or type2.startswith('Iterator[') or type2.startswith('Union[') or type2.startswith('map[') \
             or type2.startswith('Type[Tuple[') or type2.startswith('Type[List[') or type2.startswith('Collection[')
             or type2.startswith('Dict[') or type2.startswith('Iterable[') or type2 == 'range')) \
            or (type1.startswith('Test') and type2.startswith('Test')) \
            or (type1.endswith('Error') and type2.endswith('Error')) \
            or (type1.endswith('IO') and type2.endswith('IO')) \
            or (type1.startswith('Optional[') or type2.startswith('Optional[')) \
            or (type1.startswith('Callable[') or type2.startswith('Callable[')):
        return False
    if type1.startswith(type2) or type1.endswith(type2) or type2.startswith(type1) or type2.endswith(type1):
        return False
    for type_group in CompatibleTypes:
        if type1 in type_group and type2 in type_group:
            return False
    return True


# incompatible container comprehensions:
#   1.{error: List comprehension has incompatible type List[Tuple[int, str, int, Dict[str, Dict[str, str]]]]; expected List[Tuple[int, str, int]]}
# incompatible argument types.
#   1.{error: Argument 1 to "Pos" has incompatible type "int"; expected "Iterable[Any]"}
# Incompatible return value type.:
#  1. {error: Incompatible return value type (got "bytes", expected "AwaitableGenerator[Any, Any, Any, bytes]")}
#  2. {error: The return type of a generator function should be "Generator" or one of its supertypes}
#  3. {error: The return type of "__init__" must be None}
# Incompatible types in assignment.
#  1. {error: Incompatible types in assignment (expression has type "List[Char]", variable has type "str")}
# Argument/Signature of subtype method incompatible with supertype:
#  1.{error: Signature of "render" incompatible with supertype "Component"}
#  2.{error: Argument 1 of "deserialize" incompatible with supertype "Observable"}
def collect_mypy_smells(name):
    mypy_result = open(parameter.Data_Dir + name + '\mypy_result.txt').readlines()
    incompatible_mypy = csv.writer(open(parameter.Data_Dir + name + '\\incompatible_mypy.csv', 'w', newline=''))
    incompatible_mypy.writerow(['file', 'lineno', '_lineno', 'kind', 'message'])
    for record in mypy_result:
        info = record.split(':')
        if len(info) < 5:
            # print(record)
            continue
        path = record.split(':')[0]
        lineno = record.split(':')[1]
        _lineno = record.split(':')[2]
        message = record.split(':')[-1].rstrip()
        if message.find('comprehension') != -1:
            # print(message)
            incompatible_mypy.writerow([path, lineno, _lineno, 'comprehension', message])
        if message.find('Argument') != -1 and message.find('has incompatible type') != -1:
            # print(message)
            if isIncompatibleTypes(message):
                incompatible_mypy.writerow([path, lineno, _lineno, 'argument', message])
        if message.find('Incompatible return value type') != -1 or message.find('The return type of') != -1:
            # print(message)
            incompatible_mypy.writerow([path, lineno, _lineno, 'return', message])
        if message.find('Incompatible types in assignment') != -1:
            # print(message)
            if isIncompatibleTypes(message):
                incompatible_mypy.writerow([path, lineno, _lineno, 'assignment', message])
        if message.find('incompatible with supertype') != -1:
            # print(message)
            incompatible_mypy.writerow([path, lineno, _lineno, 'sub/supertype', message])


def writeIncompatibleMyPy():
    for proj_name in parameter.Project_Names:
        print("processing", proj_name)
        dump_mypy_results(proj_name)
        collect_mypy_smells(proj_name)


if __name__ == '__main__':
    writeIncompatibleMyPy()
