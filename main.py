from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from reportlab.pdfgen import canvas
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from data_handler import DataHandler
from kivy.uix.floatlayout import FloatLayout  
from kivy.uix.spinner import Spinner 

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        layout = FloatLayout()
        
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Fondo blanco
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Blanco
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)
        
        image = Image(source= 'C:/Users/Owner-1/Monica_Portable_version/logo (1).png',  # Cambia el nombre de la imagen
                      size_hint=(None, None), size=(130, 10),  # Ajusta el tamaño según sea necesario
                      pos_hint={'x': 0.1, 'top': 1})  
        self.layout.add_widget(image)

        # Dibujar rectángulo azul en la parte superior
        with self.canvas:
            Color(0.53, 0.81, .92, 1)  # Azul
            self.header_rect = Rectangle(size=(self.width, 70), pos=(0.5, self.height - 100))  # Ajusta según el tamaño
        self.bind(size=self.update_header_rect, pos=self.update_header_rect)
        
        

        # Layout para el botón "Seleccionar cuenta"
        self.account_label = Label(text='', color=(1, 1, 1, 1), size_hint=(None, None),
                                   size=(200, 50), pos_hint={'x': 0.3, 'top': 0.9})
        self.account_spinner = Spinner(text='Seleccionar Cuenta', values=[],
                                       size_hint=(None, None), size=(150, 40), pos_hint={'x': 0.6, 'top': 0.99},
                                       background_color=(0, 0, 1, 1),  # Fondo azul
                                       color=(1, 1, 1, 1))  # Texto blanco
        self.account_spinner.bind(text=self.select_account)

        layout.add_widget(self.account_label)
        layout.add_widget(self.account_spinner)
        

        # Botones en pareja (más arriba)
        add_client_btn = Button(text='', size_hint=(None, None), width=150, height=200,
                                background_color=(1, 1, 1, 1), pos_hint={'center_x': 0.25, 'center_y': 0.6},
                                color=(1, 1, 1, 1))  # Blanco
        add_client_btn.bind(on_press=self.go_to_add_clients)
        add_client_btn.background_normal = 'C:/Users/Owner-1/Monica_Portable_version/Clientes.png'

        estimates_btn = Button(text='', size_hint=(None, None), width=150, height=200,
                               background_color=(1, 1, 1, 1), pos_hint={'center_x': 0.75, 'center_y': 0.6},
                               color=(1, 1, 1, 1))  # Blanco
        estimates_btn.bind(on_press=self.go_to_estimates)
        estimates_btn.background_normal = 'C:/Users/Owner-1/Monica_Portable_version/estimados.png'

        layout.add_widget(add_client_btn)
        layout.add_widget(estimates_btn)

        # Botones en pareja (más abajo)
        inventory_btn = Button(text='', size_hint=(None, None), width=150, height=200,
                               background_color=(1, 1, 1, 1), pos_hint={'center_x': 0.25, 'center_y': 0.2},
                               color=(1, 1, 1, 1))  # Blanco
        inventory_btn.bind(on_press=self.go_to_inventory)
        inventory_btn.background_normal = 'C:/Users/Owner-1/Monica_Portable_version/inventario.png'

        account_manager_btn = Button(text='', size_hint=(None, None), width=210, height=200,
                                     background_color=(1, 1, 1, 1), pos_hint={'center_x': 0.75, 'center_y': 0.2},
                                     color=(1, 1, 1, 1))  # Blanco
        account_manager_btn.bind(on_press=self.open_account_manager_popup)
        account_manager_btn.background_normal = 'C:/Users/Owner-1/Monica_Portable_version/Empresas.png'

        layout.add_widget(inventory_btn)
        layout.add_widget(account_manager_btn)

        # Añadir el layout al widget principal
        self.add_widget(layout)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def update_header_rect(self, *args):
        # Mantener el rectángulo azul en la parte superior
        self.header_rect.size = (self.width, 50)
        self.header_rect.pos = (0, self.height - 50)

    def on_pre_enter(self):
        DataHandler.load_data()  # Asegúrate de que esta función cargue los datos correctamente
        self.update_account_spinner()  # Actualiza el spinner con las cuentas disponibles

    def update_account_spinner(self):
        accounts = DataHandler.get_accounts()  # Obtén la lista de nombres de cuentas
        print("Actualizando spinner con:", accounts)  # Agrega esta línea para depuración
        self.account_spinner.values = accounts  # Actualiza los valores del Spinner

    def select_account(self, spinner, text):
        # Actualiza la etiqueta y maneja la selección de cuenta
        self.account_label.text = f"Cuenta seleccionada: {text}"
        DataHandler.current_account = text

    def go_to_add_clients(self, instance):
        self.manager.current = 'add_clients'

    def go_to_estimates(self, instance):
        self.manager.current = 'estimates'

    def go_to_inventory(self, instance):
        self.manager.current = 'inventory'

    def open_account_manager_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10)
        account_name_input = TextInput(hint_text='Nombre de la nueva cuenta', size_hint_y=None, height=40)
        content.add_widget(account_name_input)

        add_account_btn = Button(text='Añadir Cuenta', size_hint_y=None, height=40)
        add_account_btn.bind(on_press=lambda x: self.add_account(account_name_input.text))
        content.add_widget(add_account_btn)

        delete_account_btn = Button(text='Eliminar Cuenta', size_hint_y=None, height=40)
        delete_account_btn.bind(on_press=self.delete_account)
        content.add_widget(delete_account_btn)

        self.popup = Popup(title='Gestor de Cuentas', content=content, size_hint=(0.8, 0.4))
        self.popup.open()

    def add_account(self, account_name):
        if account_name:
            DataHandler.add_account(account_name)
            self.update_account_spinner()  # Actualiza el spinner con la nueva lista de cuentas
            self.popup.dismiss()

    def delete_account(self, instance):
        account_list = DataHandler.get_account_list()
        if account_list:
            account_to_delete = account_list[0]
            DataHandler.delete_account(account_to_delete)
            self.update_account_spinner()  # Actualiza el spinner con la lista de cuentas actualizada
            self.account_label.text = ''

