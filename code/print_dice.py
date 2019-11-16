from random import randrange


def get_dice_rolls(number_of_rolls):
    """Returns list with number_of_rolls from a 6-sided dice."""

    return [randrange(1, 6+1) for _ in range(number_of_rolls)]


def get_single_dice_face(dice_roll, zero_based=False, eye='o '):
    """Return the full face of the roll for a dice-6 sided dice."""

    # Shorten roll variable, and account for zero_basing rolls
    r = dice_roll if zero_based else dice_roll - 1
    dice_str = '+-----+\n| {0} {1} |\n| {2}'.format(eye[r<1], eye[r<3], eye[r<5])
    # Return mirrored dice string with changing middle to get a full face
    return dice_str + eye[r&1] + dice_str[::-1]


def print_dice_rolls(dice_rolls, zero_based=False,  max_width=72, eye='o '):
    """Pretty print all dice_rolls using 6-sided dice(s)."""

    # Verify parameters

    if any(roll > 6 for roll in dice_rolls):
        raise ValueError('Roll is higher than 6')

    if len(eye) != 2:
        raise ValueError('Excpected two choice for eye parameter')

    # Set up some default values
    dice_width = 5
    dice_lines = 5

    # Will try to collate output of multiple dice rolls into lines
    # of up to max_width length
    output_buffer = [''] * dice_lines

    # Output the dice rolls using output_buffer
    for roll in dice_rolls:

        # Build a proper dice_str according to 6 and roll
        current_dice = get_single_dice_face(roll, zero_based, eye)

        # Check width of output_buffer against max_width,
        # and if next line go over, then print and reset buffer
        if len(output_buffer[0]) + dice_width >= 72:
            for idx, line in enumerate(output_buffer):
                print(line)
                output_buffer[idx] = ''

        # Append dice to output_buffer
        for idx, line in enumerate(current_dice.split('\n')):
            output_buffer[idx] += line + '  '


    # Print remaining dices in output_buffer
    if len(output_buffer[0]) > 0:
        for line in output_buffer:
            print(line)
