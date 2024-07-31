
import pandas as pd
import re

# Load the data from the Excel file
file_path = '/content/copy of data 1yr (1) 1.xlsx'
data = pd.read_excel(file_path)

# Define categories and associated keywords
categories = {
    'Network Issue': ['network', 'connectivity', 'internet', 'wifi', 'lan', 'wan', 'server down'],
    'Software Issue': [
        'software', 'application', 'program', 'crash', 'error', 'bug', 'sap', 'finance', 'abap', 't-code',
        'integration', 'authorization', 'slowness', 'duplicate', 'print', 'order', 'transaction',
        'data mapping', 'edi', 'ke4h', 'f110', 'issue', 'mrp', 'inspection', 'attp', 'asn', 'ssl certificates',
        'filezilla connection', 'smart source PO', 'EDICOM', 'sales interface error'
    ],
    'Hardware Issue': ['hardware', 'computer', 'laptop', 'pc', 'mouse', 'keyboard'],
    'Account Issue': [
        'account', 'login', 'password', 'credential', 'username', 'access', 'permission', 'reset',
        'unlock', 'reactivation', 'role', 'user id', 'firefighter', 'validity', 'creation', 'modification',
        'extend', 'id', 'firefighter', 'firefighter ID', 'account reactivation', 'out of validity date',
        'backend password reset', 'backend account unlock', 'general account administration', 'new user creation',
        'user creation', 'test user ID', 'role assignment', 'role request', 'role assignment issue', 'role issue',
        'role assignment', 'role access', 'assign role', 'role ZG0', 'role ITS_S'
    ],
    'SAP Functional Issue': [
        'MRP run issue', 'inspection lot', 'OTC issue', 'performance issue', 'transactional data locked',
        'batch locked', 'ABAP dumps', 'printer issue', 'EDI interface not working', 'slow processing',
        'route dependent condition', 'material master update', 'QM lot not created', 'storage type creation error',
        'CO60 issue', 'PH7 assistance request', 'GRIR issue', 'AFAB issue', 'COGI issue', 'FEBAN issue',
        'Quality Hold interface Issue', 'ALM notifications issue'
    ],
    'EDI and Integration Issue': [
        'EDI duplicate invoices', 'Idoc message type', 'inbound non-PO invoice issue', 'ALEBW user locked',
        'ATTP and NOSP connection issue', 'SHPCON from partner FRANCERP', 'EDI order status',
        'Henry Schein EDI', 'IDOC communication', 'SeeBurger', 'entity and MDL upload failure'
    ],
    'File Transfer Issue': [
        'FTP site', 'file delivery issue', 'file transfer', 'files not delivered', 'smart source PO', 'filezilla connection'
    ],
    'General IT Request': [
        'access request', 'password reset', 'open connection', 'user account validity extension', 'extract active users',
        'Control-M access reinitialization', 'IT offline form submission', 'general IT request', 'digital certificates issue',
        'Flex Pre-Upgrade Activity', 'Flex POST-Upgrade Activity', 'Hyperion', 'Seeburger Access Request', 'Application Data Request',
        'Analytics folder issue'
    ],
    'General Inquiry': ['general', 'inquiry', 'question', 'info', 'information']
}

# Function to categorize based on keywords
def categorize_description(description):
    description = str(description)  # Ensure the description is a string
    for category, keywords in categories.items():
        if any(re.search(r'\b{}\b'.format(keyword), description, re.IGNORECASE) for keyword in keywords):
            return category
    return 'Other'  # Default category if no keywords match

# Apply the categorization function to the 'Short Description' column
data['Category'] = data['Short Description'].apply(categorize_description)

# Calculate the number of tickets in each category
category_counts = data['Category'].value_counts().reset_index()
category_counts.columns = ['Category', 'Number of Tickets']
print(category_counts)

# Save the updated dataframe and category counts to a new Excel file
output_file_path = '/content/book.xlsx'
with pd.ExcelWriter(output_file_path) as writer:
    data.to_excel(writer, sheet_name='Tickets', index=False)
    category_counts.to_excel(writer, sheet_name='Category Counts', index=False)

output_file_path