class EstimatesScreen(Screen):
    def __init__(self, **kwargs):
        super(EstimatesScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.estimate_list_label = Label(text='Lista de Estimados:')
        self.estimates_grid = GridLayout(cols=7, size_hint_y=None)
        self.estimates_grid.bind(minimum_height=self.estimates_grid.setter('height'))
        self.selected_estimates = []
        self.inputs = None
        self.clients_grid = None

        self.update_estimate_list()

        remove_selected_btn = Button(text='Eliminar Seleccionado', size_hint_y=None, height=40)
        remove_selected_btn.bind(on_press=self.remove_selected_items)

        add_item_btn = Button(text='Añadir Estimado', size_hint_y=None, height=40)
        add_item_btn.bind(on_press=self.show_add_item_popup)

        generate_pdf_btn = Button(text='Generar PDF', size_hint_y=None, height=40)
        generate_pdf_btn.bind(on_press=self.generate_pdf)

        back_btn = Button(text='Regresar al Menú Principal')
        back_btn.bind(on_press=self.go_back)

        scroll_view_estimates = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True,
                                           bar_width=10, scroll_type=['bars', 'content'])
        scroll_view_estimates.add_widget(self.estimates_grid)

        layout.add_widget(self.estimate_list_label)
        layout.add_widget(scroll_view_estimates)
        layout.add_widget(remove_selected_btn)
        layout.add_widget(add_item_btn)
        layout.add_widget(generate_pdf_btn)
        layout.add_widget(back_btn)
        self.add_widget(layout)



    def on_enter(self):
        """Actualiza la lista de estimados al entrar en la pantalla."""
        self.update_estimate_list()

    def truncate_text(self, text, length=10):
        """Trunca el texto a una longitud máxima, añadiendo puntos suspensivos si es necesario."""
        if len(text) > length:
            return text[:length - 3] + '...'
        return text

    def on_code_input_clients_change(self, instance, value):
        self.clients_grid.clear_widgets()

        client_headers = ['Codigo', 'Nombre', 'Repr', 'Telefono', 'Correo', 'RFC']
        for header in client_headers:
            self.clients_grid.add_widget(Label(text=header, bold=True))

        clients = DataHandler.get_clients()
        for client in clients:
            if client[0] == value:
                for detail in client:
                    truncated_detail = self.truncate_text(detail, length=10)
                    self.clients_grid.add_widget(Label(text=truncated_detail))

    def on_code_input_inventory_change(self, instance, value):
        self.inventory_grid.clear_widgets()

        inventory_headers = ['Codigo', 'Descripcion', 'Precio', 'Tipo']
        for header in inventory_headers:
            self.inventory_grid.add_widget(Label(text=header, bold=True))

        codes = [code.strip() for code in value.split(',') if code.strip()]

        inventory = DataHandler.get_inventory()

        self.total_price = 0.0

        for code in codes:
            for item in inventory:
                if item[0] == code:
                    for i, detail in enumerate(item):
                        if i in [0, 1, 2, 3]:
                            truncated_detail = self.truncate_text(detail, length=10)
                            self.inventory_grid.add_widget(Label(text=truncated_detail))

                        if i == 2:
                            try:
                                self.total_price += float(detail)
                            except ValueError:
                                pass

        self.update_total_price_label()

    def update_total_price_label(self):
        try:
            discount = float(self.inputs['Descuento'].text) / 100
        except ValueError:
            discount = 0.0

        discounted_total = self.total_price * (1 - discount)
        self.total_price_label.text = f"Total con Descuento: {discounted_total:.2f}"

    def update_estimate_list(self):
        self.estimates_grid.clear_widgets()

        headers = ['Seleccionar', 'Descripcion', 'Descuento', 'Fecha', 'Estado']

        self.estimates_grid.cols = len(headers)

        for header in headers:
            label = Label(text=header, bold=True, size_hint_x=None, width=100)
            self.estimates_grid.add_widget(label)

        estimates = DataHandler.get_estimates()
        self.selected_estimates = []

        for estimate in estimates:
            checkbox = CheckBox(size_hint_x=None, width=40)
            self.selected_estimates.append(checkbox)
            self.estimates_grid.add_widget(checkbox)

            for detail in estimate:
                label = Label(text=detail, size_hint_x=None, width=100)
                self.estimates_grid.add_widget(label)

    def remove_selected_items(self, instance):
        estimates = DataHandler.get_estimates()
        new_estimates = [estimate for i, estimate in enumerate(estimates) if
                         i >= len(self.selected_estimates) or not self.selected_estimates[i].active]
        DataHandler.accounts_data[DataHandler.current_account]['estimates'] = new_estimates
        DataHandler.save_data()
        self.update_estimate_list()

    

    def generate_pdf(self, instance):
        filename = "estimados.pdf"
        pdf_canvas = canvas.Canvas(filename)

        x_position = 100
        y_position = 800

        pdf_canvas.drawString(x_position, y_position, "Detalle del Estimado Seleccionado")
        y_position -= 30

        estimates = DataHandler.get_estimates()
        total_price = 0.0

        print("Estimados disponibles:", estimates)

        for i, checkbox in enumerate(self.selected_estimates):
            if checkbox.active:
                if i < len(estimates):
                    estimate = estimates[i]
                    estimate = estimate + ('N/A',) * (5 - len(estimate))

                    if len(estimate) >= 5:
                        description = estimate[1] if len(estimate) > 1 else 'N/A'
                        discount = estimate[2] if len(estimate) > 2 else '0'
                        date = estimate[3] if len(estimate) > 3 else 'N/A'
                        status = estimate[4] if len(estimate) > 4 else 'N/A'

                        print(f"Procesando estimado {i}: {estimate}")

                        details = [
                            f"Descripcion: {description}",
                            f"Descuento: {discount}",
                            f"Fecha: {date}",
                            f"Estado: {status}"
                        ]
                        for detail in details:
                            pdf_canvas.drawString(x_position, y_position, detail)
                            y_position -= 20

                        try:
                            total_price += float(discount)
                        except ValueError:
                            total_price += 0.0

                        break
                else:
                    print(f"Índice {i} fuera de rango para los estimados.")

        discount_rate = 0.0
        discounted_total = total_price * (1 - discount_rate)

        extra_details = [
            f"Total con Descuento: {discounted_total:.2f}",
        ]
        for detail in extra_details:
            pdf_canvas.drawString(x_position, y_position, detail)
            y_position -= 20

        pdf_canvas.save()

        success_popup = Popup(title='PDF Generado', content=Label(text=f'PDF guardado como {filename}.'),
                              size_hint=(0.5, 0.5))
        success_popup.open()

    def show_add_item_popup(self, instance):
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        header_layout.add_widget(Widget())
        account_name_label = Label(text=f'Nombre de la cuenta: {DataHandler.current_account}', size_hint_x=None,
                                   width=200)
        header_layout.add_widget(account_name_label)

        client_section = BoxLayout(orientation='vertical', size_hint_y=None, height=200, spacing=10)
        client_code_label = Label(text='Codigo Cliente', size_hint_y=None, height=20)
        client_code_input = TextInput(hint_text='Codigo Cliente', size_hint_y=None, height=40)
        client_code_input.bind(text=self.on_code_input_clients_change)

        self.clients_grid = GridLayout(cols=6, size_hint_y=None)
        self.clients_grid.bind(minimum_height=self.clients_grid.setter('height'))
        scroll_view_clients = ScrollView(size_hint=(1.1, 1), do_scroll_x=False, do_scroll_y=True, bar_width=15,
                                         scroll_type=['bars', 'content'])
        scroll_view_clients.add_widget(self.clients_grid)

        client_section.add_widget(client_code_label)
        client_section.add_widget(client_code_input)
        client_section.add_widget(scroll_view_clients)

        inventory_section = BoxLayout(orientation='vertical', size_hint_y=None, height=200, spacing=10)
        inventory_code_label = Label(text='Codigo Inventario', size_hint_y=None, height=20)
        inventory_code_input = TextInput(hint_text='Codigo Inventario', size_hint_y=None, height=40)
        inventory_code_input.bind(text=self.on_code_input_inventory_change)

        self.inventory_grid = GridLayout(cols=4, size_hint_y=None)
        self.inventory_grid.bind(minimum_height=self.inventory_grid.setter('height'))
        scroll_view_inventory = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True, bar_width=10,
                                           scroll_type=['bars', 'content'])
        scroll_view_inventory.add_widget(self.inventory_grid)

        inventory_section.add_widget(inventory_code_label)
        inventory_section.add_widget(inventory_code_input)
        inventory_section.add_widget(scroll_view_inventory)

        main_section = BoxLayout(orientation='horizontal', spacing=10)

        client_inventory_section = BoxLayout(orientation='vertical', spacing=20, size_hint=(0.6, 0.6))
        client_inventory_section.add_widget(client_section)
        client_inventory_section.add_widget(inventory_section)

        inputs_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(0.4, 1))
        self.inputs = {
            'Descripcion': TextInput(hint_text='Descripcion', size_hint_y=None, height=40),
            'Descuento': TextInput(hint_text='Descuento (%)', size_hint_y=None, height=40),
            'Fecha': TextInput(hint_text='Fecha', size_hint_y=None, height=40),
            'Estado': TextInput(hint_text='Estado', size_hint_y=None, height=40),
        }

        self.total_price_label = Label(text='Total con Descuento: 0.00', size_hint_y=None, height=40)
        inputs_layout.add_widget(self.total_price_label)

        for key, input_widget in self.inputs.items():
            if key != 'Cliente':
                inputs_layout.add_widget(input_widget)

        apply_discount_button = Button(text='Aplicar Descuento', size_hint_y=None, height=40)
        apply_discount_button.bind(on_press=self.apply_discount)
        inputs_layout.add_widget(apply_discount_button)

        main_section.add_widget(client_inventory_section)
        main_section.add_widget(inputs_layout)

        buttons_layout = BoxLayout(size_hint_y=None, height=40)
        add_button = Button(text='Añadir')
        add_button.bind(on_press=self.add_item_from_popup)
        cancel_button = Button(text='Cancelar')
        cancel_button.bind(on_press=self.close_popup)
        buttons_layout.add_widget(add_button)
        buttons_layout.add_widget(cancel_button)

        popup_layout.add_widget(header_layout)
        popup_layout.add_widget(main_section)
        popup_layout.add_widget(buttons_layout)

        self.popup = Popup(title='Añadir Nuevo Estimado', content=popup_layout, size_hint=(0.95, 0.95))
        self.popup.open()

    def add_item_from_popup(self, instance):
        new_item = tuple(input_widget.text for input_widget in self.inputs.values())
        if any(field.strip() == '' for field in new_item):
            self.show_error_popup("Todos los campos deben estar llenos.")
            return

        DataHandler.add_estimate(new_item)
        self.update_estimate_list()
        self.popup.dismiss()

    def apply_discount(self, instance):
        """Aplica el descuento y actualiza el total mostrado."""
        try:
            discount = float(self.inputs['Descuento'].text) / 100
        except ValueError:
            discount = 0.0

        discounted_total = self.total_price * (1 - discount)
        self.total_price_label.text = f"Total con Descuento: {discounted_total:.2f}"

    def close_popup(self, instance):
        self.popup.dismiss()

    def show_error_popup(self, message):
        content = BoxLayout(orientation='vertical')
        error_label = Label(text=message, size_hint_y=None, height=40)
        ok_button = Button(text='OK', size_hint_y=None, height=40)
        ok_button.bind(on_press=lambda x: self.error_popup.dismiss())
        content.add_widget(error_label)
        content.add_widget(ok_button)
        self.error_popup = Popup(title='Error', content=content, size_hint=(0.6, 0.4))
        self.error_popup.open()

    def go_back(self, instance):
        self.manager.current = 'main_menu'

