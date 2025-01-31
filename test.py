import subprocess


def is_file_open(file_path):
    try:
        # Run lsof and check output
        output = subprocess.check_output(["lsof", file_path], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        # lsof exits with 1 if the file is not open
        return False


# Example usage
# file_path = "/home/prosper/Desktop/workspace/Academics/smartstudy/store/materials/MAT111/10 Usability Heuristics for User Interface Design_1622399977365.pdf"
file_path = "./store/materials/MAT111/10 Usability Heuristics for User Interface Design_1622399977365.pdf"
if is_file_open(file_path):
    print(f"{file_path} is open.")
else:
    print(f"{file_path} is not open.")
