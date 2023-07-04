const express = require('express');
const app = express();
const routes = require('./routes');

// Configura a pasta onde o arquivo index.html está localizado
app.use(express.static(__dirname + '/public'));

// Configura as rotas
app.use('/', routes);

const port = 7000; // Porta do servidor
app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}`);
});
