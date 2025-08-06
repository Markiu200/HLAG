class MyClass:
    def __init__(self, string1, string2 = None, children = []):
        self.string1 = string1
        self.string2 = string2
        self.children = children


the_path = "String 1"
root = MyClass(the_path)

root.children.append(MyClass(the_path + " nested", the_path))

print(root)
