from flask import render_template, flash, redirect, url_for, abort
from . import main
from flask_login import login_required, current_user
from app.main.forms import EmailForm
from app.models import EmailClassification
from app import db
from app.services.ai_service import classify_email, generate_response
import PyPDF2
import io

# Cria a rota para a pagina principal do blueprint main
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = EmailForm()
    
    if form.validate_on_submit():
        email_text = ""
        
        # Verifica se um arquivo foi enviado
        if form.file.data:
            file = form.file.data
            filename = file.filename.lower()
            
            try:
                if filename.endswith('.txt'):
                    # Lê arquivo .txt
                    email_text = file.read().decode('utf-8')
                elif filename.endswith('.pdf'):
                    # Lê arquivo .pdf
                    try:
                        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
                        email_text = ""
                        for page in pdf_reader.pages:
                            email_text += page.extract_text() + "\n"
                    except Exception as e:
                        flash(f'Erro ao processar PDF: {str(e)}', 'danger')
                        return redirect(url_for('main.dashboard'))
                else:
                    flash('Formato de arquivo não suportado. Use apenas .txt ou .pdf', 'danger')
                    return redirect(url_for('main.dashboard'))
                    
            except Exception as e:
                flash(f'Erro ao ler arquivo: {str(e)}', 'danger')
                return redirect(url_for('main.dashboard'))
        else:
            # Se não há arquivo, usa o conteúdo do TextAreaField
            email_text = form.content.data
        
        # Verifica se temos conteúdo para processar
        if not email_text or not email_text.strip():
            flash('Nenhum conteúdo encontrado para classificar.', 'danger')
            return redirect(url_for('main.dashboard'))
        
        # Chama as funções do ai_service.py para obter categoria e resposta sugerida
        try:
            categoria = classify_email(email_text)
            resposta_sugerida = generate_response(email_text)
        except Exception as e:
            flash(f'Erro ao processar com IA: {str(e)}', 'danger')
            return redirect(url_for('main.dashboard'))
        
        # Cria uma nova instância do modelo EmailClassification
        email_classification = EmailClassification(
            content=email_text,
            category=categoria,
            suggested_response=resposta_sugerida,
            user_id=current_user.id
        )
        
        # Salva no banco de dados
        db.session.add(email_classification)
        db.session.commit()
        
        # Feedback ao usuário
        flash('E-mail classificado com sucesso!', 'success')
        
        # Redireciona para evitar reenvio do formulário
        return redirect(url_for('main.dashboard'))
    
    # Busca todas as classificações do usuário atual, ordenadas da mais recente para a mais antiga
    email_classifications = EmailClassification.query.filter_by(user_id=current_user.id).order_by(EmailClassification.timestamp.desc()).all()
    
    return render_template('dashboard.html', form=form, email_classifications=email_classifications)

@main.route('/response/<int:classification_id>')
@login_required
def view_response(classification_id):
    # Busca a classificação pelo ID
    classification = EmailClassification.query.get_or_404(classification_id)
    
    # Verificação de segurança: garante que o registro pertence ao usuário atual
    if classification.user_id != current_user.id:
        flash('Você não tem permissão para visualizar esta classificação.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Se chegou até aqui, o usuário tem permissão para ver a classificação
    return render_template('response_detail.html', classification=classification)
