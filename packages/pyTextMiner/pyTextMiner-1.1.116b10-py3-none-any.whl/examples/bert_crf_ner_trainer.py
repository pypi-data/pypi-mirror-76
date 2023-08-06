from py_ner.bert_crf_ner_train import BertCrfTrainer

data = 'data'
model_dir = 'experiments/base_model_with_crf_val'
trainer = BertCrfTrainer(data_dir=data, model_dir=model_dir)
trainer.data_loading()
trainer.train()