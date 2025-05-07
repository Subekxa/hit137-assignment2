import turtle

#Recursive function to draw the tree branches
def draw_branch(t, branch_length, left_angle, right_angle, depth, reduction_factor):
    if depth > 0:
        # Draw the current branch
        t.forward(branch_length)
        t.pencolor("brown")
        # Draw the left branch
        t.left(left_angle)
        t.pencolor("green")
        draw_branch(t, branch_length * reduction_factor, left_angle, right_angle, depth - 1, reduction_factor)
        # Return to the main branch
        t.right(left_angle + right_angle)
        # Draw the right branch
        draw_branch(t, branch_length * reduction_factor, left_angle, right_angle, depth - 1, reduction_factor)
        # Return to the main branch
        t.left(right_angle)
        t.backward(branch_length)
    
    
#main function to get user input and initiate drawing
def main():
    # Get parameters from the user
    left_angle = int(input("Enter left branch angle: "))
    right_angle = int(input("Enter right branch angle: "))
    starting_branch_length = int(input("Enter starting branch length: "))
    depth = int(input("Enter recursion depth: "))
    reduction_factor = float(input("Enter branch length reduction factor: "))

    # Set up turtle screen and turtle object
    t = turtle.Turtle()
    screen = turtle.Screen()
    screen.bgcolor("white")
    t.speed("fast")

    # Move turtle to the starting position
    t.left(90)
    t.up()
    t.backward(100)
    t.down()

    # Drawing the tree using recursive function
    draw_branch(t, starting_branch_length, left_angle, right_angle, depth, reduction_factor)

    t.color("brown")
    t.forward(100)

    # Hide the turtle and display the result
    t.hideturtle()
    turtle.done()

if __name__ == "__main__":
    main()