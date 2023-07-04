const express = require('express');
const { Pool } = require('pg');

const router = express.Router();

// Configuração da conexão com o banco de dados PostgreSQL
const pool = new Pool({
  user: 'aline',
  host: 'localhost',
  database: 'postes',
  password: 'aline123',
  port: 5432, // Porta padrão do PostgreSQL
});

// Rota para buscar os marcadores no banco de dados
router.get('/api/markers', async (req, res) => {
  try {
    const client = await pool.connect();
    const result = await client.query('SELECT * FROM postes');

    res.json(result.rows);
    client.release();
  } catch (err) {
    console.error('Erro ao buscar marcadores do banco de dados', err);
    res.status(500).json({ error: 'Erro ao buscar marcadores do banco de dados' });
  }
});

module.exports = router;
