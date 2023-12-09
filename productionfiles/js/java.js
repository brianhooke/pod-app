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

function populateDropdownWithMaterials(dropdownContent, allMaterials) {
  // Assuming allMaterials is a list of material objects
  allMaterials.forEach(material => {
      var row = dropdownContent.insertRow(-1); // Append a new row to the table

      var cellMaterial = row.insertCell(0);
      cellMaterial.innerHTML = material.material;

      var cellUnits = row.insertCell(1);
      cellUnits.innerHTML = material.units;

      var cellRate = row.insertCell(2);
      cellRate.innerHTML = material.rate;

      var cellQuantity = row.insertCell(3);
      cellQuantity.innerHTML = '<input type="number" style="width: 100%;">';
  });
}

function toggleDropdown(productId, materialType) {
  var dropdownContent = document.getElementById('dropdown-content-' + productId).querySelector('table');
  var dropdownHeader = document.querySelector('.heading-dropdown'); // Adjust if there are multiple dropdowns
  var dropdownArrow = dropdownHeader.querySelector('.dropdown-arrow');

  dropdownContent.style.display = dropdownContent.style.display === 'none' ? 'block' : 'none';

  if (dropdownContent.style.display === 'block') {
      // Change to downward arrow when the dropdown is open
      dropdownArrow.innerHTML = '&#9660;';

      if (materialType === 'allMaterials') {
          // Assuming allMaterials is available as a global variable or fetched here
          populateDropdownWithMaterials(dropdownContent, allMaterials);
      }
  } else {
      // Change back to right arrow when the dropdown is closed
      dropdownArrow.innerHTML = '&#9654;';
  }
}