class AddClientsScreen(Screen):
    def __init__(self, **kwargs):
        super(AddClientsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.client_list_label = Label(text='Lista de Clientes:')
        self.clients_grid = GridLayout(cols=7, size_hint_y=None)
        self.clients_grid.bind(minimum_height=self.clients_grid.setter('height'))
        self.selected_clients = []
        self.update_client_list()

        self.inventory_list_label = Label(text='', size_hint_y=None, height=30)
        self.inventory_grid = GridLayout(cols=7, size_hint_y=None)
        self.inventory_grid.bind(minimum_height=self.inventory_grid.setter('height'))
        self.selected_inventory_items = []

        remove_selected_btn = Button(text='Eliminar Seleccionado', size_hint_y=None, height=40)
        remove_selected_btn.bind(on_press=self.remove_selected_items)

        add_item_btn = Button(text='Añadir Clientes', size_hint_y=None, height=40)
        add_item_btn.bind(on_press=self.show_add_item_popup)

        send_to_server_btn = Button(text='Enviar a Servidor', size_hint_y=None, height=40)
        send_to_server_btn.bind(on_press=self.send_clients_to_server)  # Añadido aquí

        back_btn = Button(text='Regresar al Menú Principal')
        back_btn.bind(on_press=self.go_back)

        scroll_view_clients = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True,
                                         bar_width=10, scroll_type=['bars', 'content'])
        scroll_view_clients.add_widget(self.clients_grid)

        scroll_view_inventory = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True,
                                           bar_width=10, scroll_type=['bars', 'content'])
        scroll_view_inventory.add_widget(self.inventory_grid)

        layout.add_widget(self.client_list_label)
        layout.add_widget(scroll_view_clients)
        layout.add_widget(self.inventory_list_label)
        layout.add_widget(scroll_view_inventory)
        layout.add_widget(remove_selected_btn)
        layout.add_widget(add_item_btn)
        layout.add_widget(send_to_server_btn)  # Añadido aquí
        layout.add_widget(back_btn)
        self.add_widget(layout)

    def update_client_list(self):
        self.clients_grid.clear_widgets()
        clients = DataHandler.get_clients()
        self.selected_clients = []

        headers = ['Seleccionar', 'Codigo', 'Nombre', 'Representante', 'Telefono', 'Correo', 'RFC']
        for header in headers:
            self.clients_grid.add_widget(Label(text=header, bold=True))

        for client in clients:
            checkbox = CheckBox(size_hint_x=None, width=40)
            self.selected_clients.append(checkbox)
            self.clients_grid.add_widget(checkbox)
            for detail in client:
                self.clients_grid.add_widget(Label(text=detail))

    def update_inventory_list(self):
        self.inventory_grid.clear_widgets()
        inventory = DataHandler.get_inventory()
        self.selected_inventory_items = []

        headers = ['Seleccionar', 'Codigo', 'Descripcion', 'Precio', 'Tipo', 'Unidades', 'Media']
        for header in headers:
            self.inventory_grid.add_widget(Label(text=header, bold=True))

        for item in inventory:
            checkbox = CheckBox(size_hint_x=None, width=40)
            self.selected_inventory_items.append(checkbox)
            self.inventory_grid.add_widget(checkbox)
            for detail in item:
                self.inventory_grid.add_widget(Label(text=detail))

    def remove_selected_items(self, instance):
        clients = DataHandler.get_clients()
        new_clients = [client for i, client in enumerate(clients) if
                       i >= len(self.selected_clients) or not self.selected_clients[i].active]
        DataHandler.accounts_data[DataHandler.current_account]['clients'] = new_clients
        DataHandler.save_data()
        self.update_client_list()

    def add_client(self, instance):
        new_client = ("Nuevo", "Cliente", "", "", "", "")
        DataHandler.add_client(new_client)
        self.update_client_list()

    def show_add_item_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        self.inputs = {
            'Codigo': TextInput(hint_text='Codigo', size_hint_y=None, height=40),
            'Nombre': TextInput(hint_text='Nombre', size_hint_y=None, height=40),
            'Representante': TextInput(hint_text='Representante', size_hint_y=None, height=40),
            'Telefono': TextInput(hint_text='Telefono', size_hint_y=None, height=40),
            'Correo': TextInput(hint_text='Correo', size_hint_y=None, height=40),
            'RFC': TextInput(hint_text='RFC', size_hint_y=None, height=40),
        }

        for header, input_widget in self.inputs.items():
            content.add_widget(input_widget)

        add_button = Button(text='Añadir', size_hint_y=None, height=40)
        add_button.bind(on_press=self.add_item_from_popup)
        content.add_widget(add_button)

        cancel_button = Button(text='Cancelar', size_hint_y=None, height=40)
        cancel_button.bind(on_press=self.close_popup)
        content.add_widget(cancel_button)

        self.popup = Popup(title='Añadir Nuevo Cliente', content=content, size_hint=(0.8, 0.8))
        self.popup.open()

    def add_item_from_popup(self, instance):
        new_item = tuple(input_widget.text for input_widget in self.inputs.values())
        if any(field.strip() == '' for field in new_item):
            self.show_error_popup("Todos los campos deben estar llenos.")
            return

        DataHandler.add_client(new_item)
        self.update_client_list()
        self.popup.dismiss()

    def close_popup(self, instance):
        self.popup.dismiss()

    def show_error_popup(self, message):
        content = BoxLayout(orientation='vertical')
        error_label = Label(text=message, size_hint_y=None, height=40)
        ok_button = Button(text='OK', size_hint_y=None, height=40)
        ok_button.bind(on_press=lambda x: self.error_popup.dismiss())
        content.add_widget(error_label)
        content.add_widget(ok_button)
        self.error_popup = Popup(title='Error', content=content, size_hint=(0.6, 0.4))
        self.error_popup.open()

    def send_clients_to_server(self, instance):
        """Envía la lista de clientes al servidor SQL."""
        DataHandler.save_clients_to_sql()  # Llama al método para enviar los clientes

    def on_enter(self, *args):
        self.update_client_list()

    def go_back(self, instance):
        self.manager.current = 'main_menu'


