import sys
import csv

    
def main():
    
    # check for command-line arguements
    if len(sys.argv) != 3:
        sys.exit("missing command-line argument")
    
    data = sys.argv[1]
    STR_comp = sys.argv[2]
    
    # open input files
    with open(data, "r") as f:
        reader = csv.DictReader(f)
        csv_list = list(reader)
        
    with open(STR_comp, "r") as f:
        sequence = f.read()
        
    max_repeat = []
    
    # loop through each type of STR
    for header in range(1, len(reader.fieldnames)):
        STR = reader.fieldnames[header]
        max_repeat.append(0)
        
        # loop through each position of the sequence
        for i in range(len(sequence)):
            repeat = 0 
            while sequence[(i + (len(STR) * repeat)):(i + (len(STR) * (repeat + 1)))] == STR:
                repeat += 1
            
            if repeat > max_repeat[header - 1]:
                max_repeat[header - 1] = repeat
    
    # compare against database
    for person in range(len(csv_list)):
        match = 0
        
        for count in range(1, len(reader.fieldnames)):
            
            if int(max_repeat[count - 1]) == int(csv_list[person][reader.fieldnames[count]]):
                match += 1
                
            if match == len(reader.fieldnames) - 1:
                print(csv_list[person]["name"])
                sys.exit(0)
    
    print("No Match")            
        
        
main()                