import argparse
import pandas as pd
import json
import collections
import unicodedata
import regex
from typing import Union, List


def load_mintaka_test(path_to_test_set: str, mode: str, lang: str) -> pd.DataFrame:
    """
    Loads the Mintaka test set as a dataframe
    Args:
        path_to_test_set: path to the Mintaka test set file
        mode: mode of evaluation (kg or text)
        lang: language of evaluation (for text answers)
    Returns:
        mintaka_test: the Mintaka test set as a dataframe
    """
    mintaka_test = pd.read_json(path_to_test_set)
    mintaka_test['answer'] = mintaka_test['answer'].apply(lambda x: format_answers(x, mode, lang))
    return mintaka_test


def load_predictions(path_to_predictions: str, mode: str) -> pd.DataFrame:
    """
    Loads model predictions on the Mintaka test as a dataframe
    Args:
        path_to_predictions: path to model predictions on the Mintaka test set
        mode: mode of evaluation (kg or text)
    Returns:
        mintaka_pred: predictions on the Mintaka test set as a dataframe
    """
    with open(path_to_predictions) as pred_file:
        mintaka_pred = pd.DataFrame(json.load(pred_file).items(), columns=['id', 'pred'])
    mintaka_pred['pred'] = mintaka_pred['pred'].apply(lambda x: format_predictions(x, mode))
    return mintaka_pred


def format_answers(answer: dict, mode: str, lang: str) -> Union[list, str, None]:
    """
    Formats answers from the Mintaka test set based on evaluation mode (kg or text)
    Args:
        answer: answer from the Mintaka test set
        mode: mode of evaluation (kg or text)
        lang: language of evaluation (for text answers)
    Returns:
        The answer either as a list for KG evaluation or a string for text evaluation
    """
    if answer['answerType'] == 'entity':
        if mode == 'kg':
            if answer['answer'] is None:
                return None
            return [ent['name'] for ent in answer['answer']]  # return a list of Q-codes
        else:
            if answer['answer'] is None:
                return answer['mention']  # if no entities linked, return annotator's text answer
            else:
                return ' '.join([ent['label'][lang] if ent['label'][lang]
                                 else ent['label']['en'] for ent in answer['answer']])  # return entity labels
    else:
        return str(answer['answer'][0]) if mode == 'text' else answer['answer']


def format_predictions(pred: object, mode: str) -> Union[list, str, None]:
    """
    Formats predictions to standardized format
    Args:
        pred: predicted answer from a model
        mode: mode of evaluation (kg or text)
    Returns:
        The predicted answer formatted either as a list for KG evaluation or a string for text evaluation
    """
    if pred is None:
        return pred
    elif mode == 'text':
        return str(pred)  # return prediction as string
    elif mode == 'kg' and not isinstance(pred, list):
        return [pred]  # return prediction as list
    return pred


def normalize_and_tokenize_text(text: str) -> List[str]:
    """
    Normalize and tokenize text based on evaluation script of DPR:
    https://github.com/facebookresearch/DPR/blob/main/dpr/data/qa_validation.py#L175
    Args:
        text: a text answer
    Returns:
        tokens: a list of normalized tokens from the text answer
    """
    ALPHA_NUM = r"[\p{L}\p{N}\p{M}]+"
    NON_WS = r"[^\p{Z}\p{C}]"
    _regexp = regex.compile(
        "(%s)|(%s)" % (ALPHA_NUM, NON_WS),
        flags=regex.IGNORECASE + regex.UNICODE + regex.MULTILINE,
        )
    text = unicodedata.normalize("NFD", text)
    tokens = []
    matches = [m for m in _regexp.finditer(text)]
    for i in range(len(matches)):
        token = matches[i].group()
        tokens.append(token.lower())
    return tokens


