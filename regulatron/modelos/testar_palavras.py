def testar_palavras(texto_pesquisado, yes_words, no_words)-> bool:
    
    """
    Testa se as palavras de yes-words e no-words estão dentro de texto_pesquisado.

    Args:
        texto_pesquisado (str): Texto que deve vir da página web. Pode mesclar o título com o texto.
        yes_words (list): lista de palavras que fazem a função retornar True.
        no_words (list): lista de palavras que fazem a função retornar False.

    Returns:
        Bolean:
    """   
    contagem_no_words = 0
    texto_pesquisado = texto_pesquisado.lower()
    
    for palavra in yes_words:
        if palavra in texto_pesquisado:
            return True
    
    for palavra in no_words:
        if palavra in texto_pesquisado:
            contagem_no_words+= 1
    
    if contagem_no_words > 0:
        return False
    else:
        return True    