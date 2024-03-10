#pyinstaller --name "QIFtoCSV" --noconsole --onefile --icon=icotetas.ico ui.py
import pandas
from quiffen import Qif

def setCategory(row):
    if type(row) == dict:
        row = row["hierarchy"]
    return row

def setDate(row):
    if type(row) == pandas._libs.tslibs.timestamps.Timestamp:
        row = str(row.day) + "/" + str(row.month) + "/" + str(row.year)
    return row

def convertQIF2CSV(QIF_file_name):
    qif = Qif.parse(QIF_file_name, day_first=False, encoding="ISO-8859-1")
    df = qif.to_dataframe()

    df = df.drop(columns=[
        "cleared",
        "payee_address",
        "reimbursable_expense",
        "small_business_expense",
        "first_payment_date",
        "loan_length",
        "num_payments",
        "periods_per_annum",
        "interest_rate",
        "current_loan_balance",
        "original_loan_amount",
        "line_number",
        ])


    df['category'] = df['category'].apply(lambda row: setCategory(row))
    df['date'] = df['date'].apply(lambda row: setDate(row))

    df = df[[
        "to_account",
        "date",
        "check_number",
        "payee",
        "memo",
        "category",
        "amount",
        "splits"
        ]]

    CSV_file_name = QIF_file_name.split(".")[0] + ".xlsx"

    df.to_excel(CSV_file_name, index = True)

    return CSV_file_name

