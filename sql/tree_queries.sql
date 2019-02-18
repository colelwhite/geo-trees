-- Get a bunch of info on one tree based on its ID number
select c.description as "Common Name", g.description || ' ' || s.description as "Scientific Name"
       , f.description as "Family", tr.dbh as "Diameter (Inches)", o.description as "Owner"
	   , h.description as "Health" from common_name as c
inner join tree_tab as tt on tt.common_name = id
inner join tree as tr on tt.common_name = tr.name
inner join genus as g on tt.genus = g.id
inner join owner as o on tr.owner = o.id
inner join health as h on tr.health = h.id
inner join species as s on tt.species = s.id
inner join family as f on g.family = f.id
where tr.tree_id = 1;

-- All maples geom
select tr.geom from tree as tr
inner join tree_tab as tt on tt.common_name = tr.name
inner join genus as g on g.id = tt.genus
where g.description = 'Acer';

-- Get health of all ash (Fraxinus) trees in the database
select h.description as "Tree Condition", t.address as "Tree Location" from health as h
left outer join tree as t on t.health = id
inner join tree_tab as tt on tt.common_name = name
inner join genus as g on tt.genus = g.id
where g.description = 'Fraxinus';

-- Spatial query: Get owner information on all conifers within Ward 3
select c.description as "Tree Name", o.description as "Owner"
from tree as tr
inner join ward as w on ST_Intersects(w.geom, tr.geom)
inner join tree_tab as tt on tt.common_name = name
inner join genus as g on g.id = tt.genus
inner join family as f on f.id = g.family
inner join division as div on div.id = f.division
inner join common_name as c on c.id = tt.common_name
inner join owner as o on o.id = tr.owner
where w.ward_num = 3 and div.description = 'Coniferophyta (Conifers)';

-- Find all trees within 100m of a river or stream
-- geom is recast as geography to enable querying by metres rather than degrees
select distinct tr.tree_id from tree as tr
inner join water_course as wc on ST_DWithin(tr.geom::geography, wc.geom::geography, 100);

-- Check the projection of a spatial table
SELECT Find_SRID('public', 'water_course', 'geom');

-- Identify areas of poor tree health - sort of works
SELECT ST_ConcaveHull(ST_Collect(tr.geom),0.80,true)
from tree as tr
join health as h on h.id = tr.health
where h.description in ('Poor', 'Dead');

