#Generic .lsj File Unpacker for Elora ♡
#By Thren Stormclaw
#Version 0.3


import math
import json


LACONIC = True # Set this to false to get all the bools
               # and misc stuff in there too

def get_conf(path="ThrenUnpacker.conf"):
    print("CONF OPTIONS NOT YET IMPLEMENTED.")
    pass # Just going to keep this here for the moment as a reminder


####
#     UNDER CONSTRUCTION. WILL RE-IMPLEMENT LATER
####
'''
def LACONIC_prune(x):
    """If you're sure you don't want a specific var, use this to cut down on output filesize"""
    ### NEEDS UPDATED
    # (x should be a string)
    # If the string contains something in the prune list, prune it!
    prune_list = ["Color:\tbool","Custom:\tbool","Enabled:\tbool",
                  "Climable\tbool","ShootThroughType\tint8",
                  "ShootThrough\tbool", "WalkOn\tbool","WalkThrough\tbool",
                  ]
    for substring in prune_list:
        if substring in x:
            return True
    return False
'''
####


def input_file(input_path="input.txt"):
    try:
        with open(input_path) as f:
            print("File successfully loaded!")
            try:
                json_data = json.load(f)
            except:
                ("Oh no! It's a json decoding error! Are you sure the"
                "formatting is correct in there?")
            else:
                print("JSON data successfully decoded!")
    except FileNotFoundError:
        print("No file found. Please move the target file to the same"
              " folder as this script, rename the target"
              " file to \"input.txt\" and try again.")
        quit()
    except:
        print("Unknown Error with file loading. Sorry. 8(")
        quit()
    else:
        print("...")
        return json_data


def output_file(output_lines, output_path="bg3_unpacker_output.txt"):
    with open(output_path, "w") as f:
        for line in output_lines:
            print(line, file=f)
        print(f"OUTPUT TO FILE: {output_path}")


# Not sure how useful this one will be now, but eh, might as well
def replace_in_list(x, char_list, replace_list=None):
    """removes every character in charlst from every entry in x
       can optionally take replace_list to replace each value from before
       with something else. By default it will auto-format to a list full
       of blank strings ("")"""
    if (len(replace_list) != len(char_list)
        or replace_list == None):
        replace_list = ["" for i in char_list]
        
    for char in char_list:
        x = [i.replace(char, "") for i in x]
        
    return x



# This is the first very important boi here. Makes our stuff pretty
def recursive_parse(x, depth=0):
    """Parses through x, a dictionary, and parses through any dicts/lists
       it finds inside. Final output is a flat list of everything,
       containing the data and depth in the format: DEPTH||DATA."""
    output_list = []
    
    if isinstance(x, dict):
        for key, value in x.items():
            if isinstance(value, (dict, list)):
                output_list.append(f"{depth}||||[DICT]:"+str(key))
                output_list.extend(recursive_parse(x[key], depth+1))
            else:
                output_list.append(f"{depth}||||[VAR]:"+str(key)+" = "+str(value))
                
    elif isinstance(x, list):
        for item in x:
            if isinstance(item, (list, dict)):
                output_list.append(f"{depth}||||[LIST]")
                output_list.extend(recursive_parse(item, depth+1))
            else:
                # These two aren't necessarily errors on their own,
                # but they likely indicate the presence of one
                print("BARE LITERAL DETECTED IN LIST. (Formatting of file is suspect)")
                output_list.extend(f"[Depth:{depth}]Literal in list?? It\'s: {str(item)}")
                
    else:
        print("BARE LITERAL DETECTED LIST. (Formatting of file is suspect)")
        output_list.extend(f"[Depth:{depth}]Bare Literal?? It\'s: {str(item)}")
        
    return output_list


def max_depth_finder(parse_output):
    """Finds the maximum depth of a parser func output."""
    max_depth = -1 # Easier for us to find errors this way
    for i in parse_output:
        depth, string = i.split("||||")
        depth = int(depth)
        max_depth = max(depth, max_depth)
    return max_depth

