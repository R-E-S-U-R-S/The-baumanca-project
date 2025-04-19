-- SELECT *
-- FROM information_schema.table_constraints tc 
-- JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name) 
-- JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema
--   AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
-- WHERE constraint_type = 'PRIMARY KEY' and tc.table_name = 'part' and tc.table_schema='relego';



with set_details as (select part_id, sum(quantity) as sum_quantity
                    from relego.sets_to_parts
                    where sets_to_parts.set_id = ANY (ARRAY[43247])
                    group by part_id)
                    , irrelevant_sets as (select distinct (set_id) as set_id
                         from relego.sets_to_parts
                        left join set_details on set_details.part_id = relego.sets_to_parts.part_id
                         where (relego.sets_to_parts.part_id != ALL (select part_id from set_details))
                            OR (quantity > set_details.sum_quantity))
                        select s.name,s.id,s.parts_volume from relego.set as s
                        where (s.id != ALL (select irrelevant_sets.set_id from irrelevant_sets))
                        AND (s.id != ALL(ARRAY[43247]))




                        