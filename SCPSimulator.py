import copy
import random

class Item:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __str__(self):
        return self.name+"/"+str(self.value)
    def __repr__(self):
        return self.name+"/"+str(self.value)

def SCP_Decision(input_stack, input_request, k): #Given an intial stack ordering, a cache size, and the current request, returns the cache state of SCP after that request.
    cache = copy.deepcopy(input_stack)
    request = copy.deepcopy(input_request)
    #copies the list given to not change the inputs

    hit = False
    newcache = []
    for i in cache:
        if (cache.index(i) < k):
            newcache.append(i)
            if (i.name==request.name):
                hit = True
    cache = newcache

    if (hit):
        return cache
    #Trims down the stack to the correct cache size. Also checks for a hit.

    lowest_priority = 100000000
    for i in cache:
        if (i.value < lowest_priority):
            lowest_priority = i.value
    #finds the lowest priority
    #if (k==2):
    #    print("Size "+str(k)+" cache containing "+str(cache)+" evicts " + str(i))

    for i in cache:
        if (i.value == lowest_priority):
            cache.remove(i)
            cache.append(request)
            return cache
    #Finds the value to be evicted, and returns the new cache. As of right now, breaks ties by choosing the item higher up in the stack ordering.
    print("Something has gone terribly wrong. Ruh Roh!")
    print(cache)
    print(lowest_priority)
    print(request)

def SCP_Find_Permutations(trace): #takes list of Items as input and returns dictionary of permutation/trace pairs.
    #distinct_items = []
    #distinct_items_count = 0
    #for i in trace:
    #    if not (i in distinct_items):
    #        distinct_items.append(i)
    #        distinct_items_count+=1
    #print(distinct_items)

    permutations = {} #dictionary with permutations as keys and the trace that generated it as values
    stack = [] #list of Items
    trace_copy = copy.deepcopy(trace)

    for i in trace:
        exists = False
        for j in stack:
            if (i.name == j.name):
                exists = True
                break
        #First, check if the item exists in the stack

        if (exists):
            new_stack = []

            new_stack.append(i) # k = 1 

            for k in range(2, len(stack)+1): #calculating the new stack
                added_count = 0 #for error checking - counts number of items added to new_stack per loop
                cache = SCP_Decision(stack, i, k)
                for cache_item in cache:
                    cache_item_is_new = True
                    for stack_item in new_stack:
                        if (cache_item.name == stack_item.name):
                            cache_item_is_new = False
                            break
                            #If this item's already in the stack, try the next cache item

                    if (cache_item_is_new):
                        new_stack.append(cache_item)
                        added_count += 1
                        break
                        #If it's new, add it and increase the counter.
                if (added_count != 1):
                    print("Error, " + str(added_count) + " items added to stack on iteration " + str(k) + ".")




            new_permutation = "("

            current_position = 0

            while True:

                old_item = stack[current_position]
                for new_item in new_stack:
                    if (old_item.name == new_item.name):
                        new_permutation += str(stack.index(old_item)+1)
                        current_position = new_stack.index(new_item)
                        
                        break
                        

                if (current_position == 0):
                    break
                

            new_permutation += ")"
            if (new_permutation == "(1)"):
                new_permutation = "id"
            permutations[new_permutation] = trace_copy
            #print("Permutation found: " + new_permutation)
            #Then, find the permutation and add it to the list

            stack = new_stack
            #update the stack





        else: 
            stack.append(i)
            #print("temp stack: " + str(stack))
            new_stack = []

            new_stack.append(i) # k = 1 

            for k in range(2, len(stack)+1): #calculating the new stack
                added_count = 0 #for error checking - counts number of items added to new_stack per loop
                cache = SCP_Decision(stack, i, k)
                for cache_item in cache:
                    cache_item_is_new = True
                    for stack_item in new_stack:
                        if (cache_item.name == stack_item.name):
                            cache_item_is_new = False
                            break
                            #If this item's already in the stack, try the next cache item

                    if (cache_item_is_new):
                        new_stack.append(cache_item)
                        added_count += 1
                        break
                        #If it's new, add it and increase the counter.
                if (added_count != 1):
                    print("Error, " + str(added_count) + " items added to stack on iteration " + str(k) + ".")




            
            stack = new_stack
            #update the stack

            
        for item in stack:
            if (item.name != i.name):
                item.value-=i.value
            #reduce priority of all items
            


        #temp_print = ""
        #for stack_item in stack:
        #    temp_print+= stack_item.name + "/" + str(stack_item.value) + ", "
        #print(temp_print)
        #for debugging purposes


    return permutations

