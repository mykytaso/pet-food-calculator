    const foodRowsContainer = document.getElementById("food-rows");
    const addRowButton = document.getElementById("add-row");
    const rowTemplate = document.getElementById("food-row-template");
    const totalKcalSpan = document.getElementById("total-kcal");
    const totalCostSpan = document.getElementById("total-cost");
    const toggleCostCheckbox = document.getElementById("toggle-cost");

    function createRow() {
      // Clone the template and set up the new row
      const clone = rowTemplate.content.cloneNode(true);
      // Ensure the cloned row has a unique class for identification
      const form = clone.querySelector(".food-row");

      // Clear previous values in the cloned row
      const inputs = {
        kcalPerKg: form.querySelector(".kcalPerKg"),
        mealsNumber: form.querySelector(".mealsNumber"),
        portionSize: form.querySelector(".portionSize"),
        packageSize: form.querySelector(".packageSize"),
        price: form.querySelector(".price")
      };

      const kcalOutput = form.querySelector(".kcal-output");
      const costOutput = form.querySelector(".cost-output");

      const updateRow = () => {
        const kcal_per_kg = parseFloat(inputs.kcalPerKg.value);
        const meals_number = parseFloat(inputs.mealsNumber.value);
        const portion_size = parseFloat(inputs.portionSize.value);
        const package_size = parseFloat(inputs.packageSize.value);
        const price = parseFloat(inputs.price.value);

        if (!kcal_per_kg || !meals_number || !portion_size) {
          kcalOutput.textContent = "";
          costOutput.textContent = "";
          updateTotal();
          return;
        }

        const kcal = (kcal_per_kg / 1000) * portion_size * meals_number;
        let cost = 0;

        if (package_size && price) {
          cost = (price / package_size) * portion_size * meals_number;
        }

        kcalOutput.textContent = kcal.toFixed(2);
        costOutput.textContent = cost.toFixed(2);

        // Update the total kcal and cost
        updateTotal();
      };

      for (let key in inputs) {
        inputs[key].addEventListener("input", updateRow);
      }

      form.querySelector(".delete-row").addEventListener("click", () => {
        form.remove();

        // Update the total kcal and cost
        updateTotal();
      });

      // Initialize the row with empty values
      if (!toggleCostCheckbox.checked) {
        form.querySelectorAll(".cost-field").forEach(el => {
          el.classList.add("hidden");
        });
      }

      foodRowsContainer.appendChild(form);
    }




    // Update the total kcal and cost
    function updateTotal() {
      let totalKcal = 0;
      let totalCost = 0;

      // Gets all .food-row on the page, then loops through each row using .forEach().
      document.querySelectorAll(".food-row").forEach(row => {
        // Finds the .kcal-output <span> inside the row. Gets the text. Converts it to a number.
        // If it’s missing or invalid (NaN), the || 0 makes it fallback to 0.
        const kcal = parseFloat(row.querySelector(".kcal-output")?.textContent) || 0;
        const cost = parseFloat(row.querySelector(".cost-output")?.textContent) || 0;

        totalKcal += kcal;
        totalCost += cost;
      });

      // Set the text inside the “Total kcal” and “Total cost” <span> elements.
      totalKcalSpan.textContent = totalKcal.toFixed(2);
      totalCostSpan.textContent = totalCost.toFixed(2);
    }





    toggleCostCheckbox.addEventListener("change", () => {
      const showCost = toggleCostCheckbox.checked;

      document.querySelectorAll(".cost-field").forEach(el => {
        el.classList.toggle("hidden", !showCost);
      });

      totalCostSpan.parentElement.style.display = showCost ? "block" : "none";
    });

    addRowButton.addEventListener("click", createRow);

    createRow();

    if (!toggleCostCheckbox.checked) {
      totalCostSpan.parentElement.style.display = "none";
    }