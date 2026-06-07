import uuid


def generate_invoice_number():
    return f"INV-{uuid.uuid4().hex[:8].upper()}"

    


