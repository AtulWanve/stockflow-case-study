const { deductStock, inventory } = require('./stock_service');

try {
  console.log("Before:", inventory['item-1']);
  deductStock('item-1', 15);  // Try removing more than available
  console.log("After:", inventory['item-1']);
} catch (e) {
  console.error("Error:", e.message);
}
