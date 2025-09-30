from flask import render_template, flash, redirect, url_for, abort, request, jsonify
from . import main
from flask_login import login_required, current_user
from app.main.forms import EmailForm, FeedbackForm
from app.models import EmailClassification
from app import db
from app.services.ai_service import classify_email, generate_response
import PyPDF2
import io
from sqlalchemy import text

# Cria a rota para a pagina principal do blueprint main
@main.route('/')
def index():
    return render_template('main/index.html')

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
    
    return render_template('main/dashboard.html', form=form, email_classifications=email_classifications)

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
    return render_template('main/response_detail.html', classification=classification)

@main.route('/feedback/<int:classification_id>', methods=['GET', 'POST'])
@login_required
def feedback(classification_id):
    """Página para fornecer feedback sobre a classificação da IA"""
    classification = EmailClassification.query.get_or_404(classification_id)
    
    # Verificação de segurança
    if classification.user_id != current_user.id:
        flash('Você não tem permissão para visualizar esta classificação.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    form = FeedbackForm()
    
    if form.validate_on_submit():
        # Atualizar a classificação com o feedback
        classification.user_feedback = form.feedback_type.data
        classification.corrected_category = form.corrected_category.data
        classification.feedback_notes = form.feedback_notes.data
        
        db.session.commit()
        flash('Obrigado pelo seu feedback! Isso nos ajuda a melhorar a IA.', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('main/feedback.html', form=form, classification=classification)

@main.route('/delete/<int:classification_id>', methods=['POST'])
@login_required
def delete_classification(classification_id):
    """Excluir uma classificação de email"""
    classification = EmailClassification.query.get_or_404(classification_id)
    
    # Verificação de segurança: garante que o registro pertence ao usuário atual
    if classification.user_id != current_user.id:
        flash('Você não tem permissão para excluir esta classificação.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    try:
        db.session.delete(classification)
        db.session.commit()
        flash('Classificação excluída com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao excluir classificação. Tente novamente.', 'danger')
    
    return redirect(url_for('main.dashboard'))

@main.route('/migrate-database-schema')
def migrate_database():
    """
    ROTA TEMPORÁRIA - Migração do schema do banco de dados
    Adiciona as colunas de feedback que estão faltando em produção
    """
    try:
        # Lista de colunas a serem adicionadas
        migrations = [
            {
                'column': 'user_feedback',
                'sql': 'ALTER TABLE email_classifications ADD COLUMN IF NOT EXISTS user_feedback VARCHAR(20) NULL'
            },
            {
                'column': 'corrected_category',
                'sql': 'ALTER TABLE email_classifications ADD COLUMN IF NOT EXISTS corrected_category VARCHAR(64) NULL'
            },
            {
                'column': 'feedback_notes',
                'sql': 'ALTER TABLE email_classifications ADD COLUMN IF NOT EXISTS feedback_notes TEXT NULL'
            }
        ]
        
        results = []
        
        # Executa cada migração
        for migration in migrations:
            try:
                db.session.execute(text(migration['sql']))
                db.session.commit()
                results.append(f"✅ Coluna '{migration['column']}' adicionada com sucesso")
            except Exception as e:
                db.session.rollback()
                if "already exists" in str(e).lower() or "duplicate column" in str(e).lower():
                    results.append(f"ℹ️  Coluna '{migration['column']}' já existe")
                else:
                    results.append(f"❌ Erro na coluna '{migration['column']}': {str(e)}")
        
        # Verifica as colunas finais
        try:
            result = db.session.execute(text("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'email_classifications' 
                ORDER BY column_name
            """))
            columns = result.fetchall()
            column_list = [f"{col[0]} ({col[1]}, nullable: {col[2]})" for col in columns]
            
            return jsonify({
                'status': 'success',
                'message': 'Migração concluída',
                'results': results,
                'final_columns': column_list
            })
            
        except Exception as e:
            return jsonify({
                'status': 'partial_success',
                'message': 'Migração executada mas erro ao listar colunas',
                'results': results,
                'error': str(e)
            })
            
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': 'Falha na migração',
            'error': str(e)
        }), 500


