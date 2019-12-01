from random import randrange
red = '\x1b[31;6m'
bold = '\x1b[;1m'
blue = '\x1b[34;6m'
green = '\x1b[32;6m'
def get_single_dice_face(dice_roll, eye='o '):
    """Permet de dessiner une face d'un dés"""
    print(red)
    r = dice_roll - 1
    dice_str = '+-----+\n| {0} {1} |\n| {2}'.format(eye[r<1], eye[r<3], eye[r<5])
    return dice_str + eye[r&1] + dice_str[::-1]


def print_dice_rolls(dice_rolls):
    """Affiche les 6 faces d'un dés"""
    if any(roll > 6 for roll in dice_rolls):
        raise ValueError('Roll is higher than 6')
    output_buffer = [''] * 5

    for roll in dice_rolls:

        current_dice = get_single_dice_face(roll)

        if len(output_buffer[0]) + 5 >= 72:
            for idx, line in enumerate(output_buffer):
                print(line)
                output_buffer[idx] = ''

        for idx, line in enumerate(current_dice.split('\n')):
            output_buffer[idx] += line + '  '

    if len(output_buffer[0]) > 0:
        for line in output_buffer:
            print(line)
