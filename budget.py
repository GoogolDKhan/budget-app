class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = list()

    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = ""
        total = 0
        for item in self.ledger:
            items += f"{item['description'][0:23]:23}" + f"{item['amount']:>7.2f}" + "\n"
            total += item['amount']

        output = title + items + "Total: " + str(total)
        return output

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if (self.check_funds(amount)):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        total_cash = 0
        for item in self.ledger:
            total_cash += item["amount"]
        return total_cash

    def transfer(self, amount, category):
        if (self.check_funds(amount)):
            self.withdraw(amount, "Transfer to " + category.name)
            category.deposit(amount, "Transfer from " + self.name)
            return True
        return False

    def check_funds(self, amount):
        if (self.get_balance() >= amount):
            return True
        return False

    # Category method
    def total_withdrawn(self):
        total = 0
        for item in self.ledger:
            if item["amount"] < 0:
                total += item["amount"]
        return total


def create_spend_chart(categories):

    bar_chart = "Percentage spent by category\n"
    total = 0
    subtotals = {}
    percentages = {}
    name_length = 0

    # make a dictionary of category: subtotals and find the grand total spending
    for category in categories:
        subtotal = category.total_withdrawn()
        subtotals[category.name] = subtotal
        total = total + subtotal

    # find the rounded percentage that each category contributed to overall spending and add the dictionary category: percentage
    for name, subtotal in subtotals.items():
        percent = subtotal / total * 100
        percent = percent - (percent % 10)
        percentages[name] = percent

    # create the y axis and add the values to the chart
    x = 100
    for number in range(11):
        bar_row = f"{x}".rjust(3) + "| "
        for name, percent in percentages.items():
            if percent >= (x):
                bar_row += "o  "
            else:
                bar_row += "   "
        bar_chart += bar_row + '\n'
        x -= 10

    # add the x axis
    x_axis = "    -"
    for category in categories:
        x_axis += ("---")
    bar_chart += x_axis + "\n"

    # determines the longest category name length
    for category in categories:
        if len(category.name) > name_length:
            name_length = len(category.name)

    # add the category names for x axis values
    y = 0
    while y <= name_length:
        row = "     "
        for key, value in percentages.items():
            category_name = key
            try:
                row += category_name[y] + "  "
            except:  # for when the name has already been spelled out
                row += "   "

        if y <= name_length - 1:
            bar_chart += row + '\n'
        else:
            bar_chart += row.strip(" ")

        y = y + 1
    bar_chart = bar_chart.rstrip("\n")
    return bar_chart
