from transformers import pipeline
import re

# Palavras-chave que indicam emails produtivos
PRODUCTIVE_KEYWORDS = [
    # Trabalho e negócios
    'reunião', 'meeting', 'projeto', 'project', 'relatório', 'report', 'vendas', 'sales',
    'cliente', 'customer', 'proposta', 'proposal', 'orçamento', 'budget', 'meta', 'goal',
    'resultado', 'result', 'apresentação', 'presentation', 'diretoria', 'board',
    'planejamento', 'planning', 'estratégia', 'strategy', 'análise', 'analysis',
    
    # Solicitações de trabalho
    'acesso', 'access', 'liberação', 'permissão', 'permission', 'aprovação', 'approval',
    'urgente', 'urgent', 'prazo', 'deadline', 'entrega', 'delivery', 'documento', 'document',
    'arquivo', 'file', 'pasta', 'folder', 'drive', 'sistema', 'system',
    
    # Termos profissionais
    'equipe', 'team', 'departamento', 'department', 'coordenação', 'coordination',
    'colaboração', 'collaboration', 'feedback', 'revisão', 'review', 'validação', 'validation',
    'implementação', 'implementation', 'desenvolvimento', 'development',
    
    # Indicadores de trabalho
    'cronograma', 'schedule', 'agenda', 'calendar', 'tarefa', 'task', 'atividade', 'activity',
    'processo', 'process', 'procedimento', 'procedure', 'protocolo', 'protocol',
    'requisito', 'requirement', 'especificação', 'specification'
]

# Palavras-chave que indicam emails improdutivos
UNPRODUCTIVE_KEYWORDS = [
    # Spam e promoções
    'promoção', 'promotion', 'desconto', 'discount', 'oferta', 'offer', 'grátis', 'free',
    'ganhe', 'win', 'prêmio', 'prize', 'sorteio', 'lottery', 'clique', 'click',
    
    # Conteúdo pessoal inadequado
    'piada', 'joke', 'meme', 'corrente', 'chain', 'repassar', 'forward',
    'compartilhar', 'share', 'viral', 'engraçado', 'funny',
    
    # Spam comercial
    'compre', 'buy', 'venda', 'sale', 'liquidação', 'clearance', 'barato', 'cheap',
    'investimento', 'investment', 'dinheiro fácil', 'easy money',
    
    # Conteúdo social e bem-estar (não urgente)
    'café', 'coffee', 'copa', 'cozinha', 'kitchen', 'lanche', 'snack', 'comida', 'food',
    'aniversário', 'birthday', 'festa', 'party', 'confraternização', 'celebration',
    'fique à vontade', 'aproveitem', 'enjoy', 'diversão', 'fun',
    
    # Comunicados gerais não urgentes
    'informativo', 'aviso geral', 'comunicado', 'announcement', 'fyi', 'para conhecimento',
    'nova máquina', 'equipamento', 'facility', 'instalado', 'installed',
    
    # Conteúdo de entretenimento
    'amantes de', 'lovers', 'fãs de', 'fans', 'ótima notícia', 'great news',
    'novidade', 'news', 'chegou', 'arrived', 'finalmente', 'finally'
]

