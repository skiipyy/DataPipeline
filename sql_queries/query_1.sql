-- Je vous propose de commencer par réaliser une requête SQL simple permettant de trouver le chiffre d’affaires (le montant total des ventes),
-- jour par jour, du 1er janvier 2019 au 31 décembre 2019. Le résultat sera trié sur la date à laquelle la commande a été passée.
-- Je rappelle que la requête doit être claire : n’hésitez pas à utiliser les mot clefs AS permettant de nommer les champs dans SQL.

SELECT
	date, 
   	SUM(prod_price*prod_qty) AS ventes
FROM TRANSACTION
WHERE date >= '2019-01-01' AND date <= '2019-12-31'
GROUP BY date;