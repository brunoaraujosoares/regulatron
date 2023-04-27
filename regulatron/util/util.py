def filter_dict_by_set_keys(d: dict, keys: set) -> dict: # obrigado chat gpt :)
    """
    Retorna um novo dicionário contendo apenas os elementos de `d` cujas chaves estão presentes em `keys`.
    """
    return {k: v for k, v in d.items() if k in keys}