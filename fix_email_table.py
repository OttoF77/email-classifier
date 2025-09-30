#!/usr/bin/env python3
"""
Script para aplicar migração do password_hash no banco de produção
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def apply_migration():
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL não encontrada")
        return
    
    # Fix para compatibilidade
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        print("🔗 Conectando ao banco...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("📊 Verificando tabelas disponíveis...")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        
        tables = cursor.fetchall()
        table_names = [t[0] for t in tables]
        print(f"🗂️ Tabelas encontradas: {table_names}")
        
        # Verificar e corrigir tabela email_classifications
        if 'email_classifications' in table_names:
            print("📊 Verificando estrutura da tabela email_classifications...")
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'email_classifications';
            """)
            
            columns = [c[0] for c in cursor.fetchall()]
            print(f"🔍 Colunas existentes: {columns}")
            
            missing_columns = []
            expected_columns = ['user_feedback', 'corrected_category', 'feedback_notes']
            
            for col in expected_columns:
                if col not in columns:
                    missing_columns.append(col)
            
            if missing_columns:
                print(f"🔧 Adicionando colunas faltantes: {missing_columns}")
                
                if 'user_feedback' in missing_columns:
                    cursor.execute("ALTER TABLE email_classifications ADD COLUMN user_feedback VARCHAR(20);")
                    print("  ✅ Coluna user_feedback adicionada")
                
                if 'corrected_category' in missing_columns:
                    cursor.execute("ALTER TABLE email_classifications ADD COLUMN corrected_category VARCHAR(64);")
                    print("  ✅ Coluna corrected_category adicionada")
                
                if 'feedback_notes' in missing_columns:
                    cursor.execute("ALTER TABLE email_classifications ADD COLUMN feedback_notes TEXT;")
                    print("  ✅ Coluna feedback_notes adicionada")
                
                conn.commit()
                print("✅ Migração da estrutura concluída!")
            else:
                print("ℹ️ Todas as colunas já existem")
        else:
            print("❌ Tabela email_classifications não encontrada")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    apply_migration()