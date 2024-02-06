
--PRIMER EJERCICIO
select * from agents a 
where a."name" like 'M%' or a."name" like '%O'

--SERGUNDO EJERCICIO
select * from customers c 
where c.occupation like '%Engineer%'
order by c.occupation asc

--TERCER EJERCICIO
select c.customerid, 
c."name", 
case 
	 when c."age" > 30 then 'Sí' 
	 else 'No' 
	 end as "Mayor30"
from customers c 
order by c."name" 

--CUARTO EJERCICIO
select 
c2.callid ,
c."name" ,
c2.productsold ,
case 
	 when c."age" > 30 then 'Sí' 
	 else 'No' 
	 end as "Mayor30"
from customers c 
inner join calls c2 
on c.customerid = c2.customerid 
where c.occupation like '%Engineer%'
order by c."name" desc

--QUINTO EJERCICIO
select 
c2.occupation ,count(*) AS TotalSales, 
SUM(c.duration) AS Duracion  
from calls c
inner join customers c2 
on c.customerid  = c2.customerid 
where c2.occupation like '%Engineer%'
group by c.productsold ,c.duration,c2.occupation  



