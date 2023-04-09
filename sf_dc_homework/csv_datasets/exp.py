class DepartmentReport():
    
    def __init__(self, company_name) -> None:
        self.revenues = []
        self.company_name = company_name
    
    def add_revenue(self, revenue):
        # if not hasattr(self, 'revenues'):
        #     self.revenues = []
        self.revenues.append(revenue)
        
    def average_revenue(self):
        average_revenue = sum(self.revenues) / len(self.revenues)
        return f'Average department revenue for {self.company_name}: {round(average_revenue)}'

report = DepartmentReport("Danon")
report.add_revenue(1_000_000)
report.add_revenue(400_000)

# print(report.average_revenue())
# => Average department revenue for Danon: 700000

class User():
    
    def __init__(self, email, password, balance,) -> None:
        self.email = email
        self.password = password
        self.balance = balance
        
    def login(self, email, password):
        return self.email == email and self.password == password
    
    def update_balance(self, amount):
        self.balance += amount
        
user = User("gosha@roskino.org", "qwerty", 20_000)
# print(user.login("gosha@roskino.org", "qwerty123"))
# => False
# print(user.login("gosha@roskino.org", "qwerty"))
# => True
user.update_balance(200)
user.update_balance(-500)
# print(user.balance)
# => 19700


""" Определите класс IntDataFrame, который принимает список и приводит к целым значениям все числа в этом списке. 
После этого становится доступен метод count, который считает количество ненулевых элементов, 
и метод unique, который возвращает число уникальных элементов.

В случае правильного описания класса код, приведённый ниже, должен выдать следующий результат:
"""
class IntDataFrame():
    def __init__(self, init_list) -> None:
        self.int_list = [int(x) for x in init_list]
        
    def count(self):
        count = 0
        for i in self.int_list:
            if i != 0:
                count += 1
        return count
                
    def unique(self):
        return len(set(self.int_list))
        



# df = IntDataFrame([4.7, 4, 3, 0, 2.4, 0.3, 4])
# print(df.count())
# => 5
# print(df.unique())
# => 4



class OwnLogger():
    def __init__(self) -> None:
        self.logger = {'info': [],
                       'warning': [],
                       'error': []}
        self.last_message = None
    
    def log(self, message, level):
        self.last_message = message
        self.logger[level].append(message)
        
    def show_last(self, level='all'):
        if level == 'all':
            return self.last_message
        if self.logger[level]:    
            return self.logger[level][-1] 
    
logger = OwnLogger()
logger.log("System started", "info")
# print(logger.show_last("error"))
# => None
# Некоторые интерпретаторы Python могут не выводить None, тогда в этой проверке у вас будет пустая строка
logger.log("Connection instable", "warning")
logger.log("Connection lost", "error")

print(logger.show_last())
# => Connection lost
print(logger.show_last("info"))
# => System started
        
