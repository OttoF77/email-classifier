import re

def classify_email(text, subject=""):
    """Classifica email como Produtivo ou Improdutivo - versão otimizada para Render"""
    try:
        full_text = f"{subject} {text}".lower()
        
        # Palavras-chave produtivas (expandidas)
        productive_keywords = [
            'reunião', 'meeting', 'projeto', 'project', 'relatório', 'report',
            'cliente', 'customer', 'acesso', 'access', 'urgente', 'urgent',
            'prazo', 'deadline', 'documento', 'document', 'sistema', 'system',
            'contrato', 'contract', 'proposta', 'proposal', 'orçamento', 'budget',
            'vendas', 'sales', 'negócio', 'business', 'cronograma', 'schedule',
            'deliverable', 'tarefa', 'task', 'agenda', 'ação', 'action'
        ]
        
        # Palavras-chave improdutivas (muito expandidas)
        unproductive_keywords = [
            'café', 'coffee', 'festa', 'party', 'aniversário', 'birthday',
            'máquina de café', 'coffee machine', 'copa', 'kitchen', 'social',
            'netflix', 'série', 'series', 'filme', 'movie', 'gato', 'cat',
            'cachorro', 'dog', 'brigadeiro', 'doce', 'sweet', 'chocolate',
            'happy hour', 'cerveja', 'beer', 'fofoca', 'gossip', 'whatsapp',
            'youtube', 'instagram', 'facebook', 'tiktok', 'meme', 'emoji',
            'beijos', 'abraços', 'kisses', 'hugs', 'oi pessoal', 'galera',
            'promoção', 'promotion', 'caribe', 'viagem pessoal', 'vacation'
        ]
        
        # Padrões de linguagem informal (peso maior)
        informal_patterns = [
            'oi pessoal', 'galera', '!!!', '??', '😂', '😱', '🎉', '💕',
            'super interessante', 'que legal', 'nossa', 'não vou dar spoiler'
        ]
        
        # Contar matches
        prod_count = sum(1 for keyword in productive_keywords if keyword in full_text)
        unprod_count = sum(1 for keyword in unproductive_keywords if keyword in full_text)
        informal_count = sum(1 for pattern in informal_patterns if pattern in full_text)
        
        # Linguagem informal tem peso maior para improdutivo
        unprod_count += informal_count * 2
        
        # Decisão melhorada
        if prod_count > unprod_count:
            return "Produtivo"
        elif unprod_count > prod_count:
            return "Improdutivo"
        else:
            # Fallback melhorado: detectar características
            if any(pattern in full_text for pattern in ['re: re:', 'fwd:', 'promoção', 'oi pessoal']):
                return "Improdutivo"
            elif any(word in full_text for word in ['prezado', 'atenciosamente', 'cordialmente']):
                return "Produtivo"
            else:
                return "Improdutivo"  # Padrão mais seguro
            
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
