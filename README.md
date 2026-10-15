# pauls-invoices

Produce PDF invoices from small, editable Python templates. Requires Python 3.11+; the only dependency is `fpdf2`.

## Setup

```
python3 -m venv .venv && .venv/bin/pip install -e .
cp config/config.example.toml config/config.toml
cp config/next_invoice_number.example.toml config/next_invoice_number.toml
cp config/clients/acme.example.toml config/clients/<client>.toml
cp templates/example_template.py templates/<client>.py
```

Edit the copies (they are gitignored). Then, each time you invoice, edit the items in `templates/<client>.py` and run `./invoice <client>` (run `./invoice` alone to list templates).

`config/next_invoice_number.toml` holds the number the next invoice will get; it advances only after a PDF is saved. Move it back to reissue a number. If a PDF with the same name exists you are asked before overwriting.
