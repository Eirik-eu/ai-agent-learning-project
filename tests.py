from functions.get_file_content import get_file_content


def test():
    print("Main.py: \n")
    print(get_file_content("calculator", "main.py"))

    print("pkg/calculator.py\n")
    print(get_file_content("calculator", "pkg/calculator.py"))

    print("/bin attempt. Should give an error.\n")
    print(get_file_content("calculator", "/bin/cat"))

    print("Non existant file\n")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))


if __name__ == "__main__":
    test()