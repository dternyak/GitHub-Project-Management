import os


def create_or_get_directory(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return os.path.abspath(directory)


def write_to_file(file_path, contents):
    with open(file_path, 'w') as the_file:
        the_file.write(contents)


def buffer_list_of_dicts(output, list_of_dicts):
    for i, each in enumerate(list_of_dicts):
        if i != 0: output.write('\n')
        for key, value in each.items():
            if '\n' in value:
                value = value.split('\n')[0]
            output.write('{}: {}\n'.format(key, value))


def handle_file_creation(output_file, relative_dir='output'):
    output_directory = create_or_get_directory(relative_dir)
    full_output_file_path = os.path.join(output_directory, output_file)
    return full_output_file_path
