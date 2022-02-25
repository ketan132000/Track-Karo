class Product:
    def __init__(self, name, price, image, link):
        self.name = name
        self.price = price
        self.image = image
        self.link = link

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_image(self):
        return self.image

    def get_link(self):
        return self.link
