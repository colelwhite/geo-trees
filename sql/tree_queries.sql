-- Get a bunch of info on one tree based on its ID number
select c.description as "Common Name", g.description || s.description as "Scientific Name"
       , f.description as "Family", tr.dbh as "Diameter (Inches)", o.description as "Owner"
	   , h.description as "Health" from common_name c
join tree_tab tt on tt.common_name = id
join tree tr on tt.common_name = tr.name
join genus g on tt.genus = g.id
join owner o on tr.owner = o.id
join health h on tr.health = h.id
join species s on tt.species = s.id
join family f on g.family = f.id
where tr.tree_id = 1;

-- Get health of all ash (Fraxinus) trees in the database
select h.descriptionas "Tree Condition", t.address as "Tree Location" from health h
join tree t on t.health = id
join tree_tab tt on tt.common_name = name
join genus g on tt.genus = g.id
where g.description = 'Fraxinus';