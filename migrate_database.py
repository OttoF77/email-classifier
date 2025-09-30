"""
Script de migração para adicionar colunas de feedback na tabela email_classifications
Este script adiciona as colunas que estão faltando no banco de produção.
"""

import os
import sys
import psycopg2
from urllib.parse import urlparse

def migrate_database():
    """Adiciona as colunas de feedback na tabela email_classifications"""
    
    # URL do banco de dados (usar variável de ambiente ou URL direta)
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ Erro: DATABASE_URL não encontrada nas variáveis de ambiente")
        print("💡 Configure a variável DATABASE_URL com a URL do PostgreSQL do Render")
        return False
    
    try:
        # Parse da URL do banco
        parsed_url = urlparse(database_url)
        
        # Conecta ao banco
        print("🔄 Conectando ao banco de dados...")
        conn = psycopg2.connect(
            host=parsed_url.hostname,
            database=parsed_url.path[1:],  # Remove a barra inicial
            user=parsed_url.username,
            password=parsed_url.password,
            port=parsed_url.port or 5432
        )
        
        cursor = conn.cursor()
        
        # Lista das colunas que precisam ser adicionadas
        columns_to_add = [
            {
                'name': 'user_feedback',
                'type': 'VARCHAR(20)',
                'constraint': 'NULL'
            },
            {
                'name': 'corrected_category', 
                'type': 'VARCHAR(64)',
                'constraint': 'NULL'
            },
            {
                'name': 'feedback_notes',
                'type': 'TEXT',
                'constraint': 'NULL'
            }
        ]
        
        print("🔄 Verificando colunas existentes...")
        
        # Verifica quais colunas já existem
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'email_classifications'
        """)
        
        existing_columns = [row[0] for row in cursor.fetchall()]
        print(f"📋 Colunas existentes: {existing_columns}")
        
        # Adiciona apenas as colunas que não existem
        columns_added = 0
        for column in columns_to_add:
            if column['name'] not in existing_columns:
                sql = f"""
                    ALTER TABLE email_classifications 
                    ADD COLUMN {column['name']} {column['type']} {column['constraint']}
                """
                
                print(f"➕ Adicionando coluna: {column['name']}")
                cursor.execute(sql)
                columns_added += 1
            else:
                print(f"✅ Coluna {column['name']} já existe")
        
        # Confirma as alterações
        if columns_added > 0:
            conn.commit()
            print(f"✅ Migração concluída! {columns_added} colunas adicionadas")
        else:
            print("ℹ️  Nenhuma coluna precisou ser adicionada")
        
        # Verifica o resultado final
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'email_classifications'
            ORDER BY column_name
        """)
        
        final_columns = [row[0] for row in cursor.fetchall()]
        print(f"📋 Colunas finais: {final_columns}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Erro do PostgreSQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando migração do banco de dados...")
    print("=" * 50)
    
    success = migrate_database()
    
    print("=" * 50)
    if success:
        print("🎉 Migração concluída com sucesso!")
        print("💡 Agora você pode fazer deploy da aplicação")
    else:
        print("💥 Falha na migração!")
        print("🔧 Verifique os erros acima e tente novamente")
    
    sys.exit(0 if success else 1)