def fvec3_to_hex(fvec3):
    """Turns a string/list of 3 decimals into a hex code"""
    if isinstance(fvec3, str):
        fvec3 = fvec3.split(" ")
    r, g, b = fvec3
    channels = [float(i) for i in [r, g, b]]  # Convert to float
    channels = [int(255*i) for i in channels] # to get to to 8-bit color
    r, g, b = channels
    vector_hex = 255*255*r + 255*g + b # then combine them...
    vector_hex = f"{vector_hex:X}" # And then a hex string!
    # Gotta make sure our hex codes are 6 digits!
    while len(vector_hex) < 6:
        vector_hex = "0"+vector_hex
    return vector_hex


def mat4x4_to_coords(mat4x4):
    """Turns 4x4 matrices into x/y/z coords + 3 angles of rotation data"""
    # This is what these transform matrices look like:
    #Row|Col: 0  1  2  3
    #   0   [[R1 R2 R3 X]
    #   1    [R4 R5 R6 Y]
    #   2    [R7 R8 R9 Z]
    #   3    [W1 W2 W3 1]]
    # (X,Y,Z)=Coords | R1-9=Rotation Data |
    #  W1/2/3 = ...trust me you don't wanna know
    # ALSO! Remember that lists in python start at index 0
    matrix = mat4x4.split("\r\n")
    matrix = [i for i in matrix if i != ""]
    # Removing Blank Element at end (and any others i forgot

    # matrix[row][column] (value, not column, but you get it)
    matrix = [row.split(" ") for row in matrix]
    matrix = [[i for i in row if i != ''] for row in matrix]
    matrix = [[float(i) for i in row] for row in matrix]
    # Removing Blank Element at end (but nested!)
    # And then making it all into floats (gotta do math on em!)

    # Cartesian Coords are easy. We can directly copy them
    pos_x = matrix[0][3]
    pos_y = matrix[1][3]
    pos_z = matrix[2][3]

    # Rotation is a stickier wicket
    # For those unfamiliar, these are the inverse funcs
    # for the trig functions sine and tangent.
    ang_1 = math.atan2(matrix[2][0], matrix[0][0]) # Heading
    ang_2 = math.atan2(matrix[1][2], matrix[1][1]) # Bank
    ang_3 = math.asin(matrix[1][0])                # Attitude

    # Converting to degrees (I suspect you don't like radians)
    ang_1, ang_2, ang_3 = [round(math.degrees(i), 5) for i in (ang_1, ang_2, ang_3)]

    return pos_x, pos_y, pos_z, ang_1, ang_2, ang_3

def mat3x3_to_coords(mat3x3):
    """Turns 3x3 matrices into 3 angles of rotation data.
       See mat4x4_to_coords for additional notes."""
    matrix = mat3x3.split("\r\n")
    matrix = [i for i in matrix if i != ""]

    matrix = [row.split(" ") for row in matrix]
    matrix = [[i for i in row if i != ''] for row in matrix]
    matrix = [[float(i) for i in row] for row in matrix]

    ang_1 = math.atan2(matrix[2][0], matrix[0][0]) # Heading
    ang_2 = math.atan2(matrix[1][2], matrix[1][1]) # Bank
    ang_3 = math.asin(matrix[1][0])                # Attitude

    # Converting to degrees (I suspect you don't like radians)
    ang_1, ang_2, ang_3 = [round(math.degrees(i), 3) for i in (ang_1, ang_2, ang_3)]

    return ang_1, ang_2, ang_3



def offset_list(parse_output, char="\t"): #Apply AFTER everything else!
    """Intended to be used on function output of recursive_parse, Makes the
       parse_output visually offset by the depth of each output. The "char"
       input defaults to tab, but will accept any character given to it."""
    offset_output = []
    char = str(char)
    for i in parse_output:
        depth, string = i.split("||||")
        depth = int(depth)
        offset_output.append(str(char*depth)+f"[{str(depth):>2}]"+string)
        
    return offset_output


