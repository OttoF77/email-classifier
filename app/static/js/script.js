// Email Classifier - JavaScript Functions

// ============================================
// DASHBOARD FUNCTIONS
// ============================================

$(document).ready(function() {
    // Limpa o textarea quando um arquivo é selecionado
    $('#file').change(function() {
        if (this.files && this.files.length > 0) {
            $('#content').val('').prop('disabled', true);
            $('#content').attr('placeholder', 'Arquivo selecionado: ' + this.files[0].name);
        } else {
            $('#content').prop('disabled', false);
            $('#content').attr('placeholder', 'Cole o conteúdo do email aqui...');
        }
    });
    
    // Limpa o campo de arquivo quando o textarea é usado
    $('#content').on('input', function() {
        if ($(this).val().trim().length > 0) {
            $('#file').val('').prop('disabled', true);
        } else {
            $('#file').prop('disabled', false);
        }
    });
    
    // Validação do tamanho do arquivo (16MB)
    $('#file').change(function() {
        if (this.files && this.files[0]) {
            const fileSize = this.files[0].size;
            const maxSize = 16 * 1024 * 1024; // 16MB
            
            if (fileSize > maxSize) {
                alert('O arquivo é muito grande. O tamanho máximo é 16MB.');
                $(this).val('');
                $('#content').prop('disabled', false);
                $('#content').attr('placeholder', 'Cole o conteúdo do email aqui...');
            }
        }
    });
    
    // Navegação por clique nas linhas da tabela
    $('.table-row-clickable').on('click', function() {
        const url = $(this).data('url');
        if (url) {
            window.location.href = url;
        }
    });
    
    // Event handler para botões de copiar com data attributes
    $('.copy-btn').on('click', function() {
        const targetId = $(this).data('target');
        if (targetId) {
            copyToClipboard(targetId);
        }
    });
});

// Função para prevenir propagação de eventos em botões dentro da tabela
function stopPropagation(event) {
    event.stopPropagation();
}

// ============================================
// RESPONSE DETAIL FUNCTIONS
// ============================================

function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    element.select();
    element.setSelectionRange(0, 99999); // Para mobile
    
    try {
        document.execCommand('copy');
        // Feedback visual
        const button = event.target.closest('button');
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="bi bi-check"></i> Copiado!';
        button.classList.remove('btn-outline-primary', 'btn-outline-secondary');
        button.classList.add('btn-success');
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.classList.remove('btn-success');
            button.classList.add(elementId === 'suggested-response' ? 'btn-outline-primary' : 'btn-outline-secondary');
        }, 2000);
    } catch (err) {
        console.error('Erro ao copiar: ', err);
        alert('Erro ao copiar para a área de transferência');
    }
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

// Função genérica para adicionar classes com animação
function addAnimationClass(element, className, duration = 2000) {
    const el = typeof element === 'string' ? document.querySelector(element) : element;
    if (el) {
        el.classList.add(className);
        setTimeout(() => {
            el.classList.remove(className);
        }, duration);
    }
}

// Função para scroll suave
function smoothScrollTo(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// Função para feedback visual em botões
function buttonFeedback(button, message, originalMessage, feedbackClass = 'btn-success', duration = 2000) {
    const originalClasses = button.className;
    button.innerHTML = message;
    button.className = button.className.replace(/btn-\w+/g, '') + ' ' + feedbackClass;
    
    setTimeout(() => {
        button.innerHTML = originalMessage;
        button.className = originalClasses;
    }, duration);
}
