SIZE = 100

maze = []

for row in range(SIZE):

    current_row = []

    for col in range(SIZE):

        # Start
        if row == 0 and col == 0:
            current_row.append("S")

        # Goal
        elif row == SIZE - 1 and col == SIZE - 1:
            current_row.append("G")

        # Ensure path near goal stays open
        elif row == SIZE - 1 or col == SIZE - 1:
            current_row.append(str((row + col) % 9 + 1))

        # Create wall rows with openings
        elif row % 2 == 1:

            # Openings every 10 columns
            if col % 10 == 0:
                current_row.append(str((row + col) % 9 + 1))

            else:
                current_row.append("X")

        # Normal weighted cells
        else:
            current_row.append(str((row + col) % 9 + 1))

    maze.append("".join(current_row))

# Save maze into file
with open("maze_100x100.txt", "w") as file:

    for row in maze:
        file.write(row + "\n")

print("Maze generated successfully")