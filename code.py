

def display(mission, pc_category, force_dictionary):
    mission_frame_center = "| Mission {} |".format(mission)
    print(len(mission_frame_center)*"-")
    print(mission_frame_center)
    print(len(mission_frame_center)*"-")
    print()
    print("{} {}".format("Potential contact category:", pc_category))
    print()
    for key, details in force_dictionary.items():
        print("{}: {}".format(key, details))
    print()
        
def mission_decision():
    while True:
        global mission
        mission = input('\nEnter number of mission (1-7) or [q] to exit program: ')
        if mission.lower() == 'q':
            break
        try:
            mission = int(mission)
            if mission < 1 or mission > 7:
                raise ValueError
            break
        except ValueError:
            print("\nInvalid input, You must enter integer between 1 and 7 or [q] to exit")
            
def farewell_message():
    print(22*"-")
    print("|{:^20s}|".format("See you later!"))
    print(22*"-")
    
def pc_category_decision(mission):
    while True:
        try:
            global pc_category
            pc_category = input("Mission number is {}. Enter potential contact category A, B, C, CA (counterattack) or [q] to choose another mission".format(mission)).upper()
            if pc_category.upper() not in ("A", "B", "C", "CA", "Q"):
                raise ValueError
            break
        except ValueError:
            print("\nInvalid input, You must enter potential contact category (A, B, C or CA) or 'q'")

def force_list_creator(mission, pc_category):
    force_list = []
    with open("norm_forces.txt", "r") as norm_forces:
        for force in norm_forces:
            force = force.split(", ")
            force_selectors = force[5].split(" ")
            for selector in force_selectors:
                if ("{:d}{:s}".format(mission, pc_category)) == selector[0:2] or (pc_category  == "CA" and selector[0:2] == "CA"):
                    force_list.append(force)
                    if "d" in selector:
                        force_list.append(force)
                    elif "t" in selector:
                        force_list.append(force)
                        force_list.append(force)
                    elif "q" in selector:
                        force_list.append(force)
                        force_list.append(force)
                        force_list.append(force)
    return force_list
    
def same_card_decision():
    while True:
        try:
            global same_card_decl
            same_card_decl = input("Is placement only possible on the same card? y/n ")
            if same_card_decl.lower() != "y" and same_card_decl.lower() != "n":
                raise ValueError
            break
        except ValueError:
            print("Invalid input, enter [y]es or [n]o")
            
def same_card_list_creator(force_list):
    new_list = []
    for index in range(len(force_list)):
        if force_list[index][1] == "Same card":
            new_list.append(force_list[index])
    if new_list == []:
        print("Same card forces are not available for this potential contact category")
    return new_list

def random_force(force_list):
    import random
    force = random.choice(force_list)
    force_info_breakdown(force)
    return force
    
def force_info_breakdown(force):
    global force_name
    force_name = force[0]
    global per_package_distance
    per_package_distance = force[1]
    global units
    units = force[2]
    global spotted
    spotted = force[3]
    global vof_generated
    vof_generated = force[4]
    
def force_selector(force_list):
    force = random_force(force_list)
    while True:
        units_available = input("Are following unit/s available: {}".format(units))
        try:
            if units_available.lower() == "y":
                return force
            elif units_available.lower() == "n":
                force_list.remove(force)
                if force_list == []:
                    return "Empty"
                force = random_force(force_list)
            else:
                raise ValueError
        except ValueError:
            print("\nInvalid input, You must enter [y]es or [n]o")

def placement_list_creator(pp=2, f=4, l=2, r=2):
    packed_placements = [pp*["Per package"], f*["Front at max LOS"], l*["Left front at max LOS"], r*["Right front at max LOS"]]
    placement_list = sum(packed_placements, [])
    return placement_list
                                  
def random_placement(placement_list):
    import random
    placement = random.choice(placement_list)
    return placement

def placement_remover(placement, placement_list):
    new_placement_list = []
    for index in range(len(placement_list)):
        if placement_list[index] != placement:
            new_placement_list.append(placement_list[index])
    return new_placement_list

def placement_decision(placement, same_card_decl):
    while True:
        if same_card_decl == "y":
            return "y"    
        placement_decision = input('Is "{}" direction available?'.format(placement))
        try:
            if placement_decision != "y" and placement_decision != "n":
                raise ValueError
            else:
                return placement_decision
        except ValueError:
            print("\nInvalid input. You must enter [y]es or [n]o")

