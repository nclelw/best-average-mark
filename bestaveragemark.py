# File: bestaveragemark.py
# A program to calculate the student with the highest average mark across a set of units.

def open_file(filename):
    '''
    Opens the file and returns it on success
    
    Returns none on failure
    '''
    try :
        return open(filename)
    except FileNotFoundError:
        # while it's possible to use os.path.is_file() to 
        # determine if the file exists, the pythonic way is to
        # just go head and try it. 
        # python EAFP
        # https://docs.python.org/3.4/glossary.html
        return None
    
def get_units(unitfile):
    '''
    Reads the contents of the unit file 
    returns a nested list
    '''
    units = []
    for line in unitfile:
        parts = line.strip().split(',')
        if len(parts) == 2:
            # The split by comma should give us a list of two items.
            # Convert the second item in that list to a float and 
            # append the list to the parent list (units)
            units.append( (parts[0], float(parts[1])) )
            
    return units

def get_student_records(students_file, units):
    '''
    Reads the students file
    
    The records are checked against the units and normalised. That is
    each score is converted into a value between 0 and 1 based on the marks
    scored and the maximum number of marks available for that subject.
    '''

    records = []
    for line in students_file:
        parts = line.strip().split(',')
        if len(parts) == len(units) + 1:
            # having split the line by a comma we should have the same number
            # of items in list as the length of the units list + 1.
            #
            # then go through all the scores in the list and convert each
            # one of them to a percentile
            #
            for i in range(1, len(parts)):
                if parts[i]:
                    score = float(parts[i]) / units[i -1][1]
                    parts[i] = score
                
            # finally it's appended to the return value which is another list.
            # this is a nested list, which the outer list consisting of a 
            # collection of records each record happens to begin with the
            # student name and then has the percentiles in the res of the fields
            #
            records.append(parts)
            
            
    return records

def compute_mean_pc(students_pclist):
    '''
    Calculates the mean percentiles for each student
    '''
    
    pc = []
    
    for record in students_pclist:
        # this problem can be solved very easily in two lines with a list 
        # comprehension.  Here is a longer more tedious way. 
        count = 0
        total = 0
        for i in range(1, len(record)):
            if record[i]:
                count += 1
                total += record[i]
                
        if count:
            pc.append( (total/count, record[0]))
            
        else:
            # if count is zero, we are going to have a divide by zero error which 
            # will cause the program to halt. So to avoid that with the condition nd
            # use the value of infinity for the records where the student has not
            # taken part in any exams.
            pc.append( (float("inf"), record[0] ) )
            
            
    return pc

def print_final_list(mean_pclist):
    '''
    print the percentiles with the owners
    '''
    
    mean_pclist.sort(reverse=True)
    for record in mean_pclist:
        print("{0}: {1:.3f}".format(record[1], record[0]))
        
        
        
def main():
    '''
    The main method
    '''
    
    units_file_name = input("Please enter the name of the units file : ")
    units_file = open_file(units_file_name)
    if not units_file:
        print("Could not open the units file {0} for reading ".format(units_file_name))
    else:
        records_file_name = input("Please enter the name of the student records file : ")
        records_file = open_file(records_file_name)
        
        if records_file:
            units = get_units(units_file)
            records = get_student_records(records_file, units)
            means = compute_mean_pc(records)
            print_final_list(means)
        else:
            print("Could not open the students records file {0} for reading ".format(records_file_name))
            

        units_file.close()
        
if __name__ == '__main__':
    main()
    

