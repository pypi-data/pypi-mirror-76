def test_list(the_list,switch=False,level=0):
    for each_list in the_list:
        if isinstance(each_list,list):
            test_list(each_list,switch,level+1)
        else:
            if switch:
                for num in range(level):
                    print("\t",end="")
            print(each_list)
