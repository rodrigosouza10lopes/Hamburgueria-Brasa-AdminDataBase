

# =====================================================================
# SUAS RESPOSTAS
# =====================================================================
# Escreva cada consulta SQL entre as aspas triplas, assim:
#
#   Q1 = """
#   SELECT ...
#   FROM ...
#   """
#
# Depois salve o arquivo (Ctrl+S) e veja o resultado no painel.
# Mexa só no que está ENTRE as aspas triplas.
# =====================================================================

# ---------------------------------------------------------------------
# NÍVEL 1 - AQUECIMENTO
# ---------------------------------------------------------------------

# Q1. Clientes no Centro
# Colunas do resultado: ClientesNoCentro
Q1 = """
SELECT COUNT(*) AS ClientesNoCentro
FROM Clientes
WHERE Bairro = 'Centro';
"""

# Q2. Hambúrgueres acima de R$ 30
# Colunas do resultado: NomeProduto, Preco
Q2 = """
SELECT NomeProduto, Preco
FROM Produtos
WHERE Categoria = 'Hambúrguer'
AND Preco > 30
ORDER BY Preco DESC;
"""

# Q3. Pedidos por status
# Colunas do resultado: Status, QuantidadePedidos
Q3 = """
SELECT 
    Status,
    COUNT(IdPedido) AS Total_Pedidos
FROM 
    Pedidos
WHERE 
    Status IN ('Entregue', 'Cancelado')
GROUP BY 
    Status;


"""

# Q4. Nota média e pedidos sem avaliação
# Colunas do resultado: PedidosEntregues, PedidosAvaliados, PedidosSemAvaliacao, NotaMedia
Q4 = """
SELECT 
    COUNT(*) AS total_entregues,
    COUNT(Avaliacao) AS ComAvaliacao,
    COUNT(*) - COUNT(Avaliacao) AS SemAvaliacao,
    AVG(CAST(Avaliacao AS DECIMAL(4, 2))) AS Nota_Media
FROM 
    Pedidos
WHERE 
    status = 'Entregue';
"""

# Q5. Delivery x Retirada por mês
# Colunas do resultado: Mes, TipoEntrega, QuantidadePedidos
Q5 = """

SELECT 
    MONTH(p.DataPedido) AS mes,
    p.TipoEntrega,
    COUNT(p.IdPedido) AS qtd_pedidos
FROM 
    dbo.Pedidos p
WHERE 
    p.Status = 'entregue'
GROUP BY 
    MONTH(p.DataPedido),
    p.TipoEntrega
ORDER BY 
    mes,
    p.TipoEntrega;

"""

# ---------------------------------------------------------------------
# NÍVEL 2 - CRUZANDO TABELAS
# ---------------------------------------------------------------------

# Q6. Pedidos de janeiro com cliente
# Colunas do resultado: IdPedido, DataPedido, Nome, Bairro, Status
Q6 = """
SELECT Pedidos.IdPedido, Pedidos.DataPedido, Clientes.Nome,Clientes.Bairro, Pedidos.Status
FROM Pedidos
JOIN
Clientes ON Pedidos.IdCliente = Clientes.IdCliente
WHERE Pedidos.DataPedido BETWEEN '2026-01-01' AND '2026-12-31'
ORDER BY Pedidos.DataPedido ASC;

"""

# Q7. Entregas por entregador
# Colunas do resultado: Nome, Entregas
Q7 = """

SELECT Entregadores.IdEntregador, Entregadores.Nome, COUNT( Pedidos.IdPedido) AS Total_Entregas
FROM Pedidos
JOIN
Entregadores ON Pedidos.IdEntregador = Entregadores.IdEntregador
WHERE Pedidos.Status = 'Entregue'
GROUP BY Entregadores.IdEntregador, Entregadores.Nome
ORDER BY Total_entregas DESC;

"""

# Q8. Unidades e faturamento por produto
# Colunas do resultado: NomeProduto, UnidadesVendidas, Faturamento
Q8 = """
SELECT 
    Produtos.NomeProduto, 
    SUM(ItensPedido.Quantidade) AS Total_Unidades, 
    SUM(ItensPedido.Quantidade * ItensPedido.PrecoUnitario) AS FATURAMENTO_TOTAL
FROM 
    ItensPedido
JOIN 
    Produtos ON ItensPedido.IdProduto = Produtos.IdProduto
JOIN 
    Pedidos ON ItensPedido.IdPedido = Pedidos.IdPedido
WHERE 
    Pedidos.Status = 'Entregue'
GROUP BY 
    Produtos.IdProduto, 
    Produtos.NomeProduto
ORDER BY 
    Total_Unidades DESC;

"""

# Q9. Faturamento por categoria
# Colunas do resultado: Categoria, Faturamento
Q9 = """
SELECT Produtos.Categoria, SUM(ItensPedido.Quantidade * ItensPedido.PrecoUnitario) AS Faturamento_Total
FROM ItensPedido
JOIN Produtos ON ItensPedido.IdProduto = Produtos.IdProduto
JOIN Pedidos ON ItensPedido.IdPedido = Pedidos.IdPedido
WHERE Pedidos.Status = 'Entregue'
GROUP BY Produtos.Categoria
ORDER BY Faturamento_Total;

"""

