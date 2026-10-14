document.addEventListener("DOMContentLoaded", () => {
    const orderForm = document.getElementById("order-form");

    if (!orderForm) {
        return;
    }

    const quantityInputs = [
        ...orderForm.querySelectorAll(".quantity-input")
    ];

    const itemCount = document.getElementById("item-count");
    const cartTotal = document.getElementById("cart-total");

    function updateCart() {
        let count = 0;
        let total = 0;

        quantityInputs.forEach((input) => {
            let quantity = Number.parseInt(input.value, 10);

            if (!Number.isFinite(quantity)) {
                quantity = 0;
            }

            quantity = Math.max(0, Math.min(10, quantity));
            input.value = quantity;

            count += quantity;
            total += quantity * Number(input.dataset.price);
        });

        itemCount.textContent = count;
        cartTotal.textContent = total.toFixed(2);
    }

    orderForm.querySelectorAll(".quantity-button").forEach((button) => {
        button.addEventListener("click", () => {
            const itemId = button.dataset.itemId;
            const input = document.getElementById(`quantity-${itemId}`);

            if (!input) {
                return;
            }

            let quantity = Number.parseInt(input.value, 10);

            if (!Number.isFinite(quantity)) {
                quantity = 0;
            }

            if (button.dataset.action === "increase" && quantity < 10) {
                quantity += 1;
            } else if (
                button.dataset.action === "decrease" &&
                quantity > 0
            ) {
                quantity -= 1;
            }

            input.value = quantity;
            updateCart();
        });
    });

    quantityInputs.forEach((input) => {
        input.addEventListener("input", updateCart);
        input.addEventListener("change", updateCart);
    });

    orderForm.addEventListener("submit", (event) => {
        updateCart();

        const hasItems = quantityInputs.some(
            (input) => Number(input.value) > 0
        );

        if (!hasItems) {
            event.preventDefault();

            let errorMessage = document.getElementById("cart-error");

            if (!errorMessage) {
                errorMessage = document.createElement("p");
                errorMessage.id = "cart-error";
                errorMessage.className = "message error-message";
                errorMessage.setAttribute("role", "alert");

                orderForm.prepend(errorMessage);
            }

            errorMessage.textContent =
                "Please select at least one item before placing your order.";
        }
    });

    updateCart();
});