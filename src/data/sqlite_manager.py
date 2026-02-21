# src/data/sqlite_manager.py
"""
Gerenciador de banco SQLite
"""

import sqlite3
import pandas as pd
from pathlib import Path
import logging
from config.settings import Settings

# Configurar logger
logger = logging.getLogger(__name__)


class SQLiteManager:
    """Gerencia operações com SQLite"""

    def __init__(self, db_path=None):
        """
        Inicializa o gerenciador SQLite

        Args:
            db_path: Caminho para o arquivo do banco (opcional)
        """
        self.db_path = db_path or Settings.SQLITE_PATH
        self.conn = None
        logger.info(f"SQLiteManager inicializado: {self.db_path}")

    def connect(self):
        """Estabelece conexão com o banco"""
        try:
            self.conn = sqlite3.connect(str(self.db_path))
            return self.conn
        except Exception as e:
            logger.error(f"Erro na conexão: {e}")
            return None

    def disconnect(self):
        """Fecha conexão"""
        if self.conn:
            self.conn.close()
            self.conn = None

    def df_to_sql(self, df, table_name, if_exists='replace'):
        """
        Salva DataFrame em tabela SQL

        Args:
            df: DataFrame a ser salvo
            table_name: Nome da tabela
            if_exists: Comportamento se tabela existir ('replace', 'append', 'fail')

        Returns:
            bool: True se sucesso, False caso contrário
        """
        conn = self.connect()
        if not conn:
            return False

        try:
            df.to_sql(table_name, conn, if_exists=if_exists, index=False)
            logger.info(f"DataFrame salvo em '{table_name}' ({len(df)} linhas)")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar: {e}")
            return False
        finally:
            self.disconnect()

    def sql_to_df(self, query):
        """
        Executa query SQL e retorna DataFrame

        Args:
            query: String SQL

        Returns:
            DataFrame com resultados
        """
        conn = self.connect()
        if not conn:
            return pd.DataFrame()

        try:
            df = pd.read_sql_query(query, conn)
            logger.debug(f"Query retornou {len(df)} linhas")
            return df
        except Exception as e:
            logger.error(f"Erro na query: {e}")
            return pd.DataFrame()
        finally:
            self.disconnect()

    def list_tables(self):
        """Lista tabelas do banco"""
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        conn = self.connect()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute(query)
            tables = [row[0] for row in cursor.fetchall()]
            return tables
        except Exception as e:
            logger.error(f"Erro ao listar tabelas: {e}")
            return []
        finally:
            self.disconnect()

    def execute_query(self, query, params=None):
        """
        Executa query SQL (não SELECT)

        Args:
            query: String SQL
            params: Parâmetros para query parametrizada

        Returns:
            int: Número de linhas afetadas ou None
        """
        conn = self.connect()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            conn.commit()
            return cursor.rowcount
        except Exception as e:
            logger.error(f"Erro na query: {e}")
            return None
        finally:
            self.disconnect()

    def backup_database(self):
        """
        Cria backup do banco SQLite

        Returns:
            Path: Caminho do backup ou None
        """
        import shutil
        from datetime import datetime

        backup_dir = Settings.DATA_DIR / "backups"
        backup_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"analytics_backup_{timestamp}.db"

        try:
            shutil.copy2(self.db_path, backup_path)
            logger.info(f"Backup criado: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Erro no backup: {e}")
            return None