#!/usr/bin/env python3
"""
Script para aplicar mi            print("🔧 Criando tabela email_classifications...")
            cursor.execute("""
                CREATE TABLE email_classifications (
                    id SERIAL PRIMARY KEY,
                    content TEXT NOT NULL,
                    category VARCHAR(64) NOT NULL,
                    suggested_response TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_feedback VARCHAR(20),
                    corrected_category VARCHAR(64),
                    feedback_notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                );
            """)ssword_hash no banco de produção
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
        
        if 'users' not in table_names:
            print("🔧 Criando tabela users...")
            cursor.execute("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(64) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL
                );
            """)
            
            print("� Criando tabela email_classifications...")
            cursor.execute("""
                CREATE TABLE email_classifications (
                    id SERIAL PRIMARY KEY,
                    content TEXT NOT NULL,
                    category VARCHAR(20) NOT NULL,
                    suggested_response TEXT,
                    user_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                );
            """)
            
            print("🔧 Criando tabela user_feedback...")
            cursor.execute("""
                CREATE TABLE user_feedback (
                    id SERIAL PRIMARY KEY,
                    classification_id INTEGER NOT NULL,
                    is_correct BOOLEAN NOT NULL,
                    feedback_text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (classification_id) REFERENCES email_classifications (id) ON DELETE CASCADE
                );
            """)
            
            conn.commit()
            print("✅ Tabelas criadas com sucesso!")
            
        else:
            print("📊 Verificando estrutura da tabela users...")
            cursor.execute("""
                SELECT column_name, data_type, character_maximum_length 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'password_hash';
            """)
            
            result = cursor.fetchone()
            if result:
                print(f"🔍 Campo password_hash: {result[1]}({result[2]})")
                
                if result[2] and result[2] < 255:
                    print("🔧 Alterando campo para VARCHAR(255)...")
                    cursor.execute("ALTER TABLE users ALTER COLUMN password_hash TYPE VARCHAR(255);")
                    conn.commit()
                    print("✅ Migração aplicada com sucesso!")
                else:
                    print("ℹ️ Campo já tem tamanho adequado")
            else:
                print("❌ Campo password_hash não encontrado")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    apply_migration()