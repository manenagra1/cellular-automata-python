from matplotlib import pyplot as plt
#constants
LIVE_CELL_CHARACTER = "█"
DEAD_CELL_CHARACTER = " "
BORDER_CHARACTER = "▒"
NUM_STEPS = 100
FRAME_DELAY = 0.1

def convert_to_2D(input_filename: str)-> list:
    '''
    converts the input_filename into 2D list
    peremeters: 
        input_filename: takes the input file name as a string and converts it into a 2D list
    '''
    grid=[] 
    for lines in input_filename: 
        row=[]
        for character in lines.strip(): #converts the grid charaters into 1s and 0s. 1=live and 0=dead 
            if LIVE_CELL_CHARACTER==character:
                row.append(1)
            elif character==DEAD_CELL_CHARACTER or character==BORDER_CHARACTER:
                row.append(0)
        grid.append(row)
    return grid #returns a 2D list

def count_live_neighbors(grid: list, rows:int, colums:int)->int:
    '''
    counts the live neighbors around the cell.
    perameters:
        grid: A 2D list with values of 0s to represent dead cells, and 1s to represent live ones
        rows: The specific row index of the cell  
        colums: The specific colum index of the cell
    '''
    total_neighbor_live=0
    for direction_row in [-1,0,1]: # checking the neighbor cells that are next to the cell on each side
        for direction_colum in [-1,0,1]: 
            if direction_row==0 and direction_colum==0: # skips the cell itself 
                continue
            neighbor_row = rows + direction_row
            neighbor_colum= colums + direction_colum
            if 0 <= neighbor_colum < len(grid[rows]) and 0 <= neighbor_row < len(grid): #checks only the cells that are within the border
                total_neighbor_live += grid[neighbor_row][neighbor_colum] # if grid[neighbor_row][neighbor_colum]==1 than adds 1 to total_neighbor_live but if grid[neighbor_row][neighbor_colum]==0 than adds 0 to total_neighbor_live 
    return total_neighbor_live # return the total number of live cells around the specifice cell being checked

def steps(grid:list)->list:
    '''
    Stimulates the steps on the grid.
    perameter:
        grid: A 2D list with values of 0s to represent dead cells, and 1s to represent live ones
    '''
    new_grid=[]
    for rows in range(len(grid)):
        row=[]
        for colums in range(len(grid[rows])):
            live_neighbor=count_live_neighbors(grid, rows, colums) # counts the number of live neighbor cells around the cell
            if grid[rows][colums] == 1: # checks if the cells is alive and appends 1s or 0s if the cell has the right amount of neighbors
                if live_neighbor==3 or live_neighbor==2:
                    row.append(1)
                else:
                    row.append(0)
            elif grid[rows][colums] == 0: # checks if the cells is dead and appends 1s or 0s if the cell has the right amount of neighbors
                if live_neighbor==3:
                    row.append(1)
                else:
                    row.append(0)
        new_grid.append(row) # creates a new grid that repersents the new state of the cells being live or dead
    return new_grid 

def write_grid(output_file: str, new_grid:list)->list:
    '''
    writes out the new grid to the output file with borders.
    perameters: 
        output_file: file to write the ending configuration (after 100 steps) to
        new_grid: the new state of the cells being live or dead
    '''
    output_file.write(BORDER_CHARACTER * (len(new_grid[0]) + 2) + "\n") # writes the top border
    for row in new_grid: 
        output_file.write(BORDER_CHARACTER)# writes the left side border
        for cell in row: # writes out the cells that repersent a 1 as "█", and writes out the cells that repersent a 0 as " "
            if cell == 1:
                output_file.write(LIVE_CELL_CHARACTER)
            else:
                output_file.write(DEAD_CELL_CHARACTER)
        output_file.write(BORDER_CHARACTER+"\n")# writes the right side border along with a new line
    output_file.write(BORDER_CHARACTER * (len(new_grid[0]) + 2) + "\n") # writes the bottom border

def view_grid(grid: list, frame_delay: float, step_number: int) -> None:
    """
    shows an image of the current state of the grid
    parameters:
        grid - list-of-lists representing the current grid. Inner lists use 0s to represent dead cells, and 1s to represent live ones
        frame_delay - the program will pause for this many seconds after displaying the image. 0.1s gives a pretty good animation effect
        step_number - the step number of the supplied grid (will be displayed above the image)
    """

    # check that the grid supplied is not empty
    if len(grid) == 0:
        raise Exception("grid is empty")

    # check that all rows contain the same number of cells
    row_lengths = set([len(row) for row in grid])
    if len(row_lengths) != 1:
        raise Exception(f"not all grid rows are the same length. Found lengths: {row_lengths}")

    # check that all rows contain only 0s and 1s
    if not all([set(row) <= {0, 1} for row in grid]):
        raise Exception("only 0 and 1 are allowed in grid")

    # plot the grid
    plt.cla()
    plt.imshow(grid)
    plt.title(f'step {step_number}')
    plt.pause(frame_delay)


def main(input_filename: str, output_filename: str, display: bool) -> None:
    """
    main function
    parameters:
        input_filename: file to read the starting configuration from
        output_filename: file to write the ending configuration (after 100 steps) to
        display: if True, the program should display the grid steps (using the provided view_grid function)
                 if False, the program should not display the grid steps.
    """
    input_file=open("a4_code/data/input/"+input_filename, "r", encoding='UTF-8')
    grid=convert_to_2D(input_file) #coverts the input file into a 2D list
    output_file=open("a4_code/data/output/expected_output_"+output_filename, "w", encoding='UTF-8')
    for step in range(0,NUM_STEPS+1): #repeats for 100 steps 
        if display: # displays the grid 
            view_grid(grid, frame_delay=FRAME_DELAY, step_number=step)
        new_grid=steps(grid)
        if step == 100:  # Only writes the final grid with the borders at the last step
            write_grid(output_file, grid)
        grid=new_grid #updates the grid with the new grid
    output_file.close()
    input_file.close()


input_filename=input("Enter the input file name: ").lower()+".txt"
output_filename=input_filename
display=True
main(input_filename,output_filename,display)