class Product:
    def __init__(self, name : str,
                category : str,
                quantity : int,
                reorder_level : int,
                unit_price : int,
                id_key : int | None
                ):

        self.id_key = id_key
        self.name = name
        self.category = category
        self.quantity = quantity
        self.reorder_level = reorder_level
        self.unit_price = unit_price

    def __str__(self):
        return(
        f"ID: {self.id_key} | "
        f"Name: {self.name} | "
        f"Category: {self.category} | "
        f"Quantity: {self.quantity} | "
        f"Reorder Level: {self.reorder_level} | "
        f"Unit Price: £{self.unit_price / 100:.2f}"
        )

    

        

    
        
