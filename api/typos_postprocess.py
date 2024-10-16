import difflib
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.constant import COMMAND_DICTIONARY

# 將特殊處理規則抽離到字典中
SPECIAL_CASES = {
    'ed': (lambda index: index <= 1, 'add'),     # 如果單詞是 'ed' 並且在前 3 個單詞中，替換為 'add'
    'hong': (lambda index: index <= 1, 'home'),  # 如果單詞是 'hong' 並且在前 3 個單詞中，替換為 'home'
}


# 多字母合併規則
MERGE_RULES = {
    ('n', 'f', 'c'): 'nfc',   # 將 "n f c" 合併成 "nfc"
    # 可以在這裡添加更多需要合併的字符
}


def apply_special_cases(word, index):
    """    
    Apply special case rules to a word based on its index in the sentence.
    
    :param  
    ----------  
    word: str  
        The word to be checked and potentially modified  
    index: int  
        The index of the word in the sentence  
    
    :rtype  
    ----------  
    word: str  
        The word after applying special case rules, if applicable  
    """  
    if word in SPECIAL_CASES:
        condition, replacement = SPECIAL_CASES[word]
        if condition(index):
            return replacement
    return word


def merge_letters(sentence):
    """    
    Merge consecutive single characters according to predefined rules.
    
    :param  
    ----------  
    sentence: list  
        The sentence to be processed, split by words  
    
    :rtype  
    ----------  
    merged_sentence: list  
        The processed sentence with merged characters  
    """  
    merged_sentence = []
    skip = 0  # 用於跳過已合併的單字
    for i in range(len(sentence)):
        if skip > 0:
            skip -= 1
            continue
        
        # 檢查是否有符合的合併規則
        if i + 2 < len(sentence):
            triplet = (sentence[i], sentence[i + 1], sentence[i + 2])
            if triplet in MERGE_RULES:
                merged_sentence.append(MERGE_RULES[triplet])
                skip = 2  # 合併了 3 個單字，跳過下一個兩個單字
                continue

        # 否則直接加入
        merged_sentence.append(sentence[i])
    
    return merged_sentence

def check_special_case(sentence):
    """    
    Handle special cases in the sentence by applying special rules to each word.
    
    :param  
    ----------  
    sentence: list  
        The sentence to be processed, split by words  
    
    :rtype  
    ----------  
    corrected_sentence: list  
        The processed sentence, split by words  
    """  
    corrected_sentence = []
    for index, word in enumerate(sentence):
        corrected_word = apply_special_cases(word, index)
        corrected_sentence.append(corrected_word)

    return corrected_sentence


def correct_sentence(sentence):
    """    
    Correct the words in the sentence. Perform correction based on the command dictionary and closest matches.
    
    :param  
    ----------  
    sentence: str  
        The sentence to be corrected  
    
    :rtype  
    ----------  
    corrected_sentence: str  
        The corrected sentence  
    """  
    corrected_sentence = []
    for word in sentence.split():
        if word in COMMAND_DICTIONARY:
            corrected_sentence.append(word)
        else:
            closest_word = difflib.get_close_matches(word, COMMAND_DICTIONARY, n=1, cutoff=0.6)
            if closest_word:
                corrected_sentence.append(closest_word[0])
            else:
                corrected_sentence.append(word)

        # 檢查特殊案例
        corrected_sentence = check_special_case(corrected_sentence)

    # 檢查是否需要合併單字
    corrected_sentence = merge_letters(corrected_sentence)

    return " ".join(corrected_sentence)


if __name__ == "__main__":
    import time

    # 測試
    sentence = "n f c"
    start = time.time()
    corrected = correct_sentence(sentence)
    end = time.time()
    print("Original text:", sentence)
    print("Corrected text:", corrected)
    print("spent time:", end - start)
