<?php
// Database connection configuration
$servername = "localhost";     // Or your specific server address if not localhost
$username = "root";            // Your MySQL Workbench username
$password = "your_password";   // Your MySQL Workbench password
$dbname = "contact_info";      // The database created in MySQL Workbench

// Create connection using MySQLi
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Handle form submission
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST['name'];
    $phone_number = $_POST['phone_number'];
    $email = $_POST['email'];
    $message = $_POST['message'];

    // Prepare and execute the SQL insert statement
    $stmt = $conn->prepare("INSERT INTO contacts (name, phone_number, email, message) VALUES (?, ?, ?, ?)");
    $stmt->bind_param("ssss", $name, $phone_number, $email, $message);

    // Execute the query
    if ($stmt->execute()) {
        echo "Message submitted successfully!";
    } else {
        echo "Error: " . $stmt->error;
    }

    $stmt->close();
}

$conn->close();
?>
