# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 10:06:31 2014

@author: Nick
"""
#import needed libararys
from tkinter.filedialog import askopenfilename


'''Step 1, import file to convert, the final result will export to the same directory as the orginial file.'''
#ask the user what file to convert
file_name =  askopenfilename()
print('Open file :',file_name)

with open (file_name, "r") as myfile:
    data=myfile.readlines()

    
'''Step 2, remove information prior to <gx:Track> and after </gx:Track> to have just the cordinate data.'''
#Functoin to find the start and end of the cordinate data
def find_Start_end(page):
    start = [i for i,x in enumerate(page) if x == '<gx:Track>\n']
    start = start[0]+2
    #print(start)
    end = [i for i,x in enumerate(page) if x == '</gx:Track>\n']
    end = end[0]-1
    #print(end)
    return start, end

#Function to slice the list and make a new list with just the cordinate data.
def remove_header_data(page):
    start, end = find_Start_end(data)
    new_page = page[start:end]
    return new_page
# Exicute Step 2
unfixed_cord_data = remove_header_data(data)

'''Step 3, wrangle the data, remove the <when> list items and correct the cordinate data format.'''
#Function to fix the formating of the x,y,z cordinates
def fix_cordinates(item):
    new_item = item.replace('<gx:coord>',"")
    new_item = new_item.replace('</gx:coord>',"")
    new_item = new_item.replace(' ',",")
    new_item = new_item.replace('\n'," ")
    return new_item

#Function to delet list items containing <when>    
def kill_when(page):
    new_page = [i for i in page if 'when' not in i]
    return new_page
    
#Function to cycle threw each item to fix its cordinates
def fix_all_cords(page):
    i = 0
    new_page=[]
    while i < len(page):
        new_page.append(fix_cordinates(page[i]))
        i=i+1
    return new_page


# Exicute Step 3
only_cord_data = kill_when(unfixed_cord_data)
cord_data = fix_all_cords(only_cord_data)

'''Step 4, Build the new file, put back better headers, make lines with 10000 points or less, with correct seperating code.'''

#Function to make a list of list spliting our cord_data into 10000 items or less lists.
def list_of_lists(page):
    i = 0
    index = 10000
    new_page=[]
    while i < len(page):     
        new_page.append(page[i:i + index])
        i= i + index +1
    return new_page

#Import good header, footer, and list item containers
file_name_header = "header_for_kml.txt"
print('Open file :',file_name_header)
with open (file_name_header, "r") as myfile:
    header_data=myfile.readlines()

myfile.close()
print('Close file :',file_name_header)

#Function to setup the header for construction the file later
def set_header(page):
    end_index = [i for i,x in enumerate(header_data) if x == '\t<Placemark>\n']
    end_index = end_index[0]
    return page[:end_index]

#Function to setup the tags that will go right before the cordiante blocks 
def set_item_start_tags(page):
    start_index = [i for i,x in enumerate(header_data) if x == '\t<Placemark>\n']
    start_index = start_index[0]
    end_index = [i for i,x in enumerate(header_data) if x == '\t\t\t<coordinates>\t\t\t\n']
    end_index = end_index[0]+1
    return page[start_index:end_index]
    
#Function to setup the tags that will go right after the cordiante blocks   
def set_item_end_tags(page):
    start_index = [i for i,x in enumerate(header_data) if x == '\t\t\t</coordinates>\n']
    start_index = start_index[0]
    end_index = [i for i,x in enumerate(header_data) if x == '\t</Placemark>\n']
    end_index = end_index[0]+1
    return page[start_index:end_index]

#Function to setup the footer for constructin of the file later
def set_footer(page):
    start_index = [i for i,x in enumerate(header_data) if x == '\t</Placemark>\n']
    start_index = start_index[0]+1
    return page[start_index:]


#Make the list of list
cord_list = list_of_lists(cord_data)

#make the list of lists, a list of srings
def list_to_strings(page):
    i = 0
    new_page=[]
    while i < len(page):
        new_page.append(''.join(page[i]))
        i=i+1
    return new_page

#Function to write the list of strings to our new file...
def build_cord_core(file,page):
    page
    i=0    
    while i < len(page):
        for e in set_item_start_tags(header_data):
            if e == '\t\t<name>Untitled Path</name>\n':
                d=i+1
                e = e.replace('Untitled Path',"Set %d" %d)              
                file.write(e)
            else:
                file.write(e)         
        file.write('\t\t\t\t' + page[i] + '\n')        
        for e in set_item_end_tags(header_data):
            file.write(e) 
        i = i+1
    return file

'''Step 5, output everything to a new txt file'''
#Genearte name from original file


#Function to adjust name so the output is .kml 
def adjust_name(item): 
    if item.find('.txt') != -1:
        item = item.replace('.txt',".kml")
    item = item.replace('.kml',"-corrected.kml")
    return item
 
#adjust file name   
new_file_name = adjust_name(file_name)

#Function to put the pieces of the file together
def build_file(file,page,cords):    
    for e in set_header(page):
        file.write(e)
    build_cord_core(file,list_to_strings(cords))
    for e in set_footer(page):
        file.write(e) 
    return file

#create new file with the new name.
edit_file = open(new_file_name, 'w')
print('created new file named :',new_file_name)   

#build the file and close it
build_file(edit_file,header_data,cord_list)    
edit_file.close()
print('Saved file :',new_file_name)
print('Close file :',file_name)
