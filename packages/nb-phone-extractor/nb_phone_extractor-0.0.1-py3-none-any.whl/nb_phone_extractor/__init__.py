import pandas as pd
import numpy as np
import spacy
import os
import pickle
import argparse
import xlsxwriter
import xlrd
import textwrap

def ExtractTokensFromDoc(vocab_list,document):
    words = []
    
    for token in document:
        if token in vocab_list:
            words.append(token)
    return words #a list of tokens inside the vocab_list and document

def argmax_dict(dictionary):
    highest_key = None
    highest_value = None
    for key in dictionary.keys():
        value = dictionary[key]
        if highest_value == None or value > highest_value:
            highest_key = key
            highest_value = value
            
    return highest_key

def ApplyMultinomialNB(class_list, vocab_list, prior, condprob, document):
    import math
    
    score = {}
    
    words = ExtractTokensFromDoc(vocab_list,document)
    for classification in class_list:
        score[classification] = math.log(prior[classification],10)
        for token in words:
            score[classification] += math.log(condprob[token][classification],10)
    
#     print(score)
    return argmax_dict(score)

def get_trained_data(): #input nothing, output class_list, vocab_list, prior, condprob
    #Get the head from path
    this_dir, _ = os.path.split(__file__)
    
    #Get documents variable (trng set)
    data_path = os.path.join(this_dir, 'training_data_long.pickle')
    pickle_in = open(data_path,"rb")
    documents = pickle.load(pickle_in)
    pickle_in.close()

    class_list = documents.columns.values.tolist()

    #Get output from Classifier Training
    data_path = os.path.join(this_dir, 'vocab_list_long.pickle')
    pickle_in = open(data_path,"rb")
    vocab_list = pickle.load(pickle_in)
    pickle_in.close()

    data_path = os.path.join(this_dir, 'prior_long.pickle')
    pickle_in = open(data_path,"rb")
    prior = pickle.load(pickle_in)
    pickle_in.close()

    data_path = os.path.join(this_dir, 'condprob_long.pickle')
    pickle_in = open(data_path,"rb")
    condprob = pickle.load(pickle_in)
    pickle_in.close()

    return [class_list, vocab_list, prior, condprob]

def process_test_data(files = 'all'):#input: list of files/'all', output: a list of list of tokenized words & translation list
    #Preprocess Excel Sheet(s) to be analyzed
    excel_files = []

    if files == 'all':
        curr_dir_items = os.listdir()
    else:
        curr_dir_items = files

    for item in curr_dir_items:
        if '.xlsx' in item or '.xls' in item:
            excel_files.append(item)

    test_set = []
    sheet_name_list = []
    i = 0
    for file in excel_files:
        xl = pd.ExcelFile(file)
        print('The current excel file is',file)
        sheets = xl.book.sheets()
        
        for sheet in sheets:
            print(i, sheet.name)
            sheet_name_list.append(sheet.name)
            test_document = pd.read_excel(file,sheet.name)
            test_document.set_index(pd.Series([i for i in range(len(test_document))]),inplace = True)
            test_set.append(test_document)
            i += 1

        print('')

    #Convert the list of excel sheets/dataframes (trng set) into a list of lists, with each internal list containing more lists that contain the tokenized form of each row in an excel sheet/dataframe
    print('Converting pandas df into list form with data cleaned')
    full_dataframe_list = []
    for dataframe in test_set: # for each excel_file found in list
        
        # Data cleaning
        # take out NaN
        dataframe = dataframe.fillna('nan', inplace = False)
        for column_name in dataframe.columns:
            #remove non ascii characters
            column = dataframe[column_name]
            column = column.str.replace('[^\w\s]',' ')
            #remove all numbers
            for row_no in range(len(column)):
                string = str(column[row_no])
                column[row_no] = ''.join([i for i in string if not i.isdigit()])
            #lowercase all strings
            column = column.str.lower()
            
            #consolidate all changes
            dataframe[column_name] = column
            
        dataframe_list = dataframe.values.tolist()
        full_dataframe_list.append(dataframe_list)
    print('Conversion Done')
    
    # tokenizing section
    print('Tokenizing each line in each excel file')
    tokenized_dataframe_list = []
    translation_list = [] #list to link between row in tokenized_dataframe_list and Original row from dataframe
    nlp = spacy.load('en_core_web_sm')

    for excel_sheet in full_dataframe_list:
        tokenized_dataframe_list.append([])
        i = 0
        translation_list.append([])
        for row in excel_sheet:
            tokenized_dataframe_list[-1].append([])
            for phrase in row:
                if str(phrase) == 'nan':
                    continue
                else:
                    doc = nlp(str(phrase))
                    for token in doc:
                        tokenized_dataframe_list[-1][-1].append(str(token))
            
            #if the last list was empty, then lets remove it
            if not bool(tokenized_dataframe_list[-1][-1]):
                tokenized_dataframe_list[-1] = tokenized_dataframe_list[-1][:-1]
            #last list was not empty, so add index of item in original dataframe to the translation_list
            else:
                translation_list[-1].append(i)
            
            i += 1
    print('Tokenizing Done\n')
    
    return [test_set, tokenized_dataframe_list, translation_list, sheet_name_list]

