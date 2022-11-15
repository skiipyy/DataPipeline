-- Réaliser une requête un peu plus complexe qui permet de déterminer,
-- par client et sur la période allant du 1er janvier 2019 au 31 décembre 2019, les ventes meuble et déco réalisées.

SELECT
	client_id,
    SUM(CASE WHEN pruduct_type='MEUBLE' THEN prod_price*prod_qty ELSE 0 END) AS ventes_meuble,
    SUM(CASE WHEN pruduct_type='DECO' THEN prod_price*prod_qty ELSE 0 END) AS ventes_deco
FROM TRANSACTION

LEFT JOIN PRODUCT_NOMENCLATURE
ON (TRANSACTION.prod_id = PRODUCT_NOMENCLATURE.product_id)

WHERE date >= '2019-01-01' AND date <= '2019-12-31'

GROUP BY client_id;