import re

def classify_email(text, subject=""):
    """Classifica email como Produtivo ou Improdutivo - versão otimizada para Render"""
    try:
        full_text = f"{subject} {text}".lower()
        
        # Palavras-chave produtivas
        productive_keywords = [
            'reunião', 'meeting', 'projeto', 'project', 'relatório', 'report',
            'cliente', 'customer', 'acesso', 'access', 'urgente', 'urgent',
            'prazo', 'deadline', 'documento', 'document', 'sistema', 'system'
        ]
        
        # Palavras-chave improdutivas  
        unproductive_keywords = [
            'café', 'coffee', 'festa', 'party', 'aniversário', 'birthday',
            'máquina de café', 'coffee machine', 'copa', 'kitchen', 'social'
        ]
        
        # Contar matches
        prod_count = sum(1 for keyword in productive_keywords if keyword in full_text)
        unprod_count = sum(1 for keyword in unproductive_keywords if keyword in full_text)
        
        # Decisão simples
        if prod_count > unprod_count:
            return "Produtivo"
        elif unprod_count > prod_count:
            return "Improdutivo"
        else:
            # Fallback: emails longos = produtivo
            return "Produtivo" if len(text.split()) > 10 else "Improdutivo"
            
    except Exception:
        return "Improdutivo"

def generate_response(classification, text="", subject=""):
    """Gera resposta simples baseada na classificação"""
    try:
        if classification == "Produtivo":
            return "Recebi sua solicitação. Retorno em breve com uma resposta."
        else:
            return "Obrigado pela informação. Qualquer dúvida, fico à disposição."
    except Exception:
        return "Obrigado pelo seu email."