def SCP_Generate_And_Run_Traces(trace_length, max_distinct_items, max_cost, number_iterations): #Generates random traces and returns found permutations.

    total_permutations = {}


    for i in range(1, number_iterations+1):
        distinct_items = []
        for j in range(65, max_distinct_items+65):
            distinct_items.append(Item(str(chr(j)), random.randint(1, max_cost)))
        #print("Distinct items: " + str(distinct_items))
        new_trace = []
        for item in range(0, trace_length):
            new_trace.append(copy.deepcopy(random.choice(distinct_items)))
        #print("Trace chosen: " + str(new_trace))
        found_permutations = SCP_Find_Permutations(new_trace)
        total_permutations.update(found_permutations)

    for i in total_permutations:
        print(i + " with trace " +  str(total_permutations.get(i)))

def SCP_steps(string_trace): #Expects a string of the format [A/1, B/3, C/1, etc.] and prints out step by step calculation
    trace_split = string_trace[1:-1].split(",")
    #print(string_trace)
    #print(trace_split)
    trace = []
    for item in trace_split:
        new_item = item.split("/")
        #print(new_item)
        new_item_name = new_item[0]
        new_item_name = new_item_name.strip()
        new_item_value = int(new_item[1])
        trace.append(Item(new_item_name, new_item_value))

    stack = [] #list of Items
    for i in trace:
        exists = False
        for j in stack:
            if (i.name == j.name):
                exists = True
                break
        #First, check if the item exists in the stack

        if (exists):
            new_stack = []

            new_stack.append(i) # k = 1 

            for k in range(2, len(stack)+1): #calculating the new stack
                added_count = 0 #for error checking - counts number of items added to new_stack per loop
                cache = SCP_Decision(stack, i, k)
                for cache_item in cache:
                    cache_item_is_new = True
                    for stack_item in new_stack:
                        if (cache_item.name == stack_item.name):
                            cache_item_is_new = False
                            break
                            #If this item's already in the stack, try the next cache item

                    if (cache_item_is_new):
                        new_stack.append(cache_item)
                        added_count += 1
                        break
                        #If it's new, add it and increase the counter.
                if (added_count != 1):
                    print("Error, " + str(added_count) + " items added to stack on iteration " + str(k) + ".")




            
            stack = new_stack
            #update the stack





        else: 
            stack.append(i)
            #print("temp stack: " + str(stack))
            new_stack = []

            new_stack.append(i) # k = 1 

            for k in range(2, len(stack)+1): #calculating the new stack
                added_count = 0 #for error checking - counts number of items added to new_stack per loop
                cache = SCP_Decision(stack, i, k)
                for cache_item in cache:
                    cache_item_is_new = True
                    for stack_item in new_stack:
                        if (cache_item.name == stack_item.name):
                            cache_item_is_new = False
                            break
                            #If this item's already in the stack, try the next cache item

                    if (cache_item_is_new):
                        new_stack.append(cache_item)
                        added_count += 1
                        break
                        #If it's new, add it and increase the counter.
                if (added_count != 1):
                    print("Error, " + str(added_count) + " items added to stack on iteration " + str(k) + ".")




            
            stack = new_stack
            #update the stack


            
        for item in stack:
            if (item.name != i.name):
                item.value-=i.value
            #reduce priority of all items
        print(stack)
            


        #temp_print = ""
        #for stack_item in stack:
        #    temp_print+= stack_item.name + "/" + str(stack_item.value) + ", "
        #print(temp_print)
        #for debugging purposes




#input = [Item("A", 5), Item("B", 2), Item("A", 5), Item("C", 3), Item("A", 5), Item("B", 2), Item("A", 5), Item("A", 5), Item("A", 5), Item("C", 3)]
#final_dict = SCP_Find_Permutations(input)
#for i in final_dict:
#    print(i + " with trace " +  str(final_dict.get(i)))

SCP_Generate_And_Run_Traces(10, 5, 20, 10000)

#SCP_steps("[A/16, B/6, B/6, E/1, A/16, D/4, C/9, E/1, B/6, A/16]")
#SCP_steps("[C/9, A/16, B/6, B/6, E/1, A/16, D/4, C/9]")