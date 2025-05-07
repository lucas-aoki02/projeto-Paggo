from backend.models.fonte import Data   
from backend.models.alvo import Signal
from datetime import datetime
from backend.database import FonteSessionLocal, AlvoSessionLocal
from sqlalchemy import select
from sqlalchemy.sql.expression import column

# Consulta no banco Fonte
def get_data_by_date(start_date: datetime, end_date: datetime, variables: list):
    session = FonteSessionLocal()
    try:
        query = select(Data).where(Data.timestamp >= start_date, Data.timestamp <= end_date)

        if variables:
            selected_columns = [column(var) for var in variables if hasattr(Data, var)]
            if selected_columns:
                query = select(*selected_columns).where(Data.timestamp >= start_date, Data.timestamp <= end_date)
            else:
                print("Aviso: Nenhuma das variáveis solicitadas existe no modelo Data.")
                return []

        compiled_query = query.compile(compile_kwargs={'literal_binds': True})
        print(f"Consulta SQL (get_data_by_date): {str(compiled_query)}")
        results = session.execute(query).all()

        print(f"Primeiros resultados da consulta: {results[:5]}")

        results_list = []
        if selected_columns:
            for row in results:
                record = dict(zip(variables, row))
                results_list.append(record)
        else:
            for row in results:
                record = {
                    "timestamp": row.timestamp,
                    "wind_speed": row.wind_speed if hasattr(row, "wind_speed") else None,
                    "power": row.power if hasattr(row, "power") else None,
                    "ambient_temperature": row.ambient_temperature if hasattr(row, "ambient_temperature") else None,
                }
                results_list.append(record)

        return results_list
    finally:
        session.close()

# Inserção no banco Alvo
def insert_signals(signal_data: list):
    session = AlvoSessionLocal()
    try:
        signals_to_insert = [
            Signal(
                name=entry["name"],
                timestamp=entry["timestamp"],
                signal_id=entry["signal_id"],
                value=entry["value"]
            )
            for entry in signal_data
        ]
        session.add_all(signals_to_insert)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()