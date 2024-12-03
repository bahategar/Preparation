from transformers import BertModel
import torch


class bertATE(torch.nn.Module):
    def __init__(self, pretrain_model):
        super(bertATE, self).__init__()
        self.bert = BertModel.from_pretrained(pretrain_model)
        self.linear = torch.nn.Linear(self.bert.config.hidden_size, 3)
        self.loss_fn = torch.nn.CrossEntropyLoss()

    def forward(self, ids_tensors, tags_tensors, masks_tensors):
        bert_outputs, _ = self.bert(input_ids=ids_tensors, attention_mask=masks_tensors, return_dict=False)
        linear_outputs = self.linear(bert_outputs)

        if tags_tensors is not None:
            tags_tensors = tags_tensors.view(-1)
            linear_outputs = linear_outputs.view(-1, 3)
            loss = self.loss_fn(linear_outputs, tags_tensors)
            return loss
        else:
            return linear_outputs


class bertABSA(torch.nn.Module):
    def __init__(self, pretrain_model):
        super(bertABSA, self).__init__()
        self.bert = BertModel.from_pretrained(pretrain_model)
        self.linear = torch.nn.Linear(self.bert.config.hidden_size, 3)
        self.loss_fn = torch.nn.CrossEntropyLoss()

    def forward(self, ids_tensors, lable_tensors, masks_tensors, segments_tensors):
        _, pooled_outputs = self.bert(input_ids=ids_tensors, attention_mask=masks_tensors, return_dict=False)
        linear_outputs = self.linear(pooled_outputs)

        if lable_tensors is not None:
            loss = self.loss_fn(linear_outputs, lable_tensors)
            return loss
        else:
            return linear_outputs