def extract_data(trng_data, test_data , label = 'standard'):
    #input: class_list, vocab_list, prior, condprob, test_set, tokenized_dataframe_list, translation_list, sheet_name_list
    #output: None, since it writes to excel file
    
    class_list, vocab_list, prior, condprob = trng_data[0], trng_data[1], trng_data[2], trng_data[3]
    test_set, tokenized_dataframe_list, translation_list, sheet_name_list = test_data[0],test_data[1],test_data[2],test_data[3]

    if label == 'standard':
        key_labels = ['os','rom_memory','ram_memory','battery','display_size','primary_camera','secondary_camera','chipset']
    else:
        key_labels = label
    
    # Create the Excel File
    writer = pd.ExcelWriter('extracted_data.xlsx', engine='xlsxwriter')
    writer.save()
    print('Created extracted_data.xlsx')

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('extracted_data.xlsx', engine='xlsxwriter')

    # For each excel sheet, get the data in it and sheet name
    for i in range(len(tokenized_dataframe_list)):
        sheet = tokenized_dataframe_list[i]
        sheetname = sheet_name_list[i]
        results = {label : [] for label in key_labels}
        
    # Create sheet that contains the key details of each phone
        for j in range(len(sheet)):
            document = sheet[j]
            original_document = test_set[i].loc[translation_list[i][j]].tolist()
            original_document_str = ' '.join([str(item) for item in original_document if str(item) != 'nan'])
            classification = ApplyMultinomialNB(class_list, vocab_list, prior, condprob, document)
            if classification in results.keys():
                print(original_document_str, classification)
                results[classification].append(original_document_str)
                
    # Convert the list of key details from list to dataframe
        df = pd.DataFrame(dict([ (key,pd.Series(value)) for key, value in results.items() ]))

    # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name=sheetname, index=False)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    print('')
    print('The extracted details have been saved into extracted_data.xlsx at', os.getcwd())

def wrapper():
    # Load training set data first
    trng_data = get_trained_data()

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description = textwrap.dedent('''\
Default Behaviour:
Extract following info from all Excel files in current directory

1. OS
2. ROM
3. RAM
4. Battery
5. Display Size
6. Primary Camera
7. Secondary Camera
8. Chipset
'''))

    class_list = trng_data[0]
    available_labels = ' '.join([str(count) + '. ' + ele for count, ele in enumerate(class_list,1)])
    parser.add_argument("-l", "--label", nargs = "*", default = 'standard', help = '''Specify explicitly which labels to extract.
                                                                            You can choose from the following: '''+ available_labels)

    parser.add_argument('-f','--file', nargs = '*', default = 'all', help = 'Specify explicitly which excel files to be processed')
    
    args = parser.parse_args()

    if args.label == 'standard':
        label = 'a standard set of labels'
    else:
        label = ', '.join(args.label)

    if args.file == 'all':
        file = 'all files'
    else:
        file = ', '.join (args.file)

    print('I have received a command to extract ' + label + ' from ' + file + '\n')
    test_data = process_test_data(args.file)
    extract_data(trng_data, test_data, args.label)