class InventoryScreen(Screen):
    def __init__(self, **kwargs):
        super(InventoryScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.inventory_list_label = Label(text='Lista de Inventario:')
        self.inventory_grid = GridLayout(cols=4, size_hint_y=None)
        self.inventory_grid.bind(minimum_height=self.inventory_grid.setter('height'))

        scroll_view_inventory = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True,
                                           bar_width=10, scroll_type=['bars', 'content'])
        scroll_view_inventory.add_widget(self.inventory_grid)

        layout.add_widget(self.inventory_list_label)
        layout.add_widget(scroll_view_inventory)

        add_item_btn = Button(text='Añadir Item', size_hint_y=None, height=40)
        add_item_btn.bind(on_press=self.show_add_item_popup)
        layout.add_widget(add_item_btn)

        delete_item_btn = Button(text='Eliminar Item', size_hint_y=None, height=40)
        delete_item_btn.bind(on_press=self.delete_selected_item)
        layout.add_widget(delete_item_btn)

        back_btn = Button(text='Regresar al Menú Principal', size_hint_y=None, height=40)
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

        self.load_inventory()

    def load_inventory(self):
        self.inventory_grid.clear_widgets()
        headers = ['Código', 'Descripción', 'Precio', 'Tipo']
        for header in headers:
            label = Label(text=header, bold=True, size_hint_x=None, width=100)
            self.inventory_grid.add_widget(label)

        items = DataHandler.get_inventory()
        for item in items:
            for field in item:
                label = Label(text=str(field), size_hint_x=None, width=100)
                self.inventory_grid.add_widget(label)

    def show_add_item_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10)
        self.inputs = {}
        fields = ['Código', 'Descripción', 'Precio', 'Tipo']

        for field in fields:
            box = BoxLayout(orientation='horizontal')
            label = Label(text=field, size_hint_x=None, width=100)
            input_field = TextInput(size_hint_x=None, width=200)
            self.inputs[field] = input_field
            box.add_widget(label)
            box.add_widget(input_field)
            content.add_widget(box)

        submit_button = Button(text='Añadir', size_hint_y=None, height=40)
        submit_button.bind(on_press=self.add_item)
        content.add_widget(submit_button)

        self.popup = Popup(title='Añadir Item', content=content, size_hint=(0.8, 0.6))
        self.popup.open()

    def add_item(self, instance):
        item_data = [self.inputs[field].text for field in ['Código', 'Descripción', 'Precio', 'Tipo']]
        inventory = DataHandler.get_inventory()
        inventory.append(item_data)
        DataHandler.accounts_data[DataHandler.current_account]['inventory'] = inventory
        DataHandler.save_data()
        self.load_inventory()
        self.popup.dismiss()

    def delete_selected_item(self, instance):
        # Implementar lógica para eliminar un ítem seleccionado
        pass

    def go_back(self, instance):
        self.manager.current = 'main_menu'




