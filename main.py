import os
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

today = datetime.now().strftime('%d-%m-%Y_%H-%M')
dir_path = Path(__file__).parent
os.makedirs(dir_path, exist_ok=True)
file = os.path.join(dir_path, f"exo_1_refait_{today}.xlsx") #git commit -m "L'ajout du code de l'exo"





# Données ultra-réalistes avec multiples problèmes
data = {
    'order_id': ['ORD-001', 'ORD-002', 'ORD-003', 'ORD-004', 'ORD-005', 'ORD-006', 'ORD-007', 'ORD-008', 'ORD-009', 'ORD-010'],
    'customer_id': ['CUST-01', 'CUST-02', 'CUST-01', 'CUST-03', 'CUST-04', 'CUST-05', 'CUST-03', 'CUST-06', 'CUST-07', 'CUST-08'],
    'customer_name': ['alice martin', 'BOB DUPONT', 'alice martin', 'CHARLIE LEGRAND', 'diana', None, 'EVE', 'frank', 'GRACE', 'HELEN'],
    'customer_email': ['ALICE@EMAIL.COM', 'bob@email.com', 'alice@email.com', 'charlie@email.com', 'diana@email.com', 'invalid', 'eve@email.com', 'frank@email.com', 'grace@email.com', None],
    'product_id': ['P-100', 'P-200', 'P-300', 'P-400', 'P-500', 'P-600', 'P-700', 'P-800', 'P-900', 'P-1000'],
    'product_name': ['Laptop Dell', 'iPhone 15', 'Samsung Tablet', 'Sony Headphones', 'MacBook Pro', 'iPad Air', 'Google Pixel', 'Microsoft Surface', 'Canon Camera', 'Nikon Lens'],
    'category': ['Electronics', 'Mobile', 'Tablet', 'Audio', 'Laptop', 'Tablet', 'Mobile', 'Laptop', 'Camera', 'Camera'],
    'quantity': ['1', '2', '1', '3', '1', '2', '1', '1', '1', '1'],
    'unit_price': ['899.99€', '999.99', '449.99€', '199.99€', '1299.99', '599.99€', '699.99', '899.99€', '549.99€', '399.99€'],
    'discount': ['0%', '10%', '5%', '15%', '0%', '20%', '10%', '5%', '0%', '25%'],
    'order_date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19', '2024-01-20', '2024-01-21', '2024-01-22', '2024-01-23', '2024-01-24'],
    'shipping_city': ['Paris', 'lyon', 'MARSEILLE', 'LILLE', 'Paris', 'TOULOUSE', 'BORDEAUX', 'NICE', 'STRASBOURG', None],
    'status': ['delivered', 'shipped', 'delivered', 'pending', 'delivered', 'shipped', 'delivered', 'pending', 'shipped', 'cancelled']
}

df_brutes = pd.DataFrame(data)
print("📦 DONNÉES E-COMMERCE BRUTES :")
print(df_brutes)
print(f"\n📏 Shape: {df_brutes.shape}")

df = df_brutes.copy()
df = df.drop_duplicates() 
#df['customer_name'] = df['customer_name'].str.title().fillna('Inconnu')
column_text = ['customer_name', 'shipping_city', 'status', 'product_name', 'category']
#df['customer_name'] = (
 #   df['customer_name']
 #   .str.title()
 #   .fillna('Inconnu')
#
df[column_text] = df[column_text].apply(lambda x : x.str.strip().str.title()).fillna('Inconnu')

df['customer_email'] = df['customer_email'].apply(lambda x : x.lower() if pd.notna(x) and '@' in x else None).fillna('email_manquant@domain.com')
df['quantity'] = df['quantity'].astype(int)
df['unit_price'] = (
    df['unit_price']
    .str.replace('€', '', regex=False)
    .str.replace(' ', '', regex=False)
    .replace('', 0, regex=False)
    .astype(float)
    .round(2)
)

df['discount'] = (
    df['discount']
    .str.replace('%', '', regex=False)
    .str.replace(' ', '', regex=False)
    .astype(int) / 100
   
) 


df['order_date'] = pd.to_datetime(
    df['order_date'],
    format='mixed',
    dayfirst=True,
    errors='coerce'

)

df['total_price'] = (df['quantity'] * df['unit_price']).round(2)

print(df)

df_category = (
    df.assign(
        ca_brute = df['total_price'],
        montant_remise = (lambda x : x['ca_brute'] * x['discount']),
        ca_net = (lambda x : x['ca_brute'] - x['montant_remise'])
    )
    .groupby('category')
    .agg(
        {
        'quantity' : 'sum'
        }
    )
)














onglets = {
    'Données Brutes' : df_brutes,
    'Données Néttoyées' : df,
    'Données Par Catégories' : df_category
}

with pd.ExcelWriter(file, engine='xlsxwriter') as writer:
    #df.to_excel(writer, sheet_name='Données Néttoyées', index=False)

    #workbook = writer.book
    #worksheet = writer.sheets['Données Néttoyées']
    for name, data in onglets.items():
        data.to_excel(writer, sheet_name=name, index=False)
        worksheet = writer.sheets[name]
        for i, column in enumerate(data.columns):
            column_letter = data[column].astype(str).str.len().max()
            column_letter = max(column_letter, len(column)) + 3
            worksheet.set_column(i, i, column_letter)



