
def add_employees_id(employees):
    for i in range(len(employees)):
        employees[i]['工号'] = f"QSJT-{i+1:04d}"
    return employees