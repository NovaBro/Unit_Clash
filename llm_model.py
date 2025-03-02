from mlx_lm import load, generate

model_name = 'meta-llama/Llama-3.2-1B-Instruct'
model, tokenizer = load(model_name)

prompt = "Write a story about Einstein"
# {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"}
messages = [{"role": "user", "content": prompt}]
prompt = tokenizer.apply_chat_template(
    messages, add_generation_prompt=True
)

text = generate(model, tokenizer, prompt=prompt, verbose=True)
print(text)