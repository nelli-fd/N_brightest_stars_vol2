import time

var1 = 'ra_ep2000'
var2 = 'dec_ep2000'
var3 = 'source_id'
var4 = 'phot_g_mean_mag'
var5 = 'distance'
separator = '\t'
new_line = '\n'
sort_by_index = 4
output_file = str(time.time()) + '.csv'


def generate_output_file(list_of_N_stars):
    """ Open the file for writing the data of N stars to the output file contained in the field of view.

    :param list_of_N_stars: List of data to be written in the file
    :type list_of_N_stars: list
    """
    with open(output_file, 'a') as fw:
        fw.write(var3 + separator + var1 + separator + var2 + separator +
                 var4 + separator + var5 + new_line)
        for i in range(len(list_of_N_stars)):
            for j in range(len(list_of_N_stars[i])):
                if j < len(list_of_N_stars[i]) - 1:
                    fw.write(str(list_of_N_stars[i][j]) + separator)
                else:
                    fw.write(str(list_of_N_stars[i][j]) + new_line)


def sort_by_distance(list_of_stars_inside_the_fov: list):
    """ Function to sort the list by distance of the stars from a given point.

    :param list_of_stars_inside_the_fov: Stars contained inside the field of view
    :type list_of_stars_inside_the_fov: list
    """
    if len(list_of_stars_inside_the_fov) > 1:
        mid = len(list_of_stars_inside_the_fov) // 2
        left_half = list_of_stars_inside_the_fov[:mid]
        right_half = list_of_stars_inside_the_fov[mid:]

        sort_by_distance(left_half)
        sort_by_distance(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i][sort_by_index] < right_half[j][sort_by_index]:
                list_of_stars_inside_the_fov[k] = left_half[i]
                i += 1
            else:
                list_of_stars_inside_the_fov[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            list_of_stars_inside_the_fov[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            list_of_stars_inside_the_fov[k] = right_half[j]
            j += 1
            k += 1


def find_N_brightest_stars(file_of_data: str,
                           ra_coordinate: float,
                           dec_coordinate: float,
                           fov_horizontal_length: float,
                           fov_vertical_length: float,
                           number_of_brightest_stars: int
                           ):
    """ Function to find the brightest N stars, sort it by their distance from a given point and write their data
    into the output file.

    :param file_of_data: File to read the data
    :type file_of_data: str
    :param ra_coordinate: First coordinate of the given point
    :type ra_coordinate: float
    :param dec_coordinate: Second coordinate of the given point
    :type dec_coordinate: float
    :param fov_horizontal_length: Horizontal field of view length
    :type fov_horizontal_length: float
    :param fov_vertical_length: Vertical field of view length
    :type fov_vertical_length: float
    :param number_of_brightest_stars: Number of stars that should be extracted
    :type number_of_brightest_stars: int
    """

    left_boundary_h = ra_coordinate - fov_horizontal_length / 2
    right_boundary_h = ra_coordinate + fov_horizontal_length / 2
    bottom_boundary_v = dec_coordinate - fov_vertical_length / 2
    top_boundary_v = dec_coordinate + fov_vertical_length / 2
    temp_dict = {}
    list_of_stars_in_the_fov = []
    count = 0

    with open(file_of_data, 'r') as fr:
        for line in fr.readlines()[1:]:
            """ Open the file and start reading, check whether the star is in the field of view and if yes, 
            calculate the star's distance from the center of the field of view (given point) and add first 
            N (number_of_brightest_stars) stars to the list (list_of_stars_in_the_fov) in ascending order
            by their magnitude. """
            count += 1
            if count == 1:
                first_line = line.split()
                continue
            line = [line.split(separator) for _ in line.splitlines()][0]
            for i in range(len(first_line)):
                temp_dict[first_line[i]] = line[i]
            if left_boundary_h < float(temp_dict[var1]) < right_boundary_h \
                    and bottom_boundary_v < float(temp_dict[var2]) < top_boundary_v:
                distance = ((float(temp_dict[var1]) - ra_coordinate) ** 2
                            + (float(temp_dict[var2]) - dec_coordinate) ** 2) ** 0.5
                temp_list = list([temp_dict[var3],
                                  float(temp_dict[var1]),
                                  float(temp_dict[var2]),
                                  float(temp_dict[var4]),
                                  distance])
                if len(list_of_stars_in_the_fov) == 0:
                    list_of_stars_in_the_fov.append(temp_list)
                    continue
                for index in range(len(list_of_stars_in_the_fov)):
                    if temp_list[3] < list_of_stars_in_the_fov[index][3]:
                        list_of_stars_in_the_fov.insert(index, temp_list)
                        if len(list_of_stars_in_the_fov) > number_of_brightest_stars:
                            list_of_stars_in_the_fov.pop()
                        break
        sort_by_distance(list_of_stars_in_the_fov)
        generate_output_file(list_of_stars_in_the_fov)


def check_float(potential_float: str):
    """ Function to check the validity of string and throw an exception if its invalid. """
    try:
        float(potential_float)
        return True
    except ValueError:
        return False


def check_int(potential_int: str):
    """ Function to check the validity of string and throw an exception if its invalid. """
    try:
        int(potential_int)
        return True
    except ValueError:
        return False


def main():
    """ Driver code. """
    file = 'cleaned_stars.tsv'
    ra = input('Input ra: ')
    while not check_float(ra):
        print('ValueError!')
        ra = input('Input ra: ')
    dec = input('Input dec: ')
    while not check_float(dec):
        print('ValueError!')
        dec = input('Input dec: ')
    fov_h = input('Input horizontal field of view: ')
    while not check_float(fov_h):
        print('ValueError!')
        fov_h = input('Input fov_h: ')
    fov_v = input('Input vertical field of view: ')
    while not check_float(fov_v):
        print('ValueError!')
        fov_v = input('Input fov_v: ')
    number_of_stars = input('Input number of stars: ')
    while not check_int(number_of_stars):
        print('ValueError!')
        number_of_stars = input('Input number_of_stars: ')
    find_N_brightest_stars(file, float(ra), float(dec), float(fov_h), float(fov_v), int(number_of_stars))
    print()


if __name__ == '__main__':
    main()