def calculate_em(pred: Union[list, str, None], answer: Union[list, str, None], mode: str) -> int:
    """
    Calculate an exact match score
    Args:
        pred: predicted answer from a model
        answer: answer from the Mintaka test set
        mode: mode of evaluation (kg or text)
    Returns:
        1 if the prediction exactly matches the answer, else 0
    """
    if mode == 'text' and pred and answer:
        pred = normalize_and_tokenize_text(pred)
        answer = normalize_and_tokenize_text(answer)
        for i in range(0, len(pred) - len(answer) + 1):
            if answer == pred[i: i + len(answer)]:
                return True
        return False
    else:
        return int(pred == answer)


def calculate_f1(pred: Union[str, List], answer: Union[str, List], mode: str) -> float:
    """
    Calculate an F1 score, based on the SQuAD 2.0 evaluate-v2.0.py script
    Args:
        pred: predicted answer from a model
        answer: answer from the Mintaka test set
        mode: mode of evaluation (kg or text)
    Returns:
        An F1 score based on the tokens in a text answer or the list elements in a KG answer
    """
    if not answer or not pred:
        return int(answer == pred)
    if mode == 'text':
        pred = pred.split()
        answer = answer.split()
    common = collections.Counter(pred) & collections.Counter(answer)
    num_same = sum(common.values())
    if num_same == 0:
        return 0
    precision = 1.0 * num_same / len(pred)
    recall = 1.0 * num_same / len(answer)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1


def calculate_h1(pred: Union[str, List], answer: Union[str, List], mode: str) -> int:
    """
    Calculate a hits@1 score
    Args:
        pred: predicted answer from a model
        answer: answer from the Mintaka test set
        mode: mode of evaluation (kg or text)
    Returns:
        For text or null answers, this is the same as exact match
        For list answers, returns 1 if at least one predicted answer appears in the answer, else 0
    """
    if mode == 'text' or pred is None or answer is None:
        return calculate_em(pred, answer, mode)
    else:
        return int(len(collections.Counter(pred) & collections.Counter(answer)) > 0)


def mintaka_evaluation(mode: str, path_to_test_set: str, path_to_predictions: str, lang: str):
    """
    Evaluated predictions on the Mintaka test set and returns exact match, F1, and hits@1 scores
    Args:
        mode: mode of evaluation (kg or text)
        path_to_test_set: path to Mintaka test set file
        path_to_predictions: path to file with model predictions
        lang: language of evaluation (for text answers)
    """
    mintaka_test = load_mintaka_test(path_to_test_set, mode, lang)
    mintaka_pred = load_predictions(path_to_predictions, mode)
    mintaka_test = mintaka_test.merge(mintaka_pred, on='id', how='left')

    mintaka_test['exact_match'] = mintaka_test[['pred', 'answer']].apply(lambda x: calculate_em(*x, mode), axis=1)
    mintaka_test['f1'] = mintaka_test[['pred', 'answer']].apply(lambda x: calculate_f1(*x, mode), axis=1)
    mintaka_test['hits1'] = mintaka_test[['pred', 'answer']].apply(lambda x: calculate_h1(*x, mode), axis=1)

    print(f"Exact Match: {mintaka_test.exact_match.mean():.4f}")
    print(f"F1: {mintaka_test.f1.mean():.4f}")
    print(f"Hits@1: {mintaka_test.hits1.mean():.4f}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=['kg', 'text'],
                        help="Evaluation mode using knowledge graph IDs or text")
    parser.add_argument("--path_to_test_set", help="Path to Mintaka test set file", default='data/mintaka_test.json')
    parser.add_argument("--path_to_predictions", help="Path to file with model predictions")
    parser.add_argument("--lang", default='en', choices=['en', 'ar', 'de', 'es', 'fr', 'hi', 'it',  'ja', 'pt'],
                        help="Language if evaluating on text")

    args = parser.parse_args()

    mintaka_evaluation(
        args.mode,
        args.path_to_test_set,
        args.path_to_predictions,
        args.lang
    )
