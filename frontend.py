import PySimpleGUI as sg 
from sys import platform
import webbrowser
import pytesseract as pt
import pdf2image
import os
import re
import ntpath


#do you want the raw content as well for refining search or are you feeling lucky?

#where are we putting the finished files?
layout = [
    [sg.Text("PDFtoTXT", font=('arial', 35, 'bold'))],
    [sg.Text('PDF to scan:'), sg.Input('', size=(45, 1), key='MOFO', disabled=True), sg.Button('File'), sg.Button('Folder')],
    [sg.Text("Where it'll be placed:"), sg.Input('', size=(45, 1), key='BOFO', disabled=True), sg.FolderBrowse(target='BOFO')],
    [sg.Checkbox('', default=True, tooltip='Toggle the search function.', key='SEARCH'), sg.Text('Search Terms: '), sg.Input('', key='INPUT'), sg.Button('Syntax')],
    [sg.Input('', visible=False, key='WHICH')],
    [sg.Button('GO', size=(60,2), bind_return_key=True), sg.Checkbox('Raw Content\nOutput', key='RCO', tooltip='This will output a SEPARATE file with\nALL text the program could grab from the\nPDF, as opposed to what you were searching for.')],
    [sg.Text('', key='STATUS', size=(60,1))]

]

window = sg.Window('PRSR', layout)

###FUNC###

def dothething(pdfpath):   #done

    pages = pdf2image.convert_from_path(pdf_path=pdfpath, dpi=300, size=(1654,2340))
    stuff = ''
    for i in range(len(pages)):
        content = pt.image_to_string(pages[i], lang='eng')
        stuff += content
    return stuff    

def filecontent(fileIN, folderOUT):     #done
    name1 = ntpath.split(fileIN)
    name = name1[1].split('.')
    phyle = open(f'{folderOUT}/{name[0]}_content.txt', 'a+')
    phyle.write(dothething(fileIN))
    phyle.close()
            
def foldercontent(folderIN, folderOUT):   #done
    for filename in os.listdir(folderIN):
        lilpath = os.path.join(folderIN, filename)

        if os.path.isdir(lilpath):
            print(lilpath + ' is a folder')
        
        else:
            name = filename.split('.')
            phyle = open(f'{folderOUT}/{name[0]}_content.txt', 'a+')
            phyle.write(dothething(lilpath))
            phyle.close()

def foldercontentsearch(folderIN, folderOUT, searchterm): #done
    for filename in os.listdir(folderIN):
        lilpath = os.path.join(folderIN, filename)

        if os.path.isdir(lilpath):
            print('gotteem')
        
        else:                
            name = filename.split('.')
            fyle = open(f'{folderOUT}/{name[0]}.txt', 'a+')
            phyle = open(f'{folderOUT}/{name[0]}_content.txt', 'a+')
            content = dothething(lilpath)
            phyle.write(content)
            criterion = re.compile(fr'{searchterm}')
            DIA_PT254 = criterion.findall(content)

            for thing in DIA_PT254:
                fyle.writelines(thing + '\n')

            fyle.close()
            phyle.close()

def filecontentsearch(fileIN, folderOUT, searchterm): #done
    name1 = ntpath.split(fileIN)
    name = name1[1].split('.')
    fyle = open(f'{folderOUT}/{name[0]}.txt', 'a+')
    phyle = open(f'{folderOUT}/{name[0]}_content.txt', 'a+')
    content = dothething(fileIN)
    phyle.write(content)
    criterion = re.compile(fr'{searchterm}')
    DIA_PT254 = criterion.findall(content)

    for thing in DIA_PT254:
        fyle.writelines(thing + '\n')
    
    fyle.close()
    phyle.close()

def foldersearch(folderIN, folderOUT, searchterm):  #done
    for filename in os.listdir(folderIN):
        lilpath = os.path.join(folderIN, filename)

        if os.path.isdir(lilpath):
            print(lilpath + ' is a folder')
        
        else:
            name = filename.split('.')
            fyle = open(f'{folderOUT}/{name[0]}.txt', 'a+')
            content = dothething(lilpath)
            criterion = re.compile(fr'{searchterm}')
            DIA_PT254 = criterion.findall(content)

            for thing in DIA_PT254:
                fyle.writelines(thing + '\n')

            fyle.close()

def filesearch(fileIN, folderOUT, searchterm): #done
    name1 = ntpath.split(fileIN)
    name = name1[1].split('.')
    fyle = open(f'{folderOUT}/{name[0]}.txt', 'a+')
    content = dothething(fileIN)
    criterion = re.compile(fr'{searchterm}')
    DIA_PT254 = criterion.findall(content)

    for thing in DIA_PT254:
        fyle.writelines(thing + '\n')

    fyle.close()



while True:
    event, values = window.read(100)
    
    if values == None:
        break 

    elif values['SEARCH'] == False and values['RCO'] == False:
        window['RCO'].Update(True)

    if event == None:
        break

    elif event == 'Folder':
        window['WHICH'].Update('Folder')
        foldername = sg.popup_get_folder('Which folder?')
        if foldername == None or '':
            print('none')
        else:
            window['MOFO'].Update(foldername)

    elif event == 'File':
        window['WHICH'].Update('File')
        filename = sg.popup_get_file('Which file?')
        if filename == None or '':
            print('none')
        else:
            window['MOFO'].Update(filename)
    
    elif event == 'Syntax':
        if platform == 'linux' or 'linux2':
            webbrowser.get("/usr/bin/google-chrome %s").open('https://docs.python.org/3/howto/regex.html')
        elif platform == 'win32':
            webbrowser.get('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s').open('https://docs.python.org/3/howto/regex.html')

    
    elif event == 'GO':

        if values['WHICH'] == 'File':
            if values['Browse'] == '':
                sg.popup('Pick an output destination')
            else:
                if values['SEARCH'] == True:
                    if values['INPUT'] == None or '':
                        sg.popup('Enter a search term\nor uncheck the box\nnext to the search bar')
                    else:
                        if values['RCO'] == True:
                            window['STATUS'].Update('Running...')
                            filecontentsearch(values['MOFO'], values['BOFO'], values['INPUT'])
                            window['STATUS'].Update('Finished.')
                        else:
                            window['STATUS'].Update('Running...')
                            filesearch(values['MOFO'], values['BOFO'], values['INPUT'])
                            window['STATUS'].Update('Finished.')             
                else:
                    window['STATUS'].Update('Running...')
                    filecontent(values['MOFO'], values['BOFO'])
                    window['STATUS'].Update('Finished.')


                    
        elif values['WHICH'] == 'Folder':
            if values['Browse'] == '':
                sg.popup('Pick an output destination')
            else:
                if values['SEARCH'] == True:
                    if values['INPUT'] == None or '':
                        sg.popup('Enter a search term\nor uncheck the box\nnext to the search bar')
                    else:
                        if values['RCO'] == True:
                            window['STATUS'].Update('Running...')
                            foldercontentsearch(values['MOFO'], values['BOFO'], values['INPUT'])
                            window['STATUS'].Update('Finished.')
                        else:
                            window['STATUS'].Update('Running...')
                            foldersearch(values['MOFO'], values['BOFO'], values['INPUT'])
                            window['STATUS'].Update('Finished.')             
                else:
                    window['STATUS'].Update('Running...')
                    foldercontent(values['MOFO'])
                    window['STATUS'].Update('Finished.')
                
        elif values['WHICH'] == '':
            sg.popup('Pick a File/Folder')
    

window.close()
