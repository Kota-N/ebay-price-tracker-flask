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

  if (!nameInput.value.trim() == '' || !urlInput.value.trim() == '') {
    if (
      confirm(
        `Insert a product?\n\nName: ${reqData.name}\nURL: '${reqData.url}'`
      )
    ) {
      try {
        const res = await fetch('/ebay_price_tracker/api/products/add', {
          method: 'POST',
          headers: { 'Content-type': 'application/json' },
          body: JSON.stringify(reqData),
        });
        const data = await res.json();
        alert(`Inserted!\n\n${data.added_name}`);
        console.log(data);
      } catch (error) {
        console.log(error);
        alert(error);
      }

      nameInput.value = '';
      urlInput.value = '';
      location.reload();
    }
  } else alert('Cannot insert an empty value');
});

deleteBtn.addEventListener('click', async () => {
  const reqData = { name: deleteInput.value };

  if (confirm(`Delete a product?\n\nName: ${reqData.name}`)) {
    try {
      const res = await fetch('/ebay_price_tracker/api/products/delete', {
        method: 'POST',
        headers: { 'Content-type': 'application/json' },
        body: JSON.stringify(reqData),
      });
      const data = await res.json();
      alert(`Deleted!\n\n${data.deleted_name}`);
      console.log(data);
    } catch (error) {
      console.log(error);
      alert(error);
    }
  }

  deleteInput.value = '';
  location.reload();
});
