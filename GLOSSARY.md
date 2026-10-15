# Glossary

**Invoice**
A formatted document, saved as a PDF, that bills a Client for work or costs. It carries a number, a date, the Sender's details, the Client's details, one or more Invoice items, a total, and Payment details.

**Invoice item**
One line on an Invoice: the date of the thing being billed, a description, and an amount in pounds. Expenses are Invoice items too, not a separate kind.

**Sender**
The person issuing the Invoice (the user). Their name, address, phone number and email are held once in the Sender profile.

**Sender profile**
The Sender's static details, kept in a config file and shared by every Invoice.

**Client**
The party being billed. A Client's name and address are held in a config file, one per Client.

**Payment details**
Where the Client should pay, usually the Sender's bank details.

**Invoice number**
The identifier of an Invoice, allocated automatically in sequence across all Clients (one global sequence) unless given explicitly. It advances only once the Invoice's PDF has been saved successfully.

**Next invoice number**
The counter, stored in a config file the user can edit, holding the number the next Invoice will receive. Moving it back lets a mistaken Invoice be reissued under the same number.

**Template**
A per-Client script that is edited in place each time to describe the Invoice items for the next Invoice, then run to produce the PDF.
