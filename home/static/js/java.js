// START suppliers.html form functions
var addBtnSuppliers = document.getElementById('addBtn-suppliers');
if (addBtnSuppliers) {
    addBtnSuppliers.addEventListener('click', function() {
        var table = document.getElementById('suppliersTable');
        var newRow = table.insertRow(-1);
        var fields = ['supplier', 'contact', 'email', 'phone'];

        fields.forEach(function(field, index) {
            var cell = newRow.insertCell(index);
            var input = document.createElement('input');
            input.type = 'text';
            input.name = field;
            input.maxLength = 255;
            cell.appendChild(input);
        });

        var saveCell = newRow.insertCell(fields.length);
        var saveBtn = document.createElement('button');
        saveBtn.innerHTML = 'Save';
        saveBtn.onclick = function() { saveSupplier(newRow); };
        saveCell.appendChild(saveBtn);

        this.style.display = 'none';
    });
}

function editRow(button) {
  var row = button.parentNode.parentNode;
  var id = row.getAttribute('data-id');
  var fields = ['supplier', 'contact', 'email', 'phone'];

  fields.forEach(function(field, index) {
      var cell = row.cells[index];
      var value = cell.innerText;
      cell.innerHTML = '';
      var input = document.createElement('input');
      input.type = 'text';
      input.name = field;
      input.value = value;
      input.maxLength = 255;
      cell.appendChild(input);
  });

  var saveBtn = document.createElement('button');
  saveBtn.innerHTML = 'Save';
  saveBtn.onclick = function() { saveEditedRow(row, id); };
  button.parentNode.replaceChild(saveBtn, button);
}

function deleteRow(button) {
  var row = button.parentNode.parentNode;
  var id = row.getAttribute('data-id');

  if (confirm('Are you sure you want to delete this supplier?')) {
      fetch('/delete_supplier/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken') // Get CSRF token from cookies
          },
          body: JSON.stringify({ 'id': id })
      })
      .then(response => response.json())
      .then(data => {
          if(data.status === 'success') {
              alert('Supplier deleted successfully');
              location.reload();
          } else {
              alert('Error deleting supplier: ' + data.message);
          }
      })
      .catch((error) => {
          console.error('Error:', error);
          alert('An error occurred while deleting the supplier.');
      });
  }
}

function saveEditedRow(row, id) {
  var supplierData = {
      'id': id,
      'supplier': row.cells[0].getElementsByTagName('input')[0].value,
      'contact': row.cells[1].getElementsByTagName('input')[0].value,
      'email': row.cells[2].getElementsByTagName('input')[0].value,
      'phone': row.cells[3].getElementsByTagName('input')[0].value,
      'csrfmiddlewaretoken': getCookie('csrftoken') // Get CSRF token from cookies
  };

  fetch('/update_supplier/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': supplierData.csrfmiddlewaretoken
      },
      body: JSON.stringify(supplierData)
  })
  .then(response => response.json())
  .then(data => {
      if(data.status === 'success') {
          alert('Supplier updated successfully');
          location.reload();
      } else {
          alert('Error updating supplier: ' + data.message);
      }
  })
  .catch((error) => {
      console.error('Error:', error);
      alert('An error occurred while updating the supplier.');
  });
}

function saveSupplier(row) {
  var supplierData = {
      'supplier': row.cells[0].getElementsByTagName('input')[0].value,
      'contact': row.cells[1].getElementsByTagName('input')[0].value,
      'email': row.cells[2].getElementsByTagName('input')[0].value,
      'phone': row.cells[3].getElementsByTagName('input')[0].value,
      'csrfmiddlewaretoken': getCookie('csrftoken') // Get CSRF token from cookies
  };

  fetch('/save_supplier/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': supplierData.csrfmiddlewaretoken
      },
      body: JSON.stringify(supplierData)
  })
  .then(response => response.json())
  .then(data => {
      if(data.status === 'success') {
          alert('Supplier saved successfully');
          location.reload();  // Reload the page
      } else {
          alert('Error saving supplier: ' + data.message);
      }
  })
  .catch((error) => {
      console.error('Error:', error);
      alert('An error occurred while saving the supplier.');
  });
}
// END suppliers.html form functions





function openPopup(productId) {
  var modal = document.getElementById('popupModal-' + productId);
  modal.style.display = 'block';
}

function closePopup(productId) {
  var modal = document.getElementById('popupModal-' + productId);
  modal.style.display = 'none';
}

