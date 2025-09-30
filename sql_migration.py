"""
Script SQL direto para migração - Adiciona colunas de feedback
Para ser executado diretamente no console do PostgreSQL do Render
"""

# SQL Commands para executar diretamente no banco
SQL_MIGRATION = """
-- Adiciona colunas de feedback na tabela email_classifications
-- Execute estes comandos um por vez no console do PostgreSQL do Render

-- 1. Adiciona coluna user_feedback
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'email_classifications' 
        AND column_name = 'user_feedback'
    ) THEN
        ALTER TABLE email_classifications 
        ADD COLUMN user_feedback VARCHAR(20) NULL;
        RAISE NOTICE 'Coluna user_feedback adicionada';
    ELSE
        RAISE NOTICE 'Coluna user_feedback já existe';
    END IF;
END $$;

-- 2. Adiciona coluna corrected_category  
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'email_classifications' 
        AND column_name = 'corrected_category'
    ) THEN
        ALTER TABLE email_classifications 
        ADD COLUMN corrected_category VARCHAR(64) NULL;
        RAISE NOTICE 'Coluna corrected_category adicionada';
    ELSE
        RAISE NOTICE 'Coluna corrected_category já existe';
    END IF;
END $$;

-- 3. Adiciona coluna feedback_notes
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'email_classifications' 
        AND column_name = 'feedback_notes'
    ) THEN
        ALTER TABLE email_classifications 
        ADD COLUMN feedback_notes TEXT NULL;
        RAISE NOTICE 'Coluna feedback_notes adicionada';
    ELSE
        RAISE NOTICE 'Coluna feedback_notes já existe';
    END IF;
END $$;

-- 4. Verifica as colunas criadas
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'email_classifications' 
ORDER BY column_name;
"""

if __name__ == "__main__":
    print("🗃️  SQL MIGRATION SCRIPT")
    print("=" * 60)
    print("📋 Execute os comandos SQL abaixo no console PostgreSQL do Render:")
    print("=" * 60)
    print(SQL_MIGRATION)
    print("=" * 60)
    print("💡 COMO EXECUTAR NO RENDER:")
    print("1. Acesse o dashboard do Render")
    print("2. Vá para seu PostgreSQL database")
    print("3. Clique em 'Connect' > 'External Connection'")  
    print("4. Use um cliente PostgreSQL (como psql ou pgAdmin)")
    print("5. Execute os comandos SQL acima")
    print("=" * 60)