class AddClientsScreen(Screen):
    def __init__(self, **kwargs):
        super(AddClientsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.client_list_label = Label(text='Lista de Clientes:')
        self.clients_grid = GridLayout(cols=7, size_hint_y=None)
        self.clients_grid.bind(minimum_height=self.clients_grid.setter('height'))
        self.selected_clients = []

        scroll_view_clients = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True,
                                         bar_width=10, scroll_type=['bars', 'content'])
        scroll_view_clients.add_widget(self.clients_grid)

        layout.add_widget(self.client_list_label)
        layout.add_widget(scroll_view_clients)

        add_client_btn = Button(text='Añadir Cliente', size_hint_y=None, height=40)
        add_client_btn.bind(on_press=self.show_add_client_popup)
        layout.add_widget(add_client_btn)

        # Botón "Enviar al Servidor" modificado
        send_to_server_btn = Button(text='Enviar Clientes al Servidor', size_hint_y=None, height=40)
        send_to_server_btn.bind(on_press=self.confirm_send_clients_to_server)
        layout.add_widget(send_to_server_btn)

        back_btn = Button(text='Regresar al Menú Principal')
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def show_add_client_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        self.inputs = {}
        fields = ['Codigo', 'Nombre', 'Representante', 'Telefono', 'Correo', 'RFC']

        for field in fields:
            box = BoxLayout(orientation='horizontal')
            label = Label(text=field, size_hint_x=None, width=100)
            input_field = TextInput(size_hint_x=None, width=200)
            self.inputs[field] = input_field
            box.add_widget(label)
            box.add_widget(input_field)
            content.add_widget(box)

        submit_button = Button(text='Añadir', size_hint_y=None, height=40)
        submit_button.bind(on_press=self.add_client)
        content.add_widget(submit_button)

        self.popup = Popup(title='Añadir Cliente', content=content, size_hint=(None, None), size=(400, 300))
        self.popup.open()

    def truncate_text(self, text, length=10):
        if len(text) > length:
            return text[:length] + '...'
        return text    

    def add_client(self, instance):
        client_data = [self.inputs[field].text for field in ['Codigo', 'Nombre', 'Representante', 'Telefono', 'Correo', 'RFC']]
        clients = DataHandler.get_clients()
        clients.append(client_data)
        DataHandler.accounts_data[DataHandler.current_account]['clients'] = clients
        DataHandler.save_data()
        self.update_client_list()
        self.popup.dismiss()

    def update_client_list(self):
        self.clients_grid.clear_widgets()

        headers = ['Seleccionar', 'Codigo', 'Nombre', 'Representante', 'Telefono', 'Correo', 'RFC']

        for header in headers:
            label = Label(text=header, bold=True)
            self.clients_grid.add_widget(label)

        clients = DataHandler.get_clients()

        for client in clients:
            checkbox = CheckBox(size_hint_x=None, width=40)
            self.selected_clients.append(checkbox)
            self.clients_grid.add_widget(checkbox)
            for detail in client:
                self.clients_grid.add_widget(Label(text=self.truncate_text(detail, length=10)))

    def confirm_send_clients_to_server(self, instance):
        # Método para confirmar antes de enviar los clientes al servidor
        content = BoxLayout(orientation='vertical')

        message = Label(text='¿Está seguro de que desea enviar los clientes al servidor?')
        content.add_widget(message)

        button_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)

        confirm_button = Button(text='Confirmar')
        confirm_button.bind(on_press=lambda x: self.send_clients_to_server(confirm_popup))

        cancel_button = Button(text='Cancelar')
        cancel_button.bind(on_press=lambda x: confirm_popup.dismiss())

        button_box.add_widget(confirm_button)
        button_box.add_widget(cancel_button)

        content.add_widget(button_box)

        confirm_popup = Popup(
            title='Confirmar Envío',
            content=content,
            size_hint=(None, None), size=(400, 200),
            auto_dismiss=False
        )

        confirm_popup.open()

    def send_clients_to_server(self, instance):
        DataHandler.save_clients_to_sql()  # Asegúrate de que este método esté definido en DataHandler

    def go_back(self, instance):
        self.manager.current = 'main_menu'




class TestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(AddClientsScreen(name='add_clients'))
        sm.add_widget(InventoryScreen(name='inventory'))
        sm.add_widget(EstimatesScreen(name='estimates'))
        return sm

if __name__ == '__main__':
    TestApp().run()



