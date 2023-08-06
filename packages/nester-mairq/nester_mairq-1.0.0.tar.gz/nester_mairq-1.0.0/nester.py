def print_lol(the_list):
  for each_item in the_list:
    if isinstance(each_item, list):
      print_lol(each_item)
    else:
      print(each_item)
movies = ['gill', 1975, 'yueyue', 'boy', ['123', 'hahahha', ['wo qu', 'hello world!!']], ['bb aslkj', 1975], 1865]
print_lol(movies)
