import re


class PrePro():

    @staticmethod
    def filter(source):
        comments = re.sub(r"(?<!\d|-)--.*$", "", source, flags=re.MULTILINE)
        return comments


if __name__ == "__main__":
    print(PrePro.filter("1 + 1 -- 1 + 1 greer"))  # "1 + 1"
    print(PrePro.filter("1 - 1 - 1 + 1"))
    print(PrePro.filter("""3+6/3   *  2 -+-  +  2*4/2 + 0/1 -((6+ ((4)))/(2)) -- Teste
                         -- Teste 2"""))
