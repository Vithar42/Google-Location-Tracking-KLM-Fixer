# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 10:06:31 2014

@author: Nick
"""
#import needed libararys
from tkinter.filedialog import askopenfilename


'''Step 1, import file to convert, must be in the same directory as this script'''


#file_name = "history-11-17-2014.txt"
#file_name = "history-12-31-2000.kml"
#file_name = "C:/Users/Nick/Downloads/KML Formating/history-11-17-2014.txt"
#file_name = askopenfilename()

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

'''
print("")  
print('--- Step 2 Results ---')
print('Start and End Indexies = ',find_Start_end(data))
print("")
print('check cord_date from index 0 to 3 = ',cord_data[0:3])
print("")
'''

'''Step 3, wrangle the data, remove the <when> list items and correct the cordinate data format.'''

#Function to fix the formating of the x,y,z cordinates
def fix_cordinates(item):
    new_item = item.replace('<gx:coord>',"")
    new_item = new_item.replace('</gx:coord>',"")
    new_item = new_item.replace(' ',",")
    new_item = new_item.replace('\n'," ")
    return new_item

#Function to delte list items containing <when>    
def kill_when(page):
    #indices = [i for i, s in enumerate(page) if 'when' not in s]
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

'''
print('--- Step 3 Results ---')
print('test if fix_cordinates works at cord_data[1] = ',fix_cordinates(cord_data[1]))
print("")
print('only_cord_data = ',only_cord_data)
print("")
print('fixed_cord_data = ',cord_data)
'''

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

def set_header(page):
    end_index = [i for i,x in enumerate(header_data) if x == '\t<Placemark>\n']
    end_index = end_index[0]
    return page[:end_index]
    
def set_item_start_tags(page):
    start_index = [i for i,x in enumerate(header_data) if x == '\t<Placemark>\n']
    start_index = start_index[0]
    end_index = [i for i,x in enumerate(header_data) if x == '\t\t\t<coordinates>\t\t\t\n']
    end_index = end_index[0]+1
    return page[start_index:end_index]
    
def set_item_end_tags(page):
    start_index = [i for i,x in enumerate(header_data) if x == '\t\t\t</coordinates>\n']
    start_index = start_index[0]
    end_index = [i for i,x in enumerate(header_data) if x == '\t</Placemark>\n']
    end_index = end_index[0]+1
    return page[start_index:end_index]

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


#Fucntion to Build the final list, start with the header,
header = set_header(header_data)
start_tags = set_item_start_tags(header_data)
end_tags = set_item_end_tags(header_data)
footer = set_footer(header_data)
cord_list_strings = list_to_strings(cord_list)
myfile.close()
print('Close file :',file_name_header)

'''
print('--- Step 4 Results ---')
#print('test list of list = ',cord_list[1])
print("check the number of lists in the list of lists")
print("cord_list has %d items" %len(cord_list))
print('--- Header ---')
print(header)
print('--- start tags ---')
print(start_tags)
print('--- end tags ---')
print(end_tags)
print('--- Footer ---')
print(footer)
'''

#Function to write the list of strings to our new file...
def build_cord_core(file,page):
    page
    i=0    
    while i < len(page):
        for e in start_tags:
            if e == '\t\t<name>Untitled Path</name>\n':
                d=i+1
                e = e.replace('Untitled Path',"Set %d" %d)              
                file.write(e)
            else:
                file.write(e)         
        file.write('\t\t\t\t' + page[i] + '\n')        
        for e in end_tags:
            file.write(e) 
        i = i+1
    return file

'''Step 5, output everything to a new txt file'''
#Genearte name from original file


new_file_name = file_name

if new_file_name.find('.txt') != -1:
    new_file_name = new_file_name.replace('.txt',".kml")
new_file_name = new_file_name.replace('.kml',"-corrected.kml")
print('created new file named :',new_file_name)

edit_file = open(new_file_name, 'w')
for e in header:
    edit_file.write(e)
build_cord_core(edit_file,cord_list_strings)
for e in footer:
    edit_file.write(e) 
edit_file.close()
print('Saved file :',new_file_name)
print('Close file :',file_name)


def quit():
    global root
    root.destroy()
    
quit()