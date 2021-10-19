from faker import Faker
import csv
import names
import random
import datetime
import pandas
import os
import math
from decimal import Decimal
import pyodbc


def generate_phones(count):
    country = "+1"
    area_codes = pandas.read_csv("Area.tsv", sep="\t", header=None, index_col=0)
    area_codes = area_codes.sample(count, replace=True)
    codes = area_codes[1].tolist()
    numbers = []
    for code in codes:
        last_digits = ""
        for index in range(0, 7):
            digit = random.randrange(0, 10)
            last_digits += str(digit)
        numbers.append(country + str(code) + last_digits)
    return numbers


def date_in_range(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date


def generate_customers():
    module_dir = os.path.dirname(__file__)
    target_dir = os.path.join(os.path.dirname(module_dir), "SQL", "Data")
    path_name = os.path.join(target_dir, "EmployeeJobList.tsv")

    # Use employee jobs to get list of cashiers
    employee_jobs = pandas.read_csv(path_name, delimiter="\t", header=None)
    valid_jobs = employee_jobs[employee_jobs[3] == 2]
    emp_indices = valid_jobs[2].values.tolist()
    emp_indices = [x - 1 for x in emp_indices]
    path_name = os.path.join(target_dir, "EmployeeList.tsv")
    employees = pandas.read_csv(path_name, delimiter="\t", header=None, index_col=0)
    employees = employees.iloc[emp_indices]

    # Sample 100 valid employees to use as customer creators
    employees = employees.sample(100, replace=True)
    start_dates = employees[7].values.tolist()
    end_dates = employees[8].values.tolist()
    employees.reset_index(inplace=True)
    customers = employees[[0]].copy()
    customers.index += 1
    dates = []

    # Builds customer create dates from employee start/end dates
    for index, start_date in enumerate(start_dates):
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = end_dates[index]

        if isinstance(end_date, float):
            end_date = datetime.date(2020, 1, 1)
        else:
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        date = date_in_range(start_date, end_date)
        dates.append(date)

    # Builds profile data for each customer
    cust_info = []
    for index in range(0, 100):
        first_name = names.get_first_name()
        last_name = names.get_last_name()
        email = first_name + last_name + "@gmail.com"
        status = random.choice([1, 3, 4])
        birth_date = date_in_range(datetime.date(1960, 1, 1), datetime.date(2000, 1, 1))
        cust_info.append([first_name, last_name, email, birth_date, status])

    customers[1] = dates
    phone_numbers = generate_phones(100)
    customers[2] = phone_numbers
    customers[3] = ""
    customers[[4, 5, 6, 7, 8]] = cust_info
    customers = customers[[4, 5, 6, 2, 3, 7, 1, 0, 8]]
    customers[9] = ""
    locations = [x for x in range(101, 201)]
    customers[10] = locations
    path_name = os.path.join(target_dir, "CustomerList.tsv")
    customers.to_csv(path_name, header=False, index=True, sep="\t")

    # Build Customer Social Media
    cust_ss = customers.sample(20)
    cust_ss["ss_code"] = cust_ss[4] + cust_ss[5]
    ss_types = []
    for index in range(0, 20):
        ss_types.append(random.randrange(1, 4))
    cust_ss["type"] = ss_types
    cust_ss["cust_id"] = cust_ss.index
    cust_ss.reset_index(inplace=True)
    cust_ss.index += 1
    cust_ss = cust_ss[["ss_code", 1, "cust_id", "type"]]
    path_name = os.path.join(target_dir, "CustomerSocialMediaList.tsv")
    cust_ss.to_csv(path_name, header=False, index=True, sep="\t")


def job_start_date(start_date, add_days):
    return start_date + datetime.timedelta(days=add_days)


def generate_employees():
    fake = Faker()
    module_dir = os.path.dirname(__file__)
    base_path = os.path.join(os.path.dirname(module_dir), "SQL", "Data")
    emp_job_path = os.path.join(base_path, "EmployeeJobList.tsv")
    employee_jobs = open(emp_job_path, 'w', newline='', )
    employee_job_writer = csv.writer(employee_jobs, delimiter='\t')
    emp_path = os.path.join(base_path, "EmployeeList.tsv")
    with open(emp_path, 'w', newline='', ) as customer_tsv:
        employee_writer = csv.writer(customer_tsv, delimiter='\t')
        phone_numbers = generate_phones(100)
        for row in range(0, 100):
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            email = first_name + last_name + "@gmail.com"
            start_date = date_in_range(datetime.date(2010, 1, 1), datetime.date(2018, 1, 1))
            birth_date = date_in_range(datetime.date(1960, 1, 1), datetime.date(2000, 1, 1))
            emp_type = random.randrange(1, 3)
            status = random.randrange(1, 6)
            end_date = ""
            if status > 1:
                max_date = min(start_date + datetime.timedelta(days=1000), datetime.date(2020, 1, 1))
                end_date = date_in_range(start_date, max_date)

            employee_writer.writerow([row + 1, first_name, last_name, email, phone_numbers[row], "", birth_date,
                                      start_date, end_date, row + 1, status, emp_type])
            for x in range(1, 3):
                select = random.randrange(0, 11)
                if select < 6:
                    job_type = random.randrange(1, 3)
                    employee_job_writer.writerow(["", job_start_date(start_date, 200), row + 1, job_type, x])
                    continue

                if select == 10:
                    employee_job_writer.writerow(["", job_start_date(start_date, 200), row + 1, 1, x])
                    employee_job_writer.writerow(["", job_start_date(start_date, 200), row + 1, 2, x])
                    continue
    employee_jobs.close()


def get_product_list():
    path_name = os.path.join(build_path(), "ProductList.tsv")
    ava_products = pandas.read_csv(path_name, delimiter="\t", converters={'Price': lambda a: Decimal(a)}, index_col="ID")
    ava_products["ID"] = ava_products.index
    path_name = os.path.join(build_path(), "StoreProductList.tsv")
    store_products = pandas.read_csv(path_name, delimiter="\t", header=None, index_col=0)
    product_list = store_products.join(ava_products, on=2, lsuffix="ls")

    return product_list


def select_store_products(store, num, product_list):
    product_list = product_list.loc[product_list[3] == store]
    product_list = product_list.sample(num)
    return product_list


# qty, ind_price, total_price, product, order
def generate_order_lines(order_index, product_list, store_index):
    order_list = []
    num = random.randrange(1, 6)
    selected_products = select_store_products(store_index, num, product_list)
    selected_products.reset_index(inplace=True)
    final_price = Decimal(0)
    total_price = 0
    for index in range(num):
        line_id = selected_products.at[index, "ID"]
        amount = Decimal(random.randrange(1, 6))
        ind_price = Decimal(selected_products.at[index, 'Price'])
        total_price = Decimal(amount * ind_price)
        row = [amount, ind_price, total_price, line_id, order_index]
        final_price += total_price
        order_list.append(row)
    return order_list, total_price


def get_employee_store(emp_num):
    path_name = os.path.join(build_path(), "EmployeeJobList.tsv")
    employee_jobs = pandas.read_csv(path_name, delimiter="\t", header=None)
    employee_jobs = employee_jobs.loc[employee_jobs[2] == emp_num]
    employee_jobs = employee_jobs.loc[employee_jobs[3] == 2]
    employee_jobs = (employee_jobs.sample(1))
    employee_jobs = employee_jobs[4].values.tolist()
    store = employee_jobs[0]
    return store


# ID, Quantity, ind_price, total_price, product, order
def generate_orders():
    product_list = get_product_list()
    path_name = os.path.join(build_path(), "CustomerList.tsv")
    customers = pandas.read_csv(path_name, delimiter="\t", header=None)
    orders = customers[[0, 7, 8]].copy()
    payments = []
    for index in range(100):
        payments.append(random.randrange(1, 3))
    orders["payment"] = payments
    orders["discount"] = 0
    emp_ids = orders[8].values.tolist()
    stores = []
    order_lines = []
    totals = []
    for index, emp in enumerate(emp_ids):
        store_id = get_employee_store(emp)
        stores.append(store_id)
        lines, total_price = generate_order_lines(index+1, product_list, store_id)
        totals.append(total_price)
        order_lines += lines
    orders["store"] = stores
    orders["o_total"] = totals
    orders["f_total"] = totals
    order_lines = pandas.DataFrame(order_lines)
    order_lines.index += 1
    path_name = os.path.join(build_path(), "OrderLineList.tsv")
    order_lines.to_csv(path_name, header=None, index=True, sep="\t")
    orders["cust_id"] = orders[0]
    orders = orders[[0, 7, "o_total", "f_total", "discount", "cust_id", "payment", "store"]]
    path_name = os.path.join(build_path(), "OrderList.tsv")
    orders.to_csv(path_name, header=None, index=False, sep="\t")

    #id,


    # Get employee list
    # Get customer list
    # Extract create employee ID's from customer list
    # Extract create employees from employee list using emp_ID


def build_path():
    module_dir = os.path.dirname(__file__)
    base_path = os.path.join(os.path.dirname(module_dir), "SQL", "Data")
    return base_path


def generate_store_products():
    path_name = os.path.join(build_path(), "ProductList.tsv")
    products = pandas.read_csv(path_name, delimiter="\t")
    product_ids = products["ID"].values.tolist()
    options = [[1], [2], [1, 2]]
    store_products = []
    for id in product_ids:
        stores = random.choice(options)
        for store in stores:
            store_products.append([datetime.date(2010, 1, 1), id, store])
    store_products = pandas.DataFrame(store_products)
    store_products.index += 1
    path_name = os.path.join(build_path(), "StoreProductList.tsv")
    store_products.to_csv(path_name, header=False, index=True, sep="\t")


# Add end date to customers
#
if __name__ == '__main__':
    # generate_employees()
    # generate_customers()
    #generate_orders()
    # generate_order_lines(200)
    # generate_store_products()
    generate_orders()
    #products = get_product_list()
    #products.to_csv("Here.tsv", sep="\t")
    #print(products)
    #print(select_store_products(2, 5, products))
