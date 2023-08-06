from difflib import Differ


def diff_compare(in_lines1, in_lines2):
    l1 = in_lines1.split("\n")
    l2 = in_lines2.split("\n")
    d = Differ()
    result = list(d.compare(l1, l2))
    result = "\n".join(result)
    return result




