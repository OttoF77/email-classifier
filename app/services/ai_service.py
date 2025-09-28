from transformers import pipeline

# Cria a função classify_email(text) que irá carregar um modelo de "zero-shot-classification" do Hugging Face para classificar o texto entre "Produtivo" e "Improdutivo".
def classify_email(text):
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    result = classifier(text, candidate_labels=["Produtivo", "Improdutivo"])
    return result['labels'][0] if result['scores'][0] > result['scores'][1] else "Improdutivo"

# Cria a função generate_response(text) que irá carregar um modelo de geração de texto do Hugging Face para criar uma resposta sugerida ao email.
def generate_response(text):
    generator = pipeline("text-generation", model="gpt2")
    responses = generator(f"Responder ao seguinte email de forma profissional e concisa: {text}", max_length=150, num_return_sequences=1)
    return responses[0]['generated_text'].replace(f"Responder ao seguinte email de forma profissional e concisa: {text}", "").strip()
