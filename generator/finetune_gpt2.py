from transformers import GPT2LMHeadModel, GPT2Tokenizer, DataCollatorForLanguageModeling, Trainer, TrainingArguments
from datasets import Dataset

model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
model = GPT2LMHeadModel.from_pretrained(model_name)

# Read the whole file and split by our custom separator, not by line
with open("data/generator_training_data.txt", "r", encoding="utf-8") as f:
    content = f.read()

emails = [e.strip() for e in content.split("<|endoftext|>") if e.strip()]
print(f"Loaded {len(emails)} whole emails as training examples")

raw_dataset = Dataset.from_dict({"text": emails})

def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, max_length=256, padding="max_length")

tokenized_dataset = raw_dataset.map(tokenize_function, batched=True, remove_columns=["text"])

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

training_args = TrainingArguments(
    output_dir="models/generator",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    save_steps=500,
    save_total_limit=1,
    logging_steps=50,
    fp16=True
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=tokenized_dataset
)

trainer.train()

trainer.save_model("models/generator/final")
tokenizer.save_pretrained("models/generator/final")

print("\nTraining complete. Model saved to models/generator/final")