def var_grouper(parse_output):
    """Intended to be used on the output of the recursive_parse function.
       Groups together literal values under the variable name they go
       with, compressing the output, improving readability, and setting
       up the stage for the object_grouper func"""
    stored_vars = None #Will be a dictionary we reset with every new variable
    new_output = []
    for line in parse_output:
        depth, string = line.split("||||")
        depth = int(depth)
        if "[DICT]" in string:
            if stored_vars is not None:
                new_output.append(process_vars(stored_vars))
            string = string.replace("[DICT]:","")
            stored_vars = {"name":string}
            stored_vars["depth"] = depth
        elif "[VAR]" in string:
            string = string.replace("[VAR]:","")
            pair = string.split(" = ")
            if pair[0] == "type":
                stored_vars["type"] = pair[1]
            elif pair[0] == "value":
                stored_vars["value"] = pair[1]
            else:
                stored_vars[pair[0]] = pair[1]        #For misc stuff
                                                      #(eg headers)
        elif "[LIST]" in string:
            if stored_vars is not None:
                new_output.append(process_vars(stored_vars))
                stored_vars = None
            new_output.append(str(depth)+"||||"+string)
            # For now let's just take this one out, maybe?
        else:
            print("I actually dunno how this happened!")
            new_output.append(str(depth)+"||||"+string)

    return new_output

            
def process_vars(stored_vars):
    """Part of var_grouper. Determines what to do to a variable based on the
       type we read it to be, etc (eg, vars with the name "Color" and vec3
       will be treated as colors, matrices will be converted, and so on)"""
    x = "" # Our output (a string)
    
    if "depth" in stored_vars.keys():
        x += str(stored_vars["depth"])+"||||"
    else:
        x += "-1||||[ERROR:DEPTH NOT FOUND]"
        
    if (("name" in stored_vars.keys())
        and len(stored_vars) > 2):
        x += "[VARIABLE]"+str(stored_vars["name"])
    elif "name" in stored_vars.keys():
        x += "[DICT]"+str(stored_vars["name"])
    else:
        x += "[NAME NOT FOUND]"
        
    if "type" not in stored_vars.keys(): #Just print whatever, I guess
        for k, v in stored_vars.items():
            if k not in ("name", "depth"):
                x += "["+str(k)+" = "+str(v)+"]"
    else: #Special cases that need some extra attention. 
        if stored_vars["type"] == "fvec3": # 3D vector (usually a color)
            x += "(fvec3 - usually a color)\t"
            x += fvec3_to_hex(stored_vars["value"])
        elif stored_vars["type"] == "mat4x4":    # Transform matrix (lvl geom)
            pos_x, pos_y, pos_z, ang_1, ang_2, ang_3 = \
                   mat4x4_to_coords(stored_vars["value"])
            x += "(mat4x4 - x/y/z & rotation data)"
            x += (f"[pos_x = {pos_x}][pos_y = {pos_y}][pos_z = {pos_z}]"
            +f"[ang_1 = {ang_1}][ang_2 = {ang_2}][ang_3 = {ang_3}]")
        elif stored_vars["type"] == "mat3x3":    # As above, but rotation
            ang_1, ang_2, ang_3 = mat3x3_to_coords(stored_vars["value"])
            x += "(mat3x3 - heading, bank, & attitude)"
            x += (f"[ang_1 = {ang_1}][ang_2 = {ang_2}][ang_3 = {ang_3}]")
        else:
            x += "("+str(stored_vars["type"])+")\t"
            if "value" in stored_vars.keys():
                x += str(stored_vars["value"])
                         
    return x


# NEXT UP:
# def object_grouper - We're gonna start collecting the low-level vars together under their headings.
# Eg. in the Gale file, near the top, BaseVisual has 6 variables underneath it, declaring the type and
# value. We want to group stuff like that, both to get it more compact, AND to eventually get it
# in columns for importing easy to a master spreadsheet




def object_grouper(parse_output, max_depth=None):
    """Intended to be used on the output of the recursive_parse function.
       Groups together literal vars under the object they're assigned to,
       allowing for formatting things in columns/tables easier"""
    if max_depth == None:
        max_depth = max_depth_finder(parse_output)
    for line in parse_output:
        pass

def celebratory_bnnuy():
    print("♡  /)__/)")
    print("  („•֊•„)♡")
    print("|￣U U￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣|")
    print("|  Hooray! The output is done!  |")



if __name__ == "__main__": # Let's Gooooooooo!
    json_test = input_file()
    output_list = recursive_parse(json_test)

    vargroup_list = var_grouper(output_list)

    #formatted_list = vargroup_list
    formatted_list = offset_list(vargroup_list)
    output_file(formatted_list)
    celebratory_bnnuy()




