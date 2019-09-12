#! /usr/bin env python


"""
Module containing useful functions shared by other modules.
"""


def order_author(
    author:str,
    split_chars:list=['+', '-', '_',],
):
    """
    Detect <split_chars> in author and order first and second name.

    Parameters
    -------
    author: str
        Author's name

    split_chars: list, default <['+', '-', '_']>
        Delimiters of first and second name of the author
    Returns
    -------
        str, ordered author's first and second name
    """
    split_char = [i for i in split_chars if i in author]
    if any(split_char):
        return ''.join(sorted(author.split(split_char[0]))) 
    return author