function toggleEditSave(productId) {
  var table = document.getElementById('table-' + productId);
  var modalContent = document.getElementById('popupModal-' + productId).querySelector('.modal-content');
  var btn = event.target;
  var materialsNotIncludedSection = document.getElementById('materials-not-included-' + productId);

  if (btn.textContent === 'Edit') {
      // Add a new heading with the text 'Selected Materials'
      var newHeading = document.createElement('h4');
      newHeading.id = 'edit-heading-' + productId;
      newHeading.textContent = 'Selected Materials';
      modalContent.insertBefore(newHeading, table);

      // Create 'Materials Not Included' section if it doesn't exist
      if (!materialsNotIncludedSection) {
          materialsNotIncludedSection = document.createElement('div');
          materialsNotIncludedSection.id = 'materials-not-included-' + productId;
          materialsNotIncludedSection.className = 'materials-not-included';
          materialsNotIncludedSection.innerHTML = `
            <div class="heading-dropdown" onclick="toggleDropdown('${productId}')">
              // <h4>Materials Not Included</h4>
              <span class="dropdown-arrow">&#9660;</span>
            </div>
            <div id="dropdown-content-${productId}" class="dropdown-content" style="display:none;">
              <table>
                <tr>
                  <th>Material</th>
                  <th>Units</th>
                  <th>Rate</th>
                  <th>Quantity</th>
                </tr>
                <!-- Additional rows can be dynamically inserted here -->
              </table>
            </div>
          `;
          modalContent.appendChild(materialsNotIncludedSection);
      }

      // Convert quantity display to editable inputs
      var quantityCells = table.querySelectorAll('.quantity-cell');
      quantityCells.forEach(function(cell) {
          var quantity = cell.innerText;
          cell.innerHTML = '<input type="number" value="' + quantity + '" style="width: 100%;">';
      });

      btn.textContent = 'Save';
  } else {
      // Remove the new heading when switching back from 'Edit' to 'Save'
      var editHeading = document.getElementById('edit-heading-' + productId);
      if (editHeading) {
          modalContent.removeChild(editHeading);
      }

      // Remove 'Materials Not Included' section when switching back from 'Edit' to 'Save'
      if (materialsNotIncludedSection) {
          modalContent.removeChild(materialsNotIncludedSection);
      }

      // Convert inputs back to text and handle the save logic
      var quantityInputs = table.querySelectorAll('.quantity-cell input');
      var quantities = [];
      quantityInputs.forEach(function(input) {
          var cell = input.parentElement;
          var quantity = input.value;
          cell.innerText = quantity;  // Convert back to text
          quantities.push(quantity);  // Collect data for saving
      });

      btn.textContent = 'Edit';
  }
}

function saveMaterials(productId) {
  // Find the table for this product
  var table = document.getElementById('table-' + productId);
  var rows = table.getElementsByTagName('tr');

  // Array to store the materials data
  var materialsData = [];

  // Iterate over each row (skip the header row)
  for (var i = 1; i < rows.length; i++) {
      var row = rows[i];

      // Extracting the data-product-id and data-material-id
      var productID = row.getAttribute('data-product-id');
      var materialID = row.getAttribute('data-material-id');

      // Find the quantity input in this row
      var quantityInput = row.querySelector('.quantity-cell input');
      var quantity = quantityInput.value;

      // Add to the materials data array
      materialsData.push({
          product: productID,
          material: materialID,
          quantity: quantity
      });
  }

  // Now, materialsData contains all the information needed to save
  // You can send this to your server using AJAX or another method
  console.log(materialsData);
}

function getCookie(name) {// Function to get CSRF token
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

function populateDropdownWithMaterials(dropdownContent, allMaterialsData) {
  console.log("Populating dropdown with materials", allMaterialsData);
  allMaterialsData.forEach(material => {
    console.log("Adding material to dropdown:", material.fields);
    var row = dropdownContent.insertRow(-1);

    var cellMaterial = row.insertCell(0);
    cellMaterial.innerHTML = material.fields.material;

    var cellUnits = row.insertCell(1);
    cellUnits.innerHTML = material.fields.units;

    var cellRate = row.insertCell(2);
    cellRate.innerHTML = material.fields.rate;

    var cellQuantity = row.insertCell(3);
    cellQuantity.innerHTML = '<input type="number" style="width: 100%;">';
  });
  console.log("populateDropdown function called");
}

function toggleDropdown(productId, materialType) {
  console.log("toggleDropdown called for productId:", productId, "and materialType:", materialType);

  var dropdownContent = document.getElementById('dropdown-content-' + productId).querySelector('table');
  var dropdownHeader = document.querySelector('.heading-dropdown');
  var dropdownArrow = dropdownHeader.querySelector('.dropdown-arrow');

  console.log("Dropdown content element:", dropdownContent);
  console.log("Dropdown header element:", dropdownHeader);
  console.log("All materials:", allMaterialsData);

  dropdownContent.style.display = dropdownContent.style.display === 'none' ? 'block' : 'none';

  if (dropdownContent.style.display === 'block') {
    dropdownArrow.innerHTML = '&#9660;';
    console.log("Dropdown is now open");
    if (materialType === 'all_materials') {
      console.log("Material type is all_materials, populating dropdown...");
      populateDropdownWithMaterials(dropdownContent, allMaterialsData);
    }
  } else {
    dropdownArrow.innerHTML = '&#9654;';
    console.log("Dropdown is now closed");
  }
}


