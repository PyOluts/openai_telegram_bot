from config  import PATH_TO_RESOURCES

def load_massage(name:str)->str:
    with open(PATH_TO_RESOURCES/f"{name}.txt",encoding="UTF-8") as file:
        return file.read()
