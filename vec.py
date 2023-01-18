import os
import torch
from transformers import T5Tokenizer, AutoModelForCausalLM

device = os.environ.get("DEVICE", "cpu")

tokenizer = T5Tokenizer.from_pretrained("rinna/japanese-gpt2-medium")
tokenizer.do_lower_case = True
model = AutoModelForCausalLM.from_pretrained("rinna/japanese-gpt2-medium").to(device)


def calc_vec(text):
    input_ids = tokenizer.encode(text, return_tensors="pt").to(device)
    return torch.mean(model(input_ids)[0][0], 0)

def calc_text_distances(original, texts):
    result = []
    metrics = calc_vec(original) 
    for text in texts:
        vec = calc_vec(text)
        result.append(int(torch.dist(metrics, vec)))
    return result

def sort_with_distance(original, texts):
    distances = calc_text_distances(original, texts)
    text_with_distances = [[texts[i], distances[i]] for i in range(len(texts))]
    return map(lambda x:x[0], sorted(text_with_distances, key=lambda x: x[1]))

