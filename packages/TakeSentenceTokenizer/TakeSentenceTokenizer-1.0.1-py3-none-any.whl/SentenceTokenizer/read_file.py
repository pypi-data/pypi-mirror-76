def read_txt_file(txt_path: str):
    with open(txt_path, 'r',encoding='utf-8') as f:
        lines = [line.rstrip() for line in f]
        return lines
        
def read_json(dict_path: str):
    with open(dict_path, encoding='utf-8') as f:
        return json.loads(f.read())