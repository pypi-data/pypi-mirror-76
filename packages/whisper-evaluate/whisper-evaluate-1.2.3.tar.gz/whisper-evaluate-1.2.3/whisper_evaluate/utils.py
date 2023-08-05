from whisper_evaluate.config import en_zh
import sys
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    stream=sys.stdout)


def get_type_index_from_whisper_result(res: dict, _type: str) -> set:
    """
    Args:
        res: the predict result, a dict, like:
            {'matched_words': [],
            'review_words': [],
            'new_words': [{'word': '+1s', 'offset_start': 3, 'offset_end': 5, 'type': 'Politics'}]}
        _type: str, like: 政治
    """
    query_words = res["matched_words"] + res["new_words"]
    if _type == "政治":
        query_words += res["review_words"]
    index_set = set()
    for ele in query_words:
        if en_zh[ele["type"]] == _type:
            for i in range(ele["offset_start"], ele["offset_end"] + 1):
                index_set.add(i)
    return index_set


def get_all_index_from_whisper_result(res: dict) -> set:
    """Get all valid index
    """
    query_words = res["matched_words"] + res["new_words"]
    index_set = set()
    for ele in query_words:
        for i in range(ele["offset_start"], ele["offset_end"] + 1):
            index_set.add(i)
    for ele in res["review_words"]:
        if ele["type"] == "Politics":
            for i in range(ele["offset_start"], ele["offset_end"] + 1):
                index_set.add(i)
    return index_set


def context_test_single(label: list, predict: dict) -> bool:
    label_type = label[3]
    start, end = eval(label[2])
    if label_type == "其他":
        predict_index_set = get_all_index_from_whisper_result(predict)
        for i in range(start, end + 1):
            if i in predict_index_set:
                return False
    else:
        predict_index_set = get_type_index_from_whisper_result(predict, label_type)
        for i in range(start, end + 1):
            if i not in predict_index_set:
                return False
    return True


def regression_test_single(label: list, predict: dict) -> bool:
    label_type = label[3]
    start, end = eval(label[2])
    if label_type == "其他":
        predict_index_set = get_all_index_from_whisper_result(predict)
        for i in range(start, end + 1):
            if i in predict_index_set:
                return False
        return True
    else:
        predict_index_set = get_type_index_from_whisper_result(predict, label_type)
        for i in range(start, end + 1):
            if i in predict_index_set:
                return True
    return False
