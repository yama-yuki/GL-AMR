import torch
from pytorch_transformers import BertTokenizer, BertModel, BertForMaskedLM

ASP = ['begin','began','begun','beginning','start','started','starting',
       'finish','finished','finishing','end','ended','ending']

model = BertForMaskedLM.from_pretrained('bert-base-uncased')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def predict_coercion(text):
    bert_text = '[CLS] ' + text + ' [SEP]'
    tokenized_text = tokenizer.tokenize(text)

    asp_index = 99
    count = 0
    for word in tokenized_text:
        if word in ASP:
            asp_index = count
            count = 0
            break
        count += 1

    to_index = asp_index + 1
    masked_index = to_index + 1
    tokenized_text.insert(to_index, 'to')
    tokenized_text.insert(masked_index, '[MASK]')

    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
    tokens_tensor = torch.tensor([indexed_tokens])

    model = BertForMaskedLM.from_pretrained('bert-base-uncased')
    model.eval()

    #tokens_tensor = tokens_tensor.to('cuda')
    #segments_tensors = segments_tensors.to('cuda')
    #model.to('cuda')

    with torch.no_grad():
        outputs = model(tokens_tensor)
        predictions = outputs[0]

    _, predicted_indexes = torch.topk(predictions[0, masked_index], k=5)
    predicted_tokens = tokenizer.convert_ids_to_tokens(
        predicted_indexes.tolist())

    return tokenized_text, predicted_tokens

def make_new_text(tokenized_text, predicted_token):
    masked_index = tokenized_text.index('[MASK]')
    best_prediction = predicted_token[0]
    CHANGE=['do','be','start','begin','finish','end']
    for i in range(5):
        if best_prediction not in CHANGE:
            best_prediction = predicted_token[i]
            break
    tokenized_text[masked_index] = best_prediction
    print(tokenized_text)
    #new_text = ' '.join(tokenized_text)
    label = predicted_token[0]+str('-01')
    print(predicted_token)
    return label

def predict_label(text):
    tokenized_text, predicted_tokens = predict_coercion(text)
    label = make_new_text(tokenized_text, predicted_tokens)
    return label

'''
if __name__ == '__main__':
    text = 'He began a book.'
    print(predict_label(text))
'''
