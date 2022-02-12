import os
import stat


def has_written():
    current_path = os.getcwd()
    written = os.path.exists(os.path.join(current_path, '.written'))
    return written


def write_variable(current_path):
    if not has_written():
        content = f"Current_Path=\"{current_path}\"\n"
        with open('search.sh', 'r+') as f:
            lines = f.readlines()
            index = 0

            for line in lines:
                if '__init__' in line:
                    break
                index += 1
            index += 1

            lines.insert(index, content)

            f.seek(0, 0)
            f.writelines(lines)


def write_path(current_path):
    if not has_written():
        # First write the $Current_Path variable to the "search.sh" file
        os.chdir(current_path)
        write_variable(current_path)

        # Write to .bash_profile
        bash_content = f"alias search=\'{os.path.join(current_path, 'search.sh')}\'\n"
        os.chdir(os.path.expanduser("~"))
        if os.path.exists('.bash_profile'):
            mode = 'a'
        else:
            mode = 'w'

        with open('.bash_profile', mode) as f:
            f.write(bash_content)

        # Create a token at directory position
        with open(f"{os.path.join(current_path, '.written')}", 'w') as f:
            f.write("WRITTEN")


def main():
    curr_path = os.getcwd()
    file_path = os.path.join(curr_path, "search.sh")
    token_path = os.path.join(curr_path, ".written")

    write_path(curr_path)
    os.chmod(file_path, stat.S_IRWXU)
    os.chmod(token_path, stat.S_IREAD)


if __name__ == '__main__':
    main()