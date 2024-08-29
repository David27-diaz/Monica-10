import os
import pickle
import pyodbc

class DataHandler:
    data_file = 'accounts_data.pkl'
    current_account = None
    accounts_data = {}

    @classmethod
    def get_accounts(cls):
        cls.load_data()
        accounts = list(cls.accounts_data.keys())
        print(f"Cuentas disponibles: {accounts}")
        return accounts

    @staticmethod
    def set_current_account(account_name):
        DataHandler.current_account = account_name
        print(f"Cuenta actual establecida a: {account_name}")

    @classmethod
    def load_data(cls):
        if os.path.exists(cls.data_file):
            with open(cls.data_file, 'rb') as f:
                cls.accounts_data = pickle.load(f)
            print(f"Datos cargados: {cls.accounts_data}")

    @classmethod
    def save_data(cls):
        with open(cls.data_file, 'wb') as f:
            pickle.dump(cls.accounts_data, f)
        print("Datos guardados con éxito.")

    @classmethod
    def add_account(cls, account_name):
        if account_name not in cls.accounts_data:
            cls.accounts_data[account_name] = {
                'clients': [],
                'inventory': [],
                'estimates': []
            }
        cls.save_data()

    @classmethod
    def get_clients(cls):
        if cls.current_account:
            return cls.accounts_data[cls.current_account]['clients']
        return []

    @classmethod
    def add_client(cls, client_data):
        if cls.current_account:
            cls.accounts_data[cls.current_account]['clients'].append(client_data)
        cls.save_data()

    @classmethod
    def get_inventory(cls):
        if cls.current_account:
            return cls.accounts_data[cls.current_account]['inventory']
        return []

    @classmethod
    def delete_account(cls, account_name):
        if account_name in cls.accounts_data:
            del cls.accounts_data[account_name]
            cls.save_data()

    @classmethod
    def add_inventory_item(cls, code, description, price, item_type):
        if cls.current_account:
            item_data = {
                'code': code,
                'description': description,
                'price': price,
                'item_type': item_type
            }
            cls.accounts_data[cls.current_account]['inventory'].append(item_data)
        cls.save_data()

    @classmethod
    def get_estimates(cls):
        if cls.current_account:
            return cls.accounts_data[cls.current_account].get('estimates', [])
        return []

    @classmethod
    def add_estimate(cls, estimate_data):
        if cls.current_account:
            if 'estimates' not in cls.accounts_data[cls.current_account]:
                cls.accounts_data[cls.current_account]['estimates'] = []
            cls.accounts_data[cls.current_account]['estimates'].append(estimate_data)
        cls.save_data()

    @classmethod
    def save_clients_to_sql(cls):
        if cls.current_account:
            conn = None
            try:
                # Conectar a la base de datos de SQL Server
                conn_str = (
                    r'DRIVER={SQL Server};'
                    r'SERVER=IP_Client,Port_Client;'
                    r'DATABASE=monica11_2;'
                    r'UID=sa;'
                    r'PWD=Admin2023;'
                )
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()

                # Obtener los datos de clientes
                clients = cls.get_clients()

                for client in clients:
                    if len(client) == 6:
                        cliente_id, nombre_clte, direccion1, telefono1, e_mail1, ciudad = client

                        # Verificar si el cliente ya existe en la base de datos
                        cursor.execute(
                            "SELECT COUNT(*) FROM clientes WHERE cliente_id = ?", 
                            (cliente_id,)
                        )
                        exists = cursor.fetchone()[0] > 0

                        if exists:
                            # Actualizar datos del cliente existente
                            cursor.execute(
                                """
                                UPDATE clientes
                                SET nombre_clte = ?, direccion1 = ?, telefono1 = ?, e_mail1 = ?, ciudad = ?
                                WHERE cliente_id = ?
                                """,
                                (nombre_clte, direccion1, telefono1, e_mail1, ciudad, cliente_id)
                            )
                        else:
                            # Insertar nuevo cliente
                            cursor.execute(
                                """
                                INSERT INTO clientes(
                                    codigo_clte, nombre_clte, direccion1, direccion2, direccion3, ciudad, 
                                    Provincia, pais, Codigo_postal, telefono1, telefono2, fax, Contacto, e_mail1, 
                                    e_mail2, registro_empresarial, registro_tributario, cuenta_cont_ventas, giro_id, 
                                    comentario, campo1, campo2, campo3, imagen, reten_ica, reten_fuente, segundo_impto, 
                                    primer_apellido, segundo_apellido, primer_nombre, segundo_nombre, monto_ult_transac, 
                                    usuario, reten_cree, resptrib
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """,
                                (
                                    '', nombre_clte, direccion1, '', '', ciudad, '', '', '', telefono1, '', '', '', 
                                    e_mail1, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 
                                    '', '', '', '', ''
                                )
                            )

                # Confirmar los cambios
                conn.commit()
                print("Clientes guardados en la base de datos con éxito.")
            except Exception as e:
                print(f"Error al guardar clientes en SQL: {e}")
            finally:
                if conn:
                    conn.close()