def classify_email(text):
    """
    Classifica email usando modelo IA aprimorado com análise de contexto
    """
    try:
        # Análise inicial com palavras-chave
        text_lower = text.lower()
        
        # Contar palavras-chave produtivas e improdutivas
        productive_score = sum(1 for keyword in PRODUCTIVE_KEYWORDS if keyword in text_lower)
        unproductive_score = sum(1 for keyword in UNPRODUCTIVE_KEYWORDS if keyword in text_lower)
        
        # Análise contextual específica
        contextual_productive_score = 0
        contextual_unproductive_score = 0
        
        # Padrões que indicam emails de trabalho
        work_patterns = [
            r'equipe\s+de\s+\w+',  # "equipe de BI", "equipe de vendas"
            r'relatório\s+\w+',    # "relatório de vendas", "relatório mensal"
            r'acesso\s+ao\s+\w+',  # "acesso ao relatório", "acesso ao system"
            r'apresentação\s+\w+', # "apresentação de resultados"
            r'final\s+do\s+dia',   # prazo urgente
            r'próxim[ao]\s+\w+',   # "próxima sexta", "próximo meeting"
            r'até\s+\w+',          # prazos
            r'preciso\s+\w+',      # necessidades de trabalho
            r'gráficos?\s+e?\s*\w*', # trabalho com dados
            r'metas?\s+\w+',       # trabalho com objetivos
        ]
        
        # Padrões que indicam emails improdutivos/sociais
        social_patterns = [
            r'café\s+(expresso|cappuccino|latte)',  # máquina de café
            r'copa\s+do\s+\w+\s+andar',             # localização social
            r'fiquem\s+à\s+vontade',               # convite informal
            r'só\s+para\s+avisar',                 # comunicado não urgente
            r'aproveitem|enjoy',                    # incentivo de diversão
            r'ótima\s+notícia\s+para',              # anúncio entusiasmado não-trabalho
            r'finalmente\s+chegou',                # chegada de item não-trabalho
            r'já\s+foi\s+instalad[ao]',             # instalação de equipamento social
            r'várias\s+opções',                    # variedade de opções não-trabalho
            r'a\s+administração',                  # assinatura genérica
        ]
        
        for pattern in work_patterns:
            if re.search(pattern, text_lower):
                contextual_productive_score += 2
        
        # Verificar padrões sociais/improdutivos
        for pattern in social_patterns:
            if re.search(pattern, text_lower):
                contextual_unproductive_score += 3  # Peso maior para detectar conteúdo social
        
        # Verificar assinaturas - só conta como produtiva se não for conteúdo social
        if re.search(r'atenciosamente|cordialmente', text_lower) and contextual_unproductive_score == 0:
            contextual_productive_score += 1
        elif re.search(r'abraços', text_lower) and contextual_unproductive_score == 0:
            contextual_productive_score += 0.5  # Peso menor para "abraços"
            
        # Verificar cargos/títulos profissionais
        professional_titles = ['gerente', 'coordenador', 'analista', 'diretor', 'supervisor']
        if any(title in text_lower for title in professional_titles):
            contextual_productive_score += 2
        
        # Score total baseado em keywords e contexto
        keyword_score = productive_score + contextual_productive_score - unproductive_score - contextual_unproductive_score
        
        # Se há evidência clara de conteúdo social/improdutivo, retorna direto
        if contextual_unproductive_score >= 2:
            return "Improdutivo"
        elif keyword_score >= 3:
            return "Produtivo"
        elif keyword_score <= -2:
            return "Improdutivo"
        
        # Usar modelo IA com prompt melhorado para casos ambíguos
        classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        
        # Labels mais específicas e contextualizadas
        candidate_labels = [
            "Email de trabalho produtivo e relevante para negócios",
            "Email improdutivo, social, bem-estar ou conteúdo não relacionado ao trabalho"
        ]
        
        # Adicionar contexto ao texto para melhor classificação
        contextualized_text = f"""
        Análise de email corporativo:
        
        {text}
        
        PRODUTIVO: solicitações de trabalho, relatórios, reuniões, projetos, prazos urgentes, 
        colaboração entre equipes, aprovações, acessos a sistemas, apresentações, vendas.
        
        IMPRODUTIVO: comunicados sobre café/comida, equipamentos sociais (máquina de café), 
        festividades, aniversários, avisos gerais não urgentes, entretenimento, bem-estar,
        instalações de copa/cozinha, convites sociais.
        """
        
        result = classifier(contextualized_text, candidate_labels)
        
        # Interpretação do resultado
        if "produtivo" in result['labels'][0].lower():
            return "Produtivo"
        else:
            return "Improdutivo"
            
    except Exception as e:
        print(f"Erro na classificação: {e}")
        # Fallback: análise simples por keywords
        text_lower = text.lower()
        productive_count = sum(1 for keyword in PRODUCTIVE_KEYWORDS[:10] if keyword in text_lower)
        return "Produtivo" if productive_count >= 2 else "Improdutivo"

def generate_response(text):
    """
    Gera resposta contextualizada baseada no tipo de email
    """
    try:
        text_lower = text.lower()
        
        # Identificar tipo de solicitação para resposta contextualizada
        if any(word in text_lower for word in ['acesso', 'liberação', 'permissão', 'access']):
            return """Olá,
            
Recebi sua solicitação de acesso. Vou verificar as permissões necessárias e liberar o acesso solicitado.

Retorno em breve com confirmação.

Atenciosamente"""
        
        elif any(word in text_lower for word in ['reunião', 'meeting', 'apresentação']):
            return """Olá,
            
Confirmado. Vou me preparar adequadamente para a reunião/apresentação.

Caso precise de algum material adicional, me avise.

Atenciosamente"""
        
        elif any(word in text_lower for word in ['relatório', 'documento', 'arquivo']):
            return """Olá,
            
Recebi sua solicitação. Vou providenciar o documento/relatório solicitado.

Retorno com as informações necessárias em breve.

Atenciosamente"""
        
        elif any(word in text_lower for word in ['urgente', 'prazo', 'deadline']):
            return """Olá,
            
Entendido a urgência. Vou priorizar esta solicitação.

Retorno com atualização em breve.

Atenciosamente"""
        
        else:
            # Resposta genérica profissional
            return """Olá,
            
Recebi seu email e vou analisar a solicitação.

Retorno com informações em breve.

Atenciosamente"""
            
    except Exception as e:
        print(f"Erro na geração de resposta: {e}")
        return """Olá,
        
Recebi seu email e vou analisar a solicitação.

Retorno com informações em breve.

Atenciosamente"""