def placement_selector(force, same_card_decl, per_package_distance, placement_list):
    if same_card_decl == "y" or force_name == "Mines!":         # mines are always placed on the same card as triggering unit
        placement = per_package_distance
        return placement, placement_list
    else:
        placement = random_placement(placement_list)
        print(placement, "was chosen")
        if "max LOS" in placement:
            if "Adjacent" not in per_package_distance:        # if "Adjacent" is possible for this force, it can still be used
                placement_list = placement_remover(placement, placement_list)
            return placement, placement_list
        elif "Per package" in placement:
            distance = per_package_distance
            placement = random_placement(placement_list)
            if "Same card" in distance:
                placement_list = placement_remover(placement, placement_list)
                return distance, placement_list
            elif "Adjacent" in distance:
                while True:
                    placement = random_placement(placement_list)
                    if placement != "Per package":
                        placement_list = placement_remover(placement, placement_list)
                        placement = placement.split(" at ")
                        direction = placement[0]
                        placement = "{} {}".format(distance, direction.lower())
                        return placement, placement_list
            else:
                while True:
                    placement = random_placement(placement_list)
                    if placement != "Per package":
                        placement_list = placement_remover(placement, placement_list)
                        return placement, placement_list
            

def force_details_compiler(force_name, placement, units, spotted, vof_generated):
    global force_dictionary
    spotted = spotted.strip("S: ")
    vof_generated = vof_generated.strip("V: ")
    units = mission_cover_determination(units)
    force_dictionary = {"Force name":force_name, "Unit/s":units, "Placement":placement, "Spotted":spotted, "VoF generated":vof_generated}

def mission_cover_determination(units):
    if "Mission Cover" in units:
        if mission == 1:
            units = units.replace("Mission Cover", "Trenches")
        else:
            units = units.replace("Mission Cover", "Foxholes")
    return units


# In[21]:


def main():
    
    while True:
        
        # user selects mission or chooses to exit program
        
        mission_decision()
        if str(mission) in'Qq':
            farewell_message()
            break   
        
        while True:
            
            # user selects potential contact category or exits to mission selection
        
            pc_category_decision(mission)
            if pc_category.lower() == "q":
                break
            
            # program creates potential forces list

            force_list = force_list_creator(mission, pc_category)

            # user declares if placement is only possible on the same card as triggering unit, 
            # if yes - program creates new list with suitable forces
                
            same_card_decision()
            
            if same_card_decl == "y":
                force_list = same_card_list_creator(force_list) 
                if force_list == []:
                    print("\nThere are no forces available in this potential contact category")
                    break
                
            while True:
                
                # program randomly chooses force and user tells if it's available

                force = force_selector(force_list)
                if force == "Empty":
                    print("\nThere are no more forces available in this potential contact category")
                    break

                placement_list = placement_list_creator(pp=2, f=4, l=2, r=2)

                while True:

                    try:

                        while True:

                            if len(placement_list) <= 2:            # if length of list is 2, only "Per package" result is left
                                raise IndexError                    # all other options were exhausted

                            # program randomly chooses placement of appearing force and user tells if it's valid

                            (placement, placement_list) = placement_selector(force, same_card_decl, per_package_distance, placement_list)
                            placement_accept = placement_decision(placement, same_card_decl)
                            if placement_accept == "y":
                                placement_list = placement_remover(placement, placement_list)
                                break
                            elif placement_accept == "n":
                                continue

                        # "/" indicates that units must be placed on different cards, so second direction is needed

                        if "/" in units:
                            
                            while True:
                            
                                if len(placement_list) <= 2:
                                    raise IndexError            
                                
                                (placement2, placement_list) = placement_selector(force, same_card_decl, per_package_distance, placement_list)
                                placement_accept = placement_decision(placement2, same_card_decl)
                                if placement_accept == "y":
                                    placement = "{}, {}".format(placement, placement2)
                                    break
                                elif placement_accept == "n":
                                    continue

                    except IndexError:
                        print("No more directions available")
                        break
                    except TypeError:
                        print("No more directions available")
                        break

                    force_details_compiler(force_name, placement, units, spotted, vof_generated)
                    display(mission, pc_category, force_dictionary)

                    break
                        
                break
                
if __name__ == "__main__":
    main()