# Q10. Bairros com 7+ pedidos entregues
# Colunas do resultado: Bairro, PedidosEntregues
Q10 = """
SELECT 
    c.Bairro,
    COUNT(p.IdPedido) AS Total_Pedidos
FROM 
    Pedidos p
JOIN 
    Clientes c ON p.IdCliente = c.IdCliente
WHERE 
    p.Status = 'Entregue'
GROUP BY 
    c.Bairro
HAVING 
    COUNT(p.IdPedido) >= 7
ORDER BY 
    Total_Pedidos DESC;


"""

# Q11. Preços praticados do X-Bacon
# Colunas do resultado: PrecoUnitario, Unidades, Faturamento
Q11 = """
SELECT 
    i.PrecoUnitario,
    SUM(i.Quantidade) AS Total_Unidades,
    SUM(i.Quantidade * i.PrecoUnitario) AS Faturamento_Total
FROM 
    ItensPedido i
JOIN 
    Produtos pr ON i.IdProduto = pr.IdProduto
JOIN 
    Pedidos pe ON i.IdPedido = pe.IdPedido
WHERE 
    pr.NomeProduto = 'X-Bacon'
    AND pe.Status = 'Entregue'
GROUP BY 
    i.PrecoUnitario
ORDER BY 
    i.PrecoUnitario ASC;

"""

# ---------------------------------------------------------------------
# NÍVEL 3 - DESAFIO
# ---------------------------------------------------------------------

# Q12. Top 3 clientes (fidelidade)
# Colunas do resultado: Nome, Pedidos, TotalGasto
Q12 = """
SELECT TOP 3
    c.Nome ,
    COUNT(DISTINCT pe.IdPedido) AS Total_Pedidos,
    SUM(i.Quantidade * i.PrecoUnitario) AS Total_Gasto
FROM 
    Clientes c
JOIN 
    Pedidos pe ON c.IdCliente = pe.IdCliente
JOIN 
    ItensPedido i ON pe.IdPedido = i.IdPedido
WHERE 
    pe.Status = 'Entregue'
GROUP BY 
    c.IdCliente,
    c.Nome
ORDER BY 
    Total_Gasto DESC;


"""

# Q13. Faturamento mês a mês
# Colunas do resultado: Mes, PedidosEntregues, Faturamento
Q13 = """
SELECT 
    MONTH(p.DataPedido) AS mes,
    COUNT(DISTINCT p.IdPedido) AS qtd_pedidos_entregues,
    SUM(i.Quantidade * i.PrecoUnitario) AS faturamento_produtos
FROM 
    dbo.Pedidos p
INNER JOIN 
    dbo.ItensPedido i ON p.IdPedido = i.IdPedido
WHERE 
    p.Status = 'entregue'
GROUP BY 
    MONTH(p.DataPedido)
ORDER BY 
    mes;

"""

# Q14. Entregador do trimestre
# Colunas do resultado: Nome, Entregas, NotaMedia
Q14 = """
SELECT 
    e.Nome AS entregador,
    COUNT(p.IdPedido) AS qtd_entregas,
    CAST(AVG(CAST(p.Avaliacao AS DECIMAL(10,2))) AS DECIMAL(10,2)) AS nota_media
FROM 
    dbo.Pedidos p
INNER JOIN 
    dbo.Entregadores e ON p.IdEntregador = e.IdEntregador
WHERE 
    p.Status = 'entregue'
GROUP BY 
    e.IdEntregador, e.Nome
HAVING 
    COUNT(p.IdPedido) >= 4 
    AND AVG(CAST(p.Avaliacao AS DECIMAL(10,2))) >= 4.0;

"""

# Q15. Valor total dos pedidos de março
# Colunas do resultado: IdPedido, Nome, ValorProdutos, TaxaEntrega, ValorTotal
Q15 = """
SELECT 
    c.Nome AS cliente,
    p.IdPedido,
    SUM(i.Quantidade * i.PrecoUnitario) + p.TaxaEntrega AS valor_total_pedido
FROM 
    dbo.Pedidos p
INNER JOIN 
    dbo.Clientes c ON p.IdCliente = c.IdCliente
INNER JOIN 
    dbo.ItensPedido i ON p.IdPedido = i.IdPedido
WHERE 
    p.Status = 'entregue'
    AND MONTH(p.DataPedido) = 3
GROUP BY 
    c.Nome,
    p.IdPedido,
    p.TaxaEntrega
ORDER BY 
    valor_total_pedido DESC;

"""

# Q16. Clientes sem nenhum pedido
# Colunas do resultado: Nome, Bairro, DataCadastro
Q16 = """
SELECT 
    c.Nome AS cliente,
    c.Bairro AS bairro
FROM 
    dbo.Clientes c
LEFT JOIN 
    dbo.Pedidos p ON c.IdCliente = p.IdCliente
WHERE 
    p.IdPedido IS NULL;

"""

# Q17. Produto que nunca foi vendido
# Colunas do resultado: NomeProduto, Categoria, Preco
Q17 = """
SELECT 
    p.NomeProduto
FROM 
    dbo.Produtos p
LEFT JOIN 
    dbo.ItensPedido i ON p.IdProduto = i.IdProduto
WHERE 
    i.IdProduto IS NULL;
"""