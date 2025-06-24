import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime
from decimal import Decimal

class StoreManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Store Management System - Stormanag 2.0")
        self.root.geometry("1000x750")
        self.root.configure(bg="#f0f0f0")
        
        # Database connection
        self.db = self.create_db_connection()
        if self.db is None:
            messagebox.showerror("Error", "Failed to connect to database. Application will exit.")
            self.root.destroy()
            return
            
        self.cursor = self.db.cursor()
        self.initialize_tables()
        
        # Styling
        self.label_font = ('Arial', 10)
        self.entry_font = ('Arial', 10)
        self.button_font = ('Arial', 10, 'bold')
        self.title_font = ('Arial', 12, 'bold')
        
        # Create UI
        self.create_ui()
        
        # Initialize data
        self.load_products()
        self.load_customers()
        self.load_sellers()
        self.load_sale_products()
        
        # Sale items list
        self.sale_items = []
        
        # Set up closing handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_db_connection(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456789",
                database="store_management",
                port=3306,
                ssl_disabled=True,
                use_pure=True
            )
            if connection.is_connected():
                db_info = connection.get_server_info()
                print(f"Successfully connected to MySQL Server version {db_info}")
            return connection
        except mysql.connector.Error as err:
            print(f"Connection error: {err}")
            messagebox.showerror("Database Error", f"Error connecting to MySQL: {err}")
            return None

    def initialize_tables(self):
        try:
            tables = [
                """CREATE TABLE IF NOT EXISTS Sellers (
                    seller_id INT AUTO_INCREMENT PRIMARY KEY,
                    seller_name VARCHAR(100) NOT NULL,
                    contact_number VARCHAR(15) NOT NULL,
                    email VARCHAR(100),
                    UNIQUE KEY unique_seller (seller_name, contact_number)
                )""",
                """CREATE TABLE IF NOT EXISTS Customers (
                    customer_id INT AUTO_INCREMENT PRIMARY KEY,
                    customer_name VARCHAR(100) NOT NULL,
                    contact_number VARCHAR(15) NOT NULL,
                    email VARCHAR(100),
                    UNIQUE KEY unique_customer (customer_name, contact_number)
                )""",
                """CREATE TABLE IF NOT EXISTS Products (
                    product_id INT AUTO_INCREMENT PRIMARY KEY,
                    product_name VARCHAR(100) NOT NULL,
                    description TEXT,
                    price DECIMAL(10, 2) NOT NULL,
                    category VARCHAR(50),
                    UNIQUE KEY unique_product (product_name)
                )""",
                """CREATE TABLE IF NOT EXISTS Inventory (
                    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT NOT NULL,
                    quantity INT NOT NULL DEFAULT 0,
                    last_restocked DATE,
                    FOREIGN KEY (product_id) REFERENCES Products(product_id),
                    UNIQUE KEY unique_inventory (product_id)
                )""",
                """CREATE TABLE IF NOT EXISTS Sales (
                    sale_id INT AUTO_INCREMENT PRIMARY KEY,
                    customer_id INT,
                    seller_id INT,
                    sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    total_amount DECIMAL(10, 2),
                    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
                    FOREIGN KEY (seller_id) REFERENCES Sellers(seller_id)
                )""",
                """CREATE TABLE IF NOT EXISTS Sale_Items (
                    item_id INT AUTO_INCREMENT PRIMARY KEY,
                    sale_id INT NOT NULL,
                    product_id INT NOT NULL,
                    quantity INT NOT NULL,
                    unit_price DECIMAL(10, 2) NOT NULL,
                    FOREIGN KEY (sale_id) REFERENCES Sales(sale_id),
                    FOREIGN KEY (product_id) REFERENCES Products(product_id)
                )"""
            ]
            
            for table in tables:
                self.cursor.execute(table)
                
            self.db.commit()
            print("All tables verified/created successfully")
        except mysql.connector.Error as err:
            print(f"Table creation error: {err}")
            messagebox.showerror("Database Error", f"Failed to initialize tables: {err}")

    def create_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=10, fill=BOTH, expand=True)
        
        self.create_seller_tab()
        self.create_customer_tab()
        self.create_product_tab()
        self.create_inventory_tab()
        self.create_sales_tab()

    def create_seller_tab(self):
        tab = Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(tab, text="Sellers")

        # Seller Form
        Label(tab, text="Seller Name:", bg="#f0f0f0", font=self.label_font).grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.seller_name = Entry(tab, font=self.entry_font)
        self.seller_name.grid(row=0, column=1, padx=5, pady=5)

        Label(tab, text="Contact Number:", bg="#f0f0f0", font=self.label_font).grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.seller_contact = Entry(tab, font=self.entry_font)
        self.seller_contact.grid(row=1, column=1, padx=5, pady=5)

        Label(tab, text="Email:", bg="#f0f0f0", font=self.label_font).grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.seller_email = Entry(tab, font=self.entry_font)
        self.seller_email.grid(row=2, column=1, padx=5, pady=5)

        Button(tab, text="Add Seller", command=self.add_seller, font=self.button_font, bg="#4CAF50", fg="white").grid(row=3, column=0, columnspan=2, pady=10)

        # Seller Treeview
        self.seller_tree = ttk.Treeview(tab, columns=("ID", "Name", "Contact", "Email"), show="headings")
        self.seller_tree.heading("ID", text="ID")
        self.seller_tree.heading("Name", text="Name")
        self.seller_tree.heading("Contact", text="Contact")
        self.seller_tree.heading("Email", text="Email")
        self.seller_tree.column("ID", width=50)
        self.seller_tree.column("Name", width=150)
        self.seller_tree.column("Contact", width=100)
        self.seller_tree.column("Email", width=150)
        self.seller_tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        Button(tab, text="View Sellers", command=self.view_sellers, font=self.button_font, bg="#2196F3", fg="white").grid(row=5, column=0, columnspan=2, pady=10)

    def create_customer_tab(self):
        tab = Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(tab, text="Customers")

        # Customer Form
        Label(tab, text="Customer Name:", bg="#f0f0f0", font=self.label_font).grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.customer_name = Entry(tab, font=self.entry_font)
        self.customer_name.grid(row=0, column=1, padx=5, pady=5)

        Label(tab, text="Contact Number:", bg="#f0f0f0", font=self.label_font).grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.customer_contact = Entry(tab, font=self.entry_font)
        self.customer_contact.grid(row=1, column=1, padx=5, pady=5)

        Label(tab, text="Email:", bg="#f0f0f0", font=self.label_font).grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.customer_email = Entry(tab, font=self.entry_font)
        self.customer_email.grid(row=2, column=1, padx=5, pady=5)

        Button(tab, text="Add Customer", command=self.add_customer, font=self.button_font, bg="#4CAF50", fg="white").grid(row=3, column=0, columnspan=2, pady=10)

        # Customer Treeview
        self.customer_tree = ttk.Treeview(tab, columns=("ID", "Name", "Contact", "Email"), show="headings")
        self.customer_tree.heading("ID", text="ID")
        self.customer_tree.heading("Name", text="Name")
        self.customer_tree.heading("Contact", text="Contact")
        self.customer_tree.heading("Email", text="Email")
        self.customer_tree.column("ID", width=50)
        self.customer_tree.column("Name", width=150)
        self.customer_tree.column("Contact", width=100)
        self.customer_tree.column("Email", width=150)
        self.customer_tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        Button(tab, text="View Customers", command=self.view_customers, font=self.button_font, bg="#2196F3", fg="white").grid(row=5, column=0, columnspan=2, pady=10)

    def create_product_tab(self):
        tab = Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(tab, text="Products")

        # Product Form
        Label(tab, text="Product Name:", bg="#f0f0f0", font=self.label_font).grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.product_name = Entry(tab, font=self.entry_font)
        self.product_name.grid(row=0, column=1, padx=5, pady=5)

        Label(tab, text="Description:", bg="#f0f0f0", font=self.label_font).grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.product_desc = Entry(tab, font=self.entry_font)
        self.product_desc.grid(row=1, column=1, padx=5, pady=5)

        Label(tab, text="Price:", bg="#f0f0f0", font=self.label_font).grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.product_price = Entry(tab, font=self.entry_font)
        self.product_price.grid(row=2, column=1, padx=5, pady=5)

        Label(tab, text="Category:", bg="#f0f0f0", font=self.label_font).grid(row=3, column=0, padx=5, pady=5, sticky=W)
        self.product_category = Entry(tab, font=self.entry_font)
        self.product_category.grid(row=3, column=1, padx=5, pady=5)

        Button(tab, text="Add Product", command=self.add_product, font=self.button_font, bg="#4CAF50", fg="white").grid(row=4, column=0, columnspan=2, pady=10)

        # Product Treeview
        self.product_tree = ttk.Treeview(tab, columns=("ID", "Name", "Description", "Price", "Category"), show="headings")
        self.product_tree.heading("ID", text="ID")
        self.product_tree.heading("Name", text="Name")
        self.product_tree.heading("Description", text="Description")
        self.product_tree.heading("Price", text="Price")
        self.product_tree.heading("Category", text="Category")
        self.product_tree.column("ID", width=50)
        self.product_tree.column("Name", width=150)
        self.product_tree.column("Description", width=200)
        self.product_tree.column("Price", width=80)
        self.product_tree.column("Category", width=100)
        self.product_tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        Button(tab, text="View Products", command=self.view_products, font=self.button_font, bg="#2196F3", fg="white").grid(row=6, column=0, columnspan=2, pady=10)

    def create_inventory_tab(self):
        tab = Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(tab, text="Inventory")

        # Inventory Form
        Label(tab, text="Product:", bg="#f0f0f0", font=self.label_font).grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.inventory_product = ttk.Combobox(tab, font=self.entry_font)
        self.inventory_product.grid(row=0, column=1, padx=5, pady=5)

        Label(tab, text="Quantity:", bg="#f0f0f0", font=self.label_font).grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.inventory_quantity = Entry(tab, font=self.entry_font)
        self.inventory_quantity.grid(row=1, column=1, padx=5, pady=5)

        Button(tab, text="Update Inventory", command=self.update_inventory, font=self.button_font, bg="#4CAF50", fg="white").grid(row=2, column=0, columnspan=2, pady=10)

        # Inventory Treeview
        self.inventory_tree = ttk.Treeview(tab, columns=("ID", "Product", "Quantity", "Last Restocked"), show="headings")
        self.inventory_tree.heading("ID", text="ID")
        self.inventory_tree.heading("Product", text="Product")
        self.inventory_tree.heading("Quantity", text="Quantity")
        self.inventory_tree.heading("Last Restocked", text="Last Restocked")
        self.inventory_tree.column("ID", width=50)
        self.inventory_tree.column("Product", width=200)
        self.inventory_tree.column("Quantity", width=80)
        self.inventory_tree.column("Last Restocked", width=120)
        self.inventory_tree.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        Button(tab, text="View Inventory", command=self.view_inventory, font=self.button_font, bg="#2196F3", fg="white").grid(row=4, column=0, columnspan=2, pady=10)

    def create_sales_tab(self):
        tab = Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(tab, text="Sales")

        # Sales Form
        Label(tab, text="Customer:", bg="#f0f0f0", font=self.label_font).grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.sale_customer = ttk.Combobox(tab, font=self.entry_font)
        self.sale_customer.grid(row=0, column=1, padx=5, pady=5)

        Label(tab, text="Seller:", bg="#f0f0f0", font=self.label_font).grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.sale_seller = ttk.Combobox(tab, font=self.entry_font)
        self.sale_seller.grid(row=1, column=1, padx=5, pady=5)

        Label(tab, text="Product:", bg="#f0f0f0", font=self.label_font).grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.sale_product = ttk.Combobox(tab, font=self.entry_font)
        self.sale_product.grid(row=2, column=1, padx=5, pady=5)

        Label(tab, text="Quantity:", bg="#f0f0f0", font=self.label_font).grid(row=3, column=0, padx=5, pady=5, sticky=W)
        self.sale_quantity = Entry(tab, font=self.entry_font)
        self.sale_quantity.grid(row=3, column=1, padx=5, pady=5)

        Button(tab, text="Add to Sale", command=self.add_sale_item, font=self.button_font, bg="#4CAF50", fg="white").grid(row=4, column=0, columnspan=2, pady=10)

        # Sale Items Treeview
        self.sale_items_tree = ttk.Treeview(tab, columns=("Product", "Quantity", "Price", "Total"), show="headings")
        self.sale_items_tree.heading("Product", text="Product")
        self.sale_items_tree.heading("Quantity", text="Quantity")
        self.sale_items_tree.heading("Price", text="Price")
        self.sale_items_tree.heading("Total", text="Total")
        self.sale_items_tree.column("Product", width=200)
        self.sale_items_tree.column("Quantity", width=80)
        self.sale_items_tree.column("Price", width=80)
        self.sale_items_tree.column("Total", width=80)
        self.sale_items_tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Total Label
        self.sale_total_label = Label(tab, text="Total: $0.00", bg="#f0f0f0", font=self.title_font)
        self.sale_total_label.grid(row=6, column=0, columnspan=2, pady=5)

        Button(tab, text="Process Sale", command=self.process_sale, font=self.button_font, bg="#FF5722", fg="white").grid(row=7, column=0, pady=10)
        Button(tab, text="View Sales", command=self.view_sales, font=self.button_font, bg="#2196F3", fg="white").grid(row=7, column=1, pady=10)

    def load_products(self):
        try:
            self.cursor.execute("SELECT product_id, product_name FROM Products")
            products = self.cursor.fetchall()
            self.product_list = [f"{product[0]} - {product[1]}" for product in products]
            self.inventory_product['values'] = self.product_list
            self.sale_product['values'] = self.product_list
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load products: {err}")

    def load_customers(self):
        try:
            self.cursor.execute("SELECT customer_id, customer_name FROM Customers")
            customers = self.cursor.fetchall()
            self.customer_list = [f"{customer[0]} - {customer[1]}" for customer in customers]
            self.sale_customer['values'] = self.customer_list
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load customers: {err}")

    def load_sellers(self):
        try:
            self.cursor.execute("SELECT seller_id, seller_name FROM Sellers")
            sellers = self.cursor.fetchall()
            self.seller_list = [f"{seller[0]} - {seller[1]}" for seller in sellers]
            self.sale_seller['values'] = self.seller_list
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load sellers: {err}")

    def load_sale_products(self):
        try:
            self.cursor.execute("SELECT product_id, product_name, price FROM Products")
            self.sale_products_data = {f"{product[0]} - {product[1]}": product[2] for product in self.cursor.fetchall()}
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load product prices: {err}")

    def add_seller(self):
        name = self.seller_name.get()
        contact = self.seller_contact.get()
        email = self.seller_email.get()

        if not name or not contact:
            messagebox.showerror("Error", "Name and Contact are required fields")
            return

        try:
            self.cursor.execute("INSERT INTO Sellers (seller_name, contact_number, email) VALUES (%s, %s, %s)", 
                              (name, contact, email))
            self.db.commit()
            messagebox.showinfo("Success", "Seller added successfully")
            self.seller_name.delete(0, END)
            self.seller_contact.delete(0, END)
            self.seller_email.delete(0, END)
            self.load_sellers()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to add seller: {err}")
            self.db.rollback()

    def view_sellers(self):
        try:
            self.seller_tree.delete(*self.seller_tree.get_children())
            self.cursor.execute("SELECT seller_id, seller_name, contact_number, email FROM Sellers")
            sellers = self.cursor.fetchall()
            for seller in sellers:
                self.seller_tree.insert("", END, values=seller)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load sellers: {err}")

    def add_customer(self):
        name = self.customer_name.get()
        contact = self.customer_contact.get()
        email = self.customer_email.get()

        if not name or not contact:
            messagebox.showerror("Error", "Name and Contact are required fields")
            return

        try:
            self.cursor.execute("INSERT INTO Customers (customer_name, contact_number, email) VALUES (%s, %s, %s)", 
                              (name, contact, email))
            self.db.commit()
            messagebox.showinfo("Success", "Customer added successfully")
            self.customer_name.delete(0, END)
            self.customer_contact.delete(0, END)
            self.customer_email.delete(0, END)
            self.load_customers()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to add customer: {err}")
            self.db.rollback()

    def view_customers(self):
        try:
            self.customer_tree.delete(*self.customer_tree.get_children())
            self.cursor.execute("SELECT customer_id, customer_name, contact_number, email FROM Customers")
            customers = self.cursor.fetchall()
            for customer in customers:
                self.customer_tree.insert("", END, values=customer)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load customers: {err}")

    def add_product(self):
        name = self.product_name.get()
        desc = self.product_desc.get()
        price = self.product_price.get()
        category = self.product_category.get()

        if not name or not price:
            messagebox.showerror("Error", "Name and Price are required fields")
            return

        try:
            price = float(price)
            self.cursor.execute("INSERT INTO Products (product_name, description, price, category) VALUES (%s, %s, %s, %s)", 
                              (name, desc, price, category))
            self.db.commit()
            messagebox.showinfo("Success", "Product added successfully")
            self.product_name.delete(0, END)
            self.product_desc.delete(0, END)
            self.product_price.delete(0, END)
            self.product_category.delete(0, END)
            self.load_products()
        except ValueError:
            messagebox.showerror("Error", "Price must be a valid number")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to add product: {err}")
            self.db.rollback()

    def view_products(self):
        try:
            self.product_tree.delete(*self.product_tree.get_children())
            self.cursor.execute("SELECT product_id, product_name, description, price, category FROM Products")
            products = self.cursor.fetchall()
            for product in products:
                self.product_tree.insert("", END, values=product)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load products: {err}")

    def update_inventory(self):
        product = self.inventory_product.get()
        quantity = self.inventory_quantity.get()

        if not product or not quantity:
            messagebox.showerror("Error", "Product and Quantity are required fields")
            return

        try:
            product_id = int(product.split(" - ")[0])
            quantity = int(quantity)
            
            # Check if inventory record exists
            self.cursor.execute("SELECT quantity FROM Inventory WHERE product_id = %s", (product_id,))
            result = self.cursor.fetchone()
            
            if result:
                # Update existing inventory
                new_quantity = result[0] + quantity
                self.cursor.execute("UPDATE Inventory SET quantity = %s, last_restocked = CURDATE() WHERE product_id = %s",
                                  (new_quantity, product_id))
            else:
                # Create new inventory record
                self.cursor.execute("INSERT INTO Inventory (product_id, quantity, last_restocked) VALUES (%s, %s, CURDATE())",
                                  (product_id, quantity))
            
            self.db.commit()
            messagebox.showinfo("Success", "Inventory updated successfully")
            self.inventory_product.set('')
            self.inventory_quantity.delete(0, END)
            self.view_inventory()
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a valid integer")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to update inventory: {err}")
            self.db.rollback()

    def view_inventory(self):
        try:
            self.inventory_tree.delete(*self.inventory_tree.get_children())
            self.cursor.execute("""
                SELECT i.inventory_id, p.product_name, i.quantity, i.last_restocked 
                FROM Inventory i
                JOIN Products p ON i.product_id = p.product_id
            """)
            inventory = self.cursor.fetchall()
            for item in inventory:
                self.inventory_tree.insert("", END, values=item)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load inventory: {err}")

    def add_sale_item(self):
        product = self.sale_product.get()
        quantity = self.sale_quantity.get()

        if not product or not quantity:
            messagebox.showerror("Error", "Product and Quantity are required fields")
            return

        try:
            # Convert quantity to integer and validate
            quantity = int(quantity)
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be a positive number")
                return

            # Get product details
            product_id = int(product.split(" - ")[0])
            
            # Get product price from database and handle Decimal type
            self.cursor.execute("SELECT price FROM Products WHERE product_id = %s", (product_id,))
            result = self.cursor.fetchone()
            
            if not result:
                messagebox.showerror("Error", "Selected product not found")
                return
                
            price = float(result[0]) if isinstance(result[0], Decimal) else result[0]

            # Check inventory availability
            self.cursor.execute("SELECT quantity FROM Inventory WHERE product_id = %s", (product_id,))
            inventory = self.cursor.fetchone()
            
            if not inventory:
                messagebox.showerror("Error", "Product not available in inventory")
                return
                
            available_quantity = inventory[0]
            if quantity > available_quantity:
                messagebox.showerror("Error", f"Not enough stock. Only {available_quantity} available")
                return

            # Calculate total for this item
            total = float(price * quantity)

            # Add to sale items list
            self.sale_items.append({
                "product_id": product_id,
                "product_name": product,
                "quantity": quantity,
                "price": price,
                "total": total
            })

            # Update the treeview
            self.sale_items_tree.insert("", END, 
                                      values=(product, quantity, f"${price:.2f}", f"${total:.2f}"))

            # Update total label - handle Decimal/float conversion
            current_total_text = self.sale_total_label.cget("text")
            try:
                current_total = float(current_total_text.split("$")[1]) if "$" in current_total_text else 0.0
            except:
                current_total = 0.0
                
            new_total = current_total + total
            self.sale_total_label.config(text=f"Total: ${new_total:.2f}")

            # Clear the input fields
            self.sale_product.set('')
            self.sale_quantity.delete(0, END)

        except ValueError:
            messagebox.showerror("Error", "Quantity must be a valid number")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to add sale item: {err}")
        except Exception as err:
            messagebox.showerror("Error", f"Unexpected error: {str(err)}")

    def process_sale(self):
        if not self.sale_items:
            messagebox.showerror("Error", "No items in the sale")
            return

        customer = self.sale_customer.get()
        seller = self.sale_seller.get()

        if not customer or not seller:
            messagebox.showerror("Error", "Customer and Seller are required fields")
            return

        try:
            customer_id = int(customer.split(" - ")[0])
            seller_id = int(seller.split(" - ")[0])
            
            # Handle Decimal/float conversion for total amount
            total_amount_text = self.sale_total_label.cget("text")
            total_amount = float(total_amount_text.split("$")[1]) if "$" in total_amount_text else 0.0
            
            # Start transaction
            self.cursor.execute("START TRANSACTION")
            
            # Create sale record
            self.cursor.execute("""
                INSERT INTO Sales (customer_id, seller_id, total_amount) 
                VALUES (%s, %s, %s)
            """, (customer_id, seller_id, total_amount))
            sale_id = self.cursor.lastrowid
            
            # Add sale items and update inventory
            for item in self.sale_items:
                product_id = item['product_id']
                
                # Add sale item - ensure proper decimal handling
                unit_price = Decimal(str(item['price']))
                self.cursor.execute("""
                    INSERT INTO Sale_Items (sale_id, product_id, quantity, unit_price)
                    VALUES (%s, %s, %s, %s)
                """, (sale_id, product_id, item['quantity'], unit_price))
                
                # Update inventory
                self.cursor.execute("""
                    UPDATE Inventory 
                    SET quantity = quantity - %s 
                    WHERE product_id = %s
                """, (item['quantity'], product_id))
            
            self.db.commit()
            messagebox.showinfo("Success", "Sale processed successfully")
            
            # Reset sale form
            self.sale_items = []
            self.sale_items_tree.delete(*self.sale_items_tree.get_children())
            self.sale_total_label.config(text="Total: $0.00")
            self.sale_customer.set('')
            self.sale_seller.set('')
            self.view_inventory()
        except mysql.connector.Error as err:
            self.db.rollback()
            messagebox.showerror("Error", f"Failed to process sale: {err}")
        except Exception as err:
            self.db.rollback()
            messagebox.showerror("Error", f"An error occurred: {str(err)}")

    def view_sales(self):
        try:
            # Create a new window for sales report
            sales_window = Toplevel(self.root)
            sales_window.title("Sales Report")
            sales_window.geometry("1000x600")
            
            # Date range selection
            frame = Frame(sales_window, padx=10, pady=10)
            frame.pack(fill=X)
            
            Label(frame, text="From:").grid(row=0, column=0, padx=5)
            self.from_date = Entry(frame)
            self.from_date.grid(row=0, column=1, padx=5)
            
            Label(frame, text="To:").grid(row=0, column=2, padx=5)
            self.to_date = Entry(frame)
            self.to_date.grid(row=0, column=3, padx=5)
            
            Button(frame, text="Filter", command=self.filter_sales).grid(row=0, column=4, padx=10)
            
            # Sales Treeview
            tree = ttk.Treeview(sales_window, columns=("ID", "Date", "Customer", "Seller", "Total"), show="headings")
            tree.heading("ID", text="ID")
            tree.heading("Date", text="Date")
            tree.heading("Customer", text="Customer")
            tree.heading("Seller", text="Seller")
            tree.heading("Total", text="Total")
            tree.column("ID", width=50)
            tree.column("Date", width=120)
            tree.column("Customer", width=150)
            tree.column("Seller", width=150)
            tree.column("Total", width=100)
            tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
            
            # Load all sales initially
            self.cursor.execute("""
                SELECT s.sale_id, s.sale_date, c.customer_name, sl.seller_name, s.total_amount 
                FROM Sales s
                LEFT JOIN Customers c ON s.customer_id = c.customer_id
                LEFT JOIN Sellers sl ON s.seller_id = sl.seller_id
                ORDER BY s.sale_date DESC
            """)
            sales = self.cursor.fetchall()
            for sale in sales:
                tree.insert("", END, values=sale)
            
            # Store the tree reference for filtering
            self.sales_tree = tree
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load sales: {err}")

    def filter_sales(self):
        from_date = self.from_date.get()
        to_date = self.to_date.get()
        
        try:
            query = """
                SELECT s.sale_id, s.sale_date, c.customer_name, sl.seller_name, s.total_amount 
                FROM Sales s
                LEFT JOIN Customers c ON s.customer_id = c.customer_id
                LEFT JOIN Sellers sl ON s.seller_id = sl.seller_id
                WHERE 1=1
            """
            params = []
            
            if from_date:
                query += " AND s.sale_date >= %s"
                params.append(from_date)
            if to_date:
                query += " AND s.sale_date <= %s"
                params.append(to_date)
            
            query += " ORDER BY s.sale_date DESC"
            
            self.cursor.execute(query, tuple(params))
            sales = self.cursor.fetchall()
            
            self.sales_tree.delete(*self.sales_tree.get_children())
            for sale in sales:
                self.sales_tree.insert("", END, values=sale)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to filter sales: {err}")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.cursor.close()
            self.db.close()
            self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    app = StoreManagementSystem(root)
    root.mainloop()
