
class AdminPortal():


    def authenticate(self, username, password):
        if str(username).lower() == 'ayush' and str(password).lower() == '1234':
            return True
        else:
            return False
