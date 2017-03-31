matrix_a = [[1,2,3],[4,5,6],[7,8,9]]
matrix_b = [[1,2,3],[4,5,6],[7,8,9]]

def calculate_cell(row,column):
  cell = 0
  for y in range(len(matrix_a[0])):
    cell += matrix_a[row][y] * matrix_b[y][column]
  return cell

for row in range(len(matrix_a)):  
  for column in range(len(matrix_a[0])):
    cell = calculate_cell(row,column)
    print "[",cell,"]",
  print ""
    
