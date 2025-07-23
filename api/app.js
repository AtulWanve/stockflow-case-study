const express = require('express');
const app = express();
const port = 3000;

const inventory = [
  { product: 'item-1', quantity: 3, reorder_level: 5 },
  { product: 'item-2', quantity: 7, reorder_level: 5 },
  { product: 'item-3', quantity: 2, reorder_level: 2 },
  { product: 'item-4', quantity: 10, reorder_level: 12 },
];

app.get('/low-stock', (req, res) => {
  const lowStockItems = inventory.filter(item => item.quantity <= item.reorder_level);
  res.json(lowStockItems);
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
