<?php
$servername = "localhost"; // Endereço do servidor
$username = "root"; // Usuário do banco de dados
$password = "1864"; // Senha do banco de dados
$dbname = "feedback_db"; // Nome do banco de dados

// Cria conexão
$conn = new mysqli($servername, $username, $password, $dbname);

// Verifica a conexão
if ($conn->connect_error) {
    die("Conexão falhou: " . $conn->connect_error);
}

// Configuração do cabeçalho para JSON
header('Content-Type: application/json');

// Função para carregar todos os feedbacks
if ($_SERVER['REQUEST_METHOD'] == 'GET') {
    $sql = "SELECT * FROM feedbacks ORDER BY date DESC";
    $result = $conn->query($sql);

    $feedbacks = [];
    while ($row = $result->fetch_assoc()) {
        $feedbacks[] = $row;
    }
    echo json_encode($feedbacks);

// Função para adicionar um novo feedback
} elseif ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $data = json_decode(file_get_contents('php://input'), true);
    
    $username = $data['username'];
    $level = $data['level'];
    $area = $data['area'];
    $feedback = $data['feedback'];

    $stmt = $conn->prepare("INSERT INTO feedbacks (username, level, area, feedback) VALUES (?, ?, ?, ?)");
    $stmt->bind_param("ssss", $username, $level, $area, $feedback);

    if ($stmt->execute()) {
        echo json_encode(['message' => 'Feedback adicionado com sucesso']);
    } else {
        echo json_encode(['message' => 'Erro ao adicionar feedback']);
    }

    $stmt->close();
}

$conn->close();
?>