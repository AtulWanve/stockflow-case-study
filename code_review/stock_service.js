let inventory = {
  'item-1': 10,
  'item-2': 0,
  'item-3': 5,
};

function deductStock(itemId, qty) {
  if (!(itemId in inventory)) throw new Error("Item does not exist");
  if (qty <= 0) throw new Error("Invalid quantity");
  if (inventory[itemId] < qty) throw new Error("Insufficient stock");

  inventory[itemId] -= qty;
  return inventory[itemId];
}

module.exports = { deductStock, inventory };
