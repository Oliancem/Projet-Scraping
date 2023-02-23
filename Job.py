class Job:

    def __init__(self, url, title, company_name, type, location, description):
        self.url = url
        self.title = title
        self.company_name = company_name
        self.type = type
        self.location = location
        self.description = description

    def get_url(self):
        return self.url
    
    def get_title(self):
        return self.title
    
    def get_company_name(self):
        return self.company_name
    
    def get_type(self):
        return self.type

    def get_location(self):
        return self.location
    
    def get_description(self):
        return self.description