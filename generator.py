import base64

def generate_app(brief, attachments, round_num):
    """
    Generates the application code based on the brief, attachments, and round number.
    For now, it only handles the 'sum-of-sales' task.
    """
    if "sum-of-sales" in brief:
        if round_num == 1:
            return generate_sum_of_sales_app_round1(attachments)
        elif round_num == 2:
            return generate_sum_of_sales_app_round2(attachments)

    # Placeholder for LLM-based generation for other tasks
    return None, None, None

def generate_sum_of_sales_app_round1(attachments):
    """
    Generates the HTML, CSS, and JavaScript for the 'sum-of-sales' task, round 1.
    """
    csv_attachment = next((att for att in attachments if att["name"] == "data.csv"), None)
    if not csv_attachment:
        raise ValueError("Missing data.csv attachment")

    csv_data_encoded = csv_attachment["url"].split(",")[1]
    csv_data = base64.b64decode(csv_data_encoded).decode("utf-8")

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sales Summary</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1>Sales Summary</h1>
        <p>Total Sales: <span id="total-sales"></span></p>
    </div>
    <script>
        const csvData = `{csv_data}`;
        const rows = csvData.split('\\n').slice(1);
        let totalSales = 0;
        for (const row of rows) {{
            const columns = row.split(',');
            if (columns.length >= 2) {{
                totalSales += parseFloat(columns[1]);
            }}
        }}
        document.getElementById('total-sales').textContent = totalSales.toFixed(2);
    </script>
</body>
</html>
"""
    return "index.html", html, None

def generate_sum_of_sales_app_round2(attachments):
    """
    Generates the HTML, CSS, and JavaScript for the 'sum-of-sales' task, round 2.
    """
    csv_attachment = next((att for att in attachments if att["name"] == "data.csv"), None)
    if not csv_attachment:
        raise ValueError("Missing data.csv attachment")

    csv_data_encoded = csv_attachment["url"].split(",")[1]
    csv_data = base64.b64decode(csv_data_encoded).decode("utf-8")

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sales Summary</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1>Sales Summary</h1>
        <p>Total Sales: <span id="total-sales"></span></p>
        <table class="table" id="product-sales">
            <thead>
                <tr>
                    <th>Product</th>
                    <th>Total Sales</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        </table>
    </div>
    <script>
        const csvData = `{csv_data}`;
        const rows = csvData.split('\\n').slice(1);
        let totalSales = 0;
        const productSales = {{}};

        for (const row of rows) {{
            const columns = row.split(',');
            if (columns.length >= 2) {{
                const product = columns[0];
                const sales = parseFloat(columns[1]);
                totalSales += sales;
                productSales[product] = (productSales[product] || 0) + sales;
            }}
        }}

        document.getElementById('total-sales').textContent = totalSales.toFixed(2);

        const tableBody = document.querySelector('#product-sales tbody');
        for (const product in productSales) {{
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${{product}}</td>
                <td>${{productSales[product].toFixed(2)}}</td>
            `;
            tableBody.appendChild(row);
        }}
    </script>
</body>
</html>
"""
    return "index.html", html, None