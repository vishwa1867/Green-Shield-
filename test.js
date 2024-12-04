async function predict() {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];

    if (!file) {
        alert("Please upload an image.");
        return;
    }

    const reader = new FileReader();
    reader.onloadend = async function () {
        const base64Image = reader.result.split(',')[1];

        try {
            const response = await fetch('http://127.0.0.1:8000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image: base64Image })
            });

            if (response.ok) {
                const result = await response.json();
                document.getElementById("result").innerText = "Prediction Result: " + result.prediction;
            } else {
                const error = await response.json();
                alert("Error: " + error.detail);
            }
        } catch (error) {
            console.error("Error during prediction:", error);
            alert("Failed to predict. Please try again.");
        }
    };

    reader.readAsDataURL(file);
}
