
BEGIN;

CREATE SCHEMA IF NOT exists relego;

create table if not exists relego.set
(
    id           text not null
        primary key,
    name         text    not null,
    released     integer not null,
    theme        text    not null,
    parts_volume integer not null,
    set_img_url text
);

create unique index if not exists set__name__unique_idx
    on relego.set (name);

create table if not exists relego.part
(
    id     SERIAL primary key,
    color  text    not null,
    external_id text not null,
    constraint part__external_id__color__unique
    unique(external_id, color)
);

create table if not exists relego.sets_to_parts
(
    set_id text not null
        references relego.set(id) ON DELETE CASCADE,
    part_id integer not null
        references relego.part(id) ON DELETE CASCADE,
    quantity integer not null,
    constraint sets_to_parts_pk
    unique(set_id, part_id)
);

create index if not exists sets_to_parts__part_id_idx
    on relego.sets_to_parts (part_id);

create index if not exists sets_to_parts__quantity_idx
    on relego.sets_to_parts (quantity);

create table if not exists relego.user_data
(
    login    text not null,
    password text not null,
    set_ids  text[]
);

create unique index if not exists user_data__login__unique_idx
    on relego.user_data (login);

COMMIT;
