# Copy to templates/<client>.py, set the client, and edit the items each time.
from invoices import Invoice

inv = Invoice(client="acme", notes="Thank you for your business.")

inv.add_item("2026-10-01", "Consulting", "450.00")
inv.add_item("2026-10-03", "Train fare to client site", "32.40")

print(inv.save())
