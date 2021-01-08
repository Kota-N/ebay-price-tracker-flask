const addBtn = document.querySelector('.add-product-container button');
const deleteBtn = document.querySelector('.delete-product-container button');
const nameInput = document.getElementById('name-input');
const urlInput = document.getElementById('url-input');
const deleteInput = document.getElementById('delete-input');

addBtn.addEventListener('click', async () => {
  const reqData = {
    name: nameInput.value.trim(),
    url: urlInput.value.trim(),
  };

  try {
    const res = await fetch('/ebay_price_tracker/api/products/add', {
      method: 'POST',
      headers: { 'Content-type': 'application/json' },
      body: JSON.stringify(reqData),
    });
    const data = await res.json();
    console.log(data);
  } catch (error) {
    console.log(error);
  }

  nameInput.value = '';
  urlInput.value = '';
  location.reload();
});

deleteBtn.addEventListener('click', async () => {
  const reqData = { name: deleteInput.value };

  try {
    const res = await fetch('/ebay_price_tracker/api/products/delete', {
      method: 'POST',
      headers: { 'Content-type': 'application/json' },
      body: JSON.stringify(reqData),
    });
    const data = await res.json();
    console.log(data);
  } catch (error) {
    console.log(error);
  }

  deleteInput.value = '';
  location.reload();
});
