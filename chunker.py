def Chunker(text, chunk_size):
    """
    Splits a body of text into equally sized chunks of words.

    :param text: The text to be chunked.
    :param chunk_size: The number of words per chunk.
    :return: A list of text chunks.
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = words[i:i + chunk_size]
        chunks.append(' '.join(chunk))

    return chunks