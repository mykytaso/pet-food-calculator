const foodRowsContainer = document.getElementById("food-rows");
const addRowButton = document.getElementById("add-row");
const rowTemplate = document.getElementById("food-row-template");
const totalKcalSpan = document.getElementById("total-kcal");
const totalCostSpan = document.getElementById("total-cost");
const toggleCostBtn = document.getElementById("toggle-cost-btn");

// Create a new food row
function createFood() {
    const clone = rowTemplate.content.cloneNode(true);
    const form = clone.querySelector(".food-row");

    // Get all inputs
    const inputs = form.querySelectorAll("input");
    const kcalOutput = form.querySelector(".kcal-output");
    const costOutput = form.querySelector(".cost-output");

    // Update calculations when any input changes
    const updateFood = () => {
        const values = Array.from(inputs).map(input => parseFloat(input.value) || 0);
        const [kcalPerKg, meals, portionSize, packageSize, price] = values;

        // Calculate calories
        const kcal = kcalPerKg && meals && portionSize ?
            (kcalPerKg / 1000) * portionSize * meals : 0;

        // Calculate cost
        const cost = kcal && packageSize && price ?
            (price / packageSize) * portionSize * meals : 0;

        kcalOutput.textContent = kcal.toFixed(2);
        costOutput.textContent = cost.toFixed(2);
        updateTotal();
    };

    // Add listeners to all inputs
    inputs.forEach(input => input.addEventListener("input", updateFood));

    // Delete button
    form.querySelector(".delete-row").addEventListener("click", () => {
        form.remove();
        updateTotal();
    });

    // Hide cost fields if toggle is OFF
    if (toggleCostBtn.textContent.includes("OFF")) {
        form.querySelectorAll(".cost-field").forEach(el => el.classList.add("hidden"));
    }

    foodRowsContainer.appendChild(form);
}

// Update totals
function updateTotal() {
    let totalKcal = 0;
    let totalCost = 0;

    document.querySelectorAll(".food-row").forEach(row => {
        totalKcal += parseFloat(row.querySelector(".kcal-output").textContent) || 0;
        totalCost += parseFloat(row.querySelector(".cost-output").textContent) || 0;
    });

    totalKcalSpan.textContent = totalKcal.toFixed(2);
    totalCostSpan.textContent = totalCost.toFixed(2);
}

// Toggle cost fields
toggleCostBtn.addEventListener("click", () => {
    // Determine current state
    const isOn = toggleCostBtn.textContent.includes("ON");

    // This toggles the button text.
    toggleCostBtn.textContent = isOn ? "Cost: OFF" : "Cost: ON";

    // This selects all elements with the class cost-field and loops over them.
    document.querySelectorAll(".cost-field").forEach(el => {

        el.classList.toggle("hidden", isOn);

    });
});

// Initialize
addRowButton.addEventListener("click", createFood);
createFood();

// Hide cost fields initially if OFF
if (toggleCostBtn.textContent.includes("OFF")) {
    document.querySelectorAll(".cost-field").forEach(el => {
        if (el.tagName === "TR") el.style.display = "none";
        else el.classList.add("hidden");
    });
}
