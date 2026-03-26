<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cash Tracker Pro</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f9; padding: 20px; }
        .card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); max-width: 400px; margin: auto; }
        h2 { text-align: center; color: #2c3e50; margin-bottom: 20px; }
        .input-group { margin-bottom: 15px; display: flex; align-items: center; justify-content: space-between; }
        label { font-weight: bold; width: 100px; }
        input { padding: 8px; border: 1px solid #ccc; border-radius: 5px; width: 120px; text-align: center; font-size: 16px; }
        .total-section { background: #e8f5e9; padding: 15px; border-radius: 10px; margin-top: 20px; text-align: center; }
        #grandTotal { font-size: 24px; font-weight: bold; color: #2e7d32; }
        .btn-whatsapp { background: #25D366; color: white; border: none; padding: 12px; width: 100%; border-radius: 10px; font-size: 18px; cursor: pointer; margin-top: 15px; font-weight: bold; }
        .header-inputs { margin-bottom: 20px; border-bottom: 2px solid #eee; padding-bottom: 15px; }
        .header-inputs input { width: 100%; box-sizing: border-box; margin-top: 5px; text-align: left; }
    </style>
</head>
<body>

<div class="card">
    <h2>🏦 Cash Counter</h2>
    
    <div class="header-inputs">
        <label>Name:</label>
        <input type="text" id="userName" value="Sandeep">
        <label style="display:block; margin-top:10px;">Date:</label>
        <input type="text" id="currDate" value="26-03-2026">
    </div>

    <div id="notesContainer">
        </div>

    <div class="input-group" style="border-top: 1px solid #eee; padding-top: 10px;">
        <label>🪙 Coins (Total Value):</label>
        <input type="number" id="coinInput" placeholder="Total Rs" oninput="calculate()">
    </div>

    <div class="total-section">
        <div>GRAND TOTAL</div>
        <div id="grandTotal">₹ 0</div>
    </div>

    <button class="btn-whatsapp" onclick="shareWhatsApp()">📲 Share on WhatsApp</button>
</div>

<script>
    const notes = [2000, 500, 200, 100, 50, 20, 10];
    const container = document.getElementById('notesContainer');

    // Create Note Rows
    notes.forEach(val => {
        container.innerHTML += `
            <div class="input-group">
                <label>₹ ${val} Note:</label>
                <input type="number" class="note-qty" data-val="${val}" placeholder="Qty" oninput="calculate()">
            </div>
        `;
    });

    function calculate() {
        let total = 0;
        document.querySelectorAll('.note-qty').forEach(input => {
            let val = parseInt(input.getAttribute('data-val'));
            let qty = parseInt(input.value) || 0;
            total += val * qty;
        });

        let coins = parseInt(document.getElementById('coinInput').value) || 0;
        total += coins;

        document.getElementById('grandTotal').innerText = "₹ " + total.toLocaleString('en-IN');
        return total;
    }

    function shareWhatsApp() {
        let name = document.getElementById('userName').value;
        let date = document.getElementById('currDate').value;
        let total = calculate();
        
        let text = `🏦 *CASH REPORT*\n👤 *Name:* ${name}\n📅 *Date:* ${date}\n\n`;
        
        document.querySelectorAll('.note-qty').forEach(input => {
            let val = input.getAttribute('data-val');
            let qty = input.value;
            if(qty > 0) text += `💵 ₹${val} x ${qty} = ₹${val * qty}\n`;
        });

        let coins = document.getElementById('coinInput').value;
        if(coins > 0) text += `🪙 Coins Total = ₹${coins}\n`;

        text += `\n💰 *GRAND TOTAL: ₹${total}*`;
        
        let url = "https://wa.me/?text=" + encodeURIComponent(text);
        window.open(url, '_blank');
    }
</script>

</body>
